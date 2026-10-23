#!/usr/bin/env python3
"""
Ghost Writer — Podcast Export Script
Turns the episode scripts in podcast/scripts/ into MP3 episodes, using only
free and open-source tools: Piper (offline neural TTS) + ffmpeg.

Usage:
  python3 export_podcast.py voices [lang]          # list Piper voices (default: book language)
  python3 export_podcast.py sample VOICE [...]     # download voice(s), render a short sample
  python3 export_podcast.py build [scripts...]     # render episodes (default: all scripts)
  python3 export_podcast.py feed                   # write podcast/feed.xml (RSS)

Script tags (one per line):
  [pause 2]            silence, in seconds
  [voice NAME]         switch to a voice defined in podcast.voices (dialogue, characters)
  [narrator]           back to the narrator voice

Requires: pip install piper-tts numpy · ffmpeg in PATH
"""

import json
import re
import shutil
import subprocess
import sys
import wave
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from urllib.request import urlopen
from xml.sax.saxutils import escape

import numpy as np


DEFAULT_VOICES = {
    "it": "it_IT-paola-medium",
    "en": "en_US-lessac-medium",
    "es": "es_ES-davefx-medium",
    "fr": "fr_FR-siwis-medium",
    "de": "de_DE-thorsten-medium",
    "pt": "pt_BR-faber-medium",
}

DEFAULT_PODCAST = {
    "voice": None,            # Piper voice id, e.g. it_IT-paola-medium
    "speaker": None,          # speaker id, only for multi-speaker voices
    "speed": 1.0,             # 1.0 = natural, 0.9 = slower, 1.1 = faster
    "sentence_pause": 0.35,   # seconds between sentences
    "paragraph_pause": 0.9,   # seconds between paragraphs
    "voices": {},             # extra voices: {"NAME": {"voice": "...", "speaker": null, "speed": 1.0}}
    "intro_music": None,      # path to an audio file (CC0 / own music)
    "outro_music": None,
    "bitrate": "96k",
    "base_url": "",           # public URL where the MP3s will be hosted (for feed.xml)
}

SAMPLE_RATE = 22050
VOICES_JSON = "https://huggingface.co/rhasspy/piper-voices/resolve/main/voices.json?download=true"


# ─── Config ───────────────────────────────────────────────────────────────────

def load_config(project_dir):
    config_path = Path(project_dir) / "book.config.json"
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            return json.load(f)
    return {}

def podcast_settings(config):
    settings = dict(DEFAULT_PODCAST)
    settings.update(config.get("podcast") or {})
    lang = (config.get("language") or "en")[:2]
    if not settings["voice"]:
        settings["voice"] = DEFAULT_VOICES.get(lang, DEFAULT_VOICES["en"])
    return settings

def author_name(config):
    return (
        config.get("author_profile", {}).get("name") or
        config.get("author", {}).get("name") or
        "Author"
    )


# ─── Voices ───────────────────────────────────────────────────────────────────

def voices_dir(project_dir):
    d = Path(project_dir) / "podcast" / "voices"
    d.mkdir(parents=True, exist_ok=True)
    return d

def list_voices(lang):
    with urlopen(VOICES_JSON) as r:
        catalog = json.load(r)
    rows = []
    for key, v in sorted(catalog.items()):
        if not key.lower().startswith(lang.lower()):
            continue
        speakers = len(v.get("speaker_id_map") or {}) or 1
        rows.append(f"  {key:<36} quality={v.get('quality', '?'):<8} speakers={speakers}")
    print("\n".join(rows) if rows else f"No voices found for '{lang}'.")

def ensure_voice(project_dir, voice_id):
    d = voices_dir(project_dir)
    model = d / f"{voice_id}.onnx"
    if not model.exists() or not (d / f"{voice_id}.onnx.json").exists():
        print(f"Downloading voice {voice_id}...")
        subprocess.run(
            [sys.executable, "-m", "piper.download_voices", voice_id, "--download-dir", str(d)],
            check=True,
        )
    return model

_loaded = {}

def load_voice(project_dir, voice_id):
    if voice_id not in _loaded:
        from piper import PiperVoice
        _loaded[voice_id] = PiperVoice.load(str(ensure_voice(project_dir, voice_id)))
    return _loaded[voice_id]


# ─── Synthesis ────────────────────────────────────────────────────────────────

def synthesize(project_dir, text, voice_cfg):
    """Return mono int16 audio at SAMPLE_RATE for one sentence."""
    from piper import SynthesisConfig
    voice = load_voice(project_dir, voice_cfg["voice"])
    syn = SynthesisConfig(
        speaker_id=voice_cfg.get("speaker"),
        length_scale=1.0 / float(voice_cfg.get("speed") or 1.0),
    )
    chunks, rate = [], SAMPLE_RATE
    for chunk in voice.synthesize(text, syn_config=syn):
        rate = chunk.sample_rate
        chunks.append(np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16))
    audio = np.concatenate(chunks) if chunks else np.zeros(0, dtype=np.int16)
    return resample(audio, rate)

def resample(audio, rate):
    if rate == SAMPLE_RATE or audio.size == 0:
        return audio
    n = int(round(audio.size * SAMPLE_RATE / rate))
    x = np.linspace(0, audio.size - 1, n)
    return np.interp(x, np.arange(audio.size), audio).astype(np.int16)

def silence(seconds):
    return np.zeros(int(SAMPLE_RATE * max(seconds, 0)), dtype=np.int16)


# ─── Script parsing ───────────────────────────────────────────────────────────

def split_frontmatter(text):
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"\'')
        text = text[m.end():]
    return meta, text

def clean_inline(line):
    line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)   # links → text
    line = re.sub(r"[*_`]+", "", line)                        # emphasis
    line = re.sub(r"^\s*([-*+]|\d+\.)\s+", "", line)          # list markers
    line = re.sub(r"^\s*>\s?", "", line)                      # blockquote
    return line.strip()

def split_sentences(paragraph):
    parts = re.split(r"(?<=[.!?…»”])\s+", paragraph)
    return [p for p in (s.strip() for s in parts) if p]

def parse_script(text):
    """Yield events: ('say', voice_name, sentence) · ('pause', seconds) · ('para',)."""
    events, voice, buffer = [], None, []

    def flush():
        if buffer:
            for s in split_sentences(" ".join(buffer)):
                events.append(("say", voice, s))
            events.append(("para",))
            buffer.clear()

    for raw in text.splitlines():
        line = raw.strip()
        tag = re.fullmatch(r"\[(pause|voice|narrator)\s*([^\]]*)\]", line, flags=re.IGNORECASE)
        if tag:
            flush()
            kind, arg = tag.group(1).lower(), tag.group(2).strip()
            if kind == "pause":
                events.append(("pause", float(arg.rstrip("s") or 1)))
            elif kind == "voice":
                voice = arg or None
            else:
                voice = None
        elif not line or line == "---":
            flush()
        elif line.startswith("#"):
            flush()
            buffer.append(line.lstrip("#").strip() + ".")
            flush()
        else:
            cleaned = clean_inline(line)
            if cleaned:
                buffer.append(cleaned)
    flush()
    return events


# ─── Rendering ────────────────────────────────────────────────────────────────

def voice_config(settings, name):
    base = {"voice": settings["voice"], "speaker": settings["speaker"], "speed": settings["speed"]}
    if name is None:
        return base
    extra = settings["voices"].get(name)
    if extra is None:
        raise SystemExit(f"Voice '{name}' is used in a script but not defined in podcast.voices")
    if isinstance(extra, str):
        extra = {"voice": extra}
    return {**base, **extra}

def render_events(project_dir, events, settings):
    pieces = []
    for ev in events:
        if ev[0] == "say":
            pieces.append(synthesize(project_dir, ev[2], voice_config(settings, ev[1])))
            pieces.append(silence(settings["sentence_pause"]))
        elif ev[0] == "pause":
            pieces.append(silence(ev[1]))
        else:
            pieces.append(silence(settings["paragraph_pause"]))
    return np.concatenate(pieces) if pieces else silence(0)

def write_wav(path, audio):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(audio.tobytes())

def encode_mp3(project_dir, wav_path, mp3_path, settings, meta):
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg not found — install it (apt install ffmpeg / brew install ffmpeg)")
    inputs, labels = [], []
    for key in ("intro_music", "outro_music"):
        if settings.get(key) and not (Path(project_dir) / settings[key]).exists():
            raise SystemExit(f"{key} not found: {settings[key]}")
    order = [settings.get("intro_music"), str(wav_path), settings.get("outro_music")]
    for src in order:
        if src:
            src_path = src if src == str(wav_path) else str(Path(project_dir) / src)
            inputs += ["-i", src_path]
    n = len(inputs) // 2
    filters = "".join(f"[{i}:a]aresample=44100,aformat=channel_layouts=mono[a{i}];" for i in range(n))
    filters += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[out]"
    tags = []
    for k, v in meta.items():
        if v:
            tags += ["-metadata", f"{k}={v}"]
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", filters,
         "-map", "[out]", "-codec:a", "libmp3lame", "-b:a", settings["bitrate"], *tags, str(mp3_path)],
        check=True,
    )

def episode_scripts(project_dir, names):
    scripts_dir = Path(project_dir) / "podcast" / "scripts"
    if names:
        return [Path(n) if Path(n).exists() else scripts_dir / n for n in names]
    return sorted(scripts_dir.glob("*.md"))

def build(project_dir, names):
    project_dir = Path(project_dir)
    config = load_config(project_dir)
    settings = podcast_settings(config)
    scripts = episode_scripts(project_dir, names)
    if not scripts:
        raise SystemExit("No scripts found in podcast/scripts/ — run /ghost-writer:podcast first")
    out_dir = project_dir / "podcast" / "episodes"
    out_dir.mkdir(parents=True, exist_ok=True)

    for script in scripts:
        meta, body = split_frontmatter(script.read_text(encoding="utf-8"))
        events = parse_script(body)
        audio = render_events(project_dir, events, settings)
        wav_path = out_dir / f"{script.stem}.wav"
        mp3_path = out_dir / f"{script.stem}.mp3"
        write_wav(wav_path, audio)
        encode_mp3(project_dir, wav_path, mp3_path, settings, {
            "title": meta.get("title", script.stem),
            "album": config.get("title", ""),
            "artist": author_name(config),
            "track": meta.get("episode", ""),
            "language": config.get("language", ""),
        })
        wav_path.unlink()
        minutes = audio.size / SAMPLE_RATE / 60
        print(f"✅ {mp3_path}  ({minutes:.1f} min)")


# ─── Sample ───────────────────────────────────────────────────────────────────

def sample(project_dir, voice_ids, text=None):
    project_dir = Path(project_dir)
    config = load_config(project_dir)
    settings = podcast_settings(config)
    if not text:
        text = f"{config.get('title', 'Ghost Writer')}. {config.get('subtitle', '')}".strip()
    out_dir = project_dir / "podcast" / "samples"
    out_dir.mkdir(parents=True, exist_ok=True)
    for voice_id in voice_ids:
        voice_id, _, speaker = voice_id.partition(":")
        cfg = {**settings, "voice": voice_id, "speaker": int(speaker) if speaker else None, "voices": {}}
        audio = render_events(project_dir, parse_script(text), cfg)
        name = voice_id + (f"-{speaker}" if speaker else "")
        wav_path = out_dir / f"{name}.wav"
        write_wav(wav_path, audio)
        encode_mp3(project_dir, wav_path, out_dir / f"{name}.mp3", {**cfg, "intro_music": None, "outro_music": None}, {})
        wav_path.unlink()
        print(f"🎧 {out_dir / (name + '.mp3')}")


# ─── RSS feed ─────────────────────────────────────────────────────────────────

def feed(project_dir):
    project_dir = Path(project_dir)
    config = load_config(project_dir)
    settings = podcast_settings(config)
    base = settings["base_url"].rstrip("/")
    if not base:
        print("⚠️  podcast.base_url is empty — enclosure URLs will be relative. Set it before publishing.")
    episodes_dir = project_dir / "podcast" / "episodes"
    title = escape(config.get("title", "Podcast"))
    author = escape(author_name(config))
    items = []
    for script in episode_scripts(project_dir, []):
        mp3 = episodes_dir / f"{script.stem}.mp3"
        if not mp3.exists():
            continue
        meta, _ = split_frontmatter(script.read_text(encoding="utf-8"))
        date = datetime.fromtimestamp(mp3.stat().st_mtime, tz=timezone.utc)
        url = f"{base}/{mp3.name}" if base else mp3.name
        items.append(f"""    <item>
      <title>{escape(meta.get('title', script.stem))}</title>
      <description>{escape(meta.get('description', ''))}</description>
      <enclosure url="{escape(url)}" length="{mp3.stat().st_size}" type="audio/mpeg"/>
      <guid isPermaLink="false">{escape(script.stem)}</guid>
      <pubDate>{format_datetime(date)}</pubDate>
      <itunes:episode>{escape(meta.get('episode', ''))}</itunes:episode>
    </item>""")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>{title}</title>
    <description>{escape(config.get('subtitle', '') or config.get('title', ''))}</description>
    <language>{escape(config.get('language', 'en'))}</language>
    <itunes:author>{author}</itunes:author>
    <link>{escape(base)}</link>
{chr(10).join(items)}
  </channel>
</rss>
"""
    out = project_dir / "podcast" / "feed.xml"
    out.write_text(xml, encoding="utf-8")
    print(f"✅ {out} ({len(items)} episodes)")


if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = args[0] if args else "build"
    rest = args[1:]
    if cmd == "voices":
        list_voices(rest[0] if rest else (load_config(".").get("language") or "en")[:2])
    elif cmd == "sample":
        text = None
        if "--text" in rest:
            i = rest.index("--text")
            text, rest = rest[i + 1], rest[:i] + rest[i + 2:]
        sample(".", rest or [podcast_settings(load_config("."))["voice"]], text)
    elif cmd == "build":
        build(".", rest)
    elif cmd == "feed":
        feed(".")
    else:
        print(__doc__)
