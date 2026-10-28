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
  python3 export_podcast.py jingle [--style S] [--seconds N] [--seed N] [--drums synth|kit|none]
                                   [--bars N] [--bpm N] [--bed 0.4]  # --style grime-loop: seamless beat,
                                                   # real samples; --bed = instruments level
                                   [--bassline 0.5] [--bass-sound piano|organ]   # bass riff + its level
                                                   # compose an intro jingle (podcast/music/)

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
    "intro_overlap": 1.5,     # seconds the voice starts before the intro music ends
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

def audio_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())

def encode_mp3(project_dir, wav_path, mp3_path, settings, meta):
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg not found — install it (apt install ffmpeg / brew install ffmpeg)")
    music = {}
    for key in ("intro_music", "outro_music"):
        if settings.get(key):
            path = Path(project_dir) / settings[key]
            if not path.exists():
                raise SystemExit(f"{key} not found: {settings[key]}")
            music[key] = path

    inputs, filters, n = [], [], 0
    def add_input(path):
        nonlocal n
        inputs.extend(["-i", str(path)])
        filters.append(f"[{n}:a]aresample=44100,aformat=channel_layouts=mono[a{n}]")
        n += 1
        return f"[a{n - 1}]"

    voice = add_input(wav_path)
    if "intro_music" in music:
        intro = add_input(music["intro_music"])
        delay = max(audio_duration(music["intro_music"]) - float(settings["intro_overlap"]), 0)
        fade = float(settings["intro_overlap"]) + 0.5
        chain, label = filters[-1].rsplit("[", 1)
        filters[-1] = f"{chain},afade=t=out:st={max(delay - 0.5, 0):.2f}:d={fade:.2f}[{label}"
        filters.append(f"{voice}adelay={int(delay * 1000)}[vd]")
        filters.append(f"{intro}[vd]amix=inputs=2:duration=longest:normalize=0[iv]")
        voice = "[iv]"
    if "outro_music" in music:
        outro = add_input(music["outro_music"])
        filters.append(f"{voice}{outro}concat=n=2:v=0:a=1[out]")
    else:
        filters.append(f"{voice}anull[out]")

    tags = []
    for k, v in meta.items():
        if v:
            tags += ["-metadata", f"{k}={v}"]
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters),
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


# ─── Jingle ───────────────────────────────────────────────────────────────────
# Composed from scratch with numpy: no samples, no licenses, same seed = same jingle.

JINGLE_STYLES = {
    #             scale    chords (scale degrees)  bpm  drums
    "warm":       ("major", [0, 5, 3, 4],          88,  False),
    "upbeat":     ("major", [0, 4, 5, 3],          116, True),
    "mysterious": ("minor", [0, 5, 2, 6],          70,  False),
    "playful":    ("major", [0, 3, 4, 0],          128, True),
}
PRESET_STYLES = {
    "essay": "warm", "manual": "upbeat", "fiction": "mysterious",
    "biography": "warm", "fable": "playful", "childrens-book": "playful",
}
SCALES = {"major": [0, 2, 4, 5, 7, 9, 11], "minor": [0, 2, 3, 5, 7, 8, 10]}
JINGLE_RATE = 44100

def midi_hz(note):
    return 440.0 * 2 ** ((note - 69) / 12)

def envelope(n, attack, release):
    env = np.ones(n)
    a, r = min(int(attack * JINGLE_RATE), n), min(int(release * JINGLE_RATE), n)
    if a:
        env[:a] = np.linspace(0, 1, a)
    if r:
        env[-r:] *= np.linspace(1, 0, r)
    return env

def pad_tone(freq, n):
    t = np.arange(n) / JINGLE_RATE
    tone = sum(np.sin(2 * np.pi * freq * k * d * t) / k ** 1.5 for k in range(1, 6) for d in (0.997, 1.003))
    return tone * envelope(n, 0.25, 0.6)

def bell_tone(freq, n):
    t = np.arange(n) / JINGLE_RATE
    tone = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-t * 9)
    return tone * np.exp(-t * 3.5) * envelope(n, 0.004, 0.05)

def kick(n):
    t = np.arange(n) / JINGLE_RATE
    return np.sin(2 * np.pi * (45 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 12)

def hat(n, rng):
    t = np.arange(n) / JINGLE_RATE
    noise = rng.standard_normal(n)
    noise = np.diff(noise, prepend=0)   # crude high-pass
    return noise * np.exp(-t * 60) * 0.15

def reverb(x):
    out = x.copy()
    for delay, gain in ((0.031, 0.35), (0.047, 0.3), (0.071, 0.25), (0.113, 0.2), (0.167, 0.15)):
        d = int(delay * JINGLE_RATE)
        y = np.zeros_like(x)
        for k in range(1, 5):
            if d * k < x.size:
                y[d * k:] += x[:-d * k] * gain ** k
        out += y
    return out

def place(track, sound, start):
    s = int(start * JINGLE_RATE)
    end = min(s + sound.size, track.size)
    if s < end:
        track[s:end] += sound[:end - s]

def compose_jingle(style="warm", seconds=7.0, seed=0):
    scale_name, progression, bpm, drums = JINGLE_STYLES[style]
    rng = np.random.default_rng(seed)
    scale = SCALES[scale_name]
    root = 57 + int(rng.integers(0, 7))          # A3..D#4
    beat = 60.0 / bpm
    tail = 2.5
    chord_len = max((seconds - tail) / len(progression), beat * 2)
    total = int((chord_len * len(progression) + tail) * JINGLE_RATE)

    def degree_note(deg, octave=0):
        return root + scale[deg % 7] + 12 * (deg // 7 + octave)

    pad, bass, bells, perc = (np.zeros(total) for _ in range(4))
    contour = rng.permutation([0, 1, 2, 1, 2, 0, 2, 1])
    for i, deg in enumerate(progression):
        start = i * chord_len
        last = i == len(progression) - 1
        length = chord_len + (tail if last else 0.3)
        n = int(length * JINGLE_RATE)
        chord = [degree_note(deg), degree_note(deg + 2), degree_note(deg + 4)]
        for note in chord:
            place(pad, pad_tone(midi_hz(note), n), start)
        place(bass, np.sin(2 * np.pi * midi_hz(chord[0] - 12) * np.arange(n) / JINGLE_RATE) * envelope(n, 0.02, 0.4), start)
        steps = 1 if last else int(chord_len / (beat / 2))
        for s in range(steps):
            note = chord[contour[(i * 3 + s) % len(contour)]] + 12
            if last:
                note = degree_note(0, 2)
            place(bells, bell_tone(midi_hz(note), int(1.5 * JINGLE_RATE)), start + s * beat / 2)
        if drums and not last:
            for b in range(int(chord_len / beat)):
                place(perc, kick(int(0.4 * JINGLE_RATE)), start + b * beat)
                place(perc, hat(int(0.1 * JINGLE_RATE), rng), start + b * beat + beat / 2)

    mix = 0.18 * pad + 0.35 * bass + 0.30 * bells + 0.5 * perc
    mix = reverb(mix)
    mix *= envelope(total, 0.05, tail)
    mix = mix / (np.max(np.abs(mix)) or 1) * 0.7
    return (mix * 32767).astype(np.int16)

def whistle_tone(freq, n, glide_from=None, vibrato_depth=0.012, glide=0.09):
    """Whistle: sine with delayed vibrato and an optional slide into the note."""
    t = np.arange(n) / JINGLE_RATE
    f = np.full(n, freq)
    if glide_from:
        g = min(int(glide * JINGLE_RATE), n)
        f[:g] = np.linspace(glide_from, freq, g)
    vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * 5.5 * t) * np.clip(t / 0.4, 0, 1)
    phase = 2 * np.pi * np.cumsum(f * vibrato) / JINGLE_RATE
    tone = np.sin(phase) + 0.08 * np.sin(2 * phase)
    return tone * envelope(n, 0.06, min(0.25, n / JINGLE_RATE / 2))

def square_bass(freq, n):
    """Eskibeat-style square sub with a short downward pitch drop."""
    t = np.arange(n) / JINGLE_RATE
    f = freq * (1 + 0.5 * np.exp(-t * 40))
    phase = 2 * np.pi * np.cumsum(f) / JINGLE_RATE
    square = np.sign(np.sin(phase)) * 0.45 + np.sin(phase) * 0.55
    return square * np.exp(-t * 4.5) * envelope(n, 0.003, 0.03)

def snare(n, rng):
    t = np.arange(n) / JINGLE_RATE
    body = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 25)
    noise = np.diff(rng.standard_normal(n), prepend=0) * np.exp(-t * 18) * 0.35
    return body * 0.6 + noise

def echo(x, delay, feedback, repeats=5):
    out = x.copy()
    d = int(delay * JINGLE_RATE)
    for k in range(1, repeats + 1):
        if d * k < x.size:
            out[d * k:] += x[:-d * k] * feedback ** k
    return out

def load_sample(path):
    """Decode any audio file to mono float at JINGLE_RATE via ffmpeg."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", str(JINGLE_RATE), "-"],
        check=True, capture_output=True,
    ).stdout
    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
    return audio / (np.max(np.abs(audio)) or 1)

def load_kit(kit_dir):
    """Real drum samples: kick.*, snare.*, hat.* in kit_dir. Missing ones fall back to synth."""
    kit = {}
    for name in ("kick", "snare", "hat"):
        found = sorted(Path(kit_dir).glob(f"{name}.*"))
        if found:
            kit[name] = load_sample(found[0])
    return kit

def compose_grime(seconds=7.0, seed=0, drum_mode="synth", kit_dir=None):
    """140 bpm grime beat under a sci-fi whistle lead (half-time snare, square bass, hat rolls).
    drum_mode: "synth", "kit" (samples from kit_dir) or "none"."""
    rng = np.random.default_rng(seed)
    kit = load_kit(kit_dir) if drum_mode == "kit" and kit_dir else {}
    if drum_mode == "kit" and not kit:
        raise SystemExit(f"No drum samples found in {kit_dir} — add kick.wav, snare.wav, hat.wav")

    def hit(name, seconds_long, gain=1.0):
        if drum_mode == "none":
            return np.zeros(1)
        if name in kit:
            return kit[name][:int(seconds_long * 2 * JINGLE_RATE)] * gain * (0.5 if name == "hat" else 1)
        n = int(seconds_long * JINGLE_RATE)
        return {"kick": lambda: kick(n), "snare": lambda: snare(n, rng), "hat": lambda: hat(n, rng)}[name]() * gain
    root = 40 + int(rng.integers(0, 4))           # E2..G2
    beat = 60.0 / 140
    bar = beat * 4
    s16 = beat / 4
    bars = max(3, int(round((seconds - 2) / bar)))
    tail = 2.2
    total = int((bars * bar + tail) * JINGLE_RATE)
    phrygian = [0, 1, 3, 5, 7, 8, 10]

    def note(deg, octave):
        return root + phrygian[deg % 7] + 12 * (deg // 7 + octave)

    lead, pad, bass, drums = (np.zeros(total) for _ in range(4))

    # Lead: two original motifs, (degree, length in 16ths); slides between notes
    motifs = [
        [(4, 4), (7, 10), (9, 2), (8, 4), (7, 8), (5, 4), (8, 8), (7, 8), (1, 12)],
        [(7, 6), (4, 2), (8, 8), (7, 4), (9, 4), (8, 12), (5, 4), (8, 4), (7, 16)],
    ]
    pos, prev = 0.0, None
    for deg, length in motifs[int(rng.integers(0, len(motifs)))]:
        if pos >= bars * bar:
            break
        freq = midi_hz(note(deg, 2))
        n = int(length * s16 * JINGLE_RATE)
        place(lead, whistle_tone(freq, n, prev), pos)
        pos, prev = pos + length * s16, freq
    lead = echo(lead, beat * 0.75, 0.38)

    # Pad: dark i - bII - i - bVII voicing, one chord per bar
    progression = [0, 1, 0, 6]
    for b in range(bars):
        deg = progression[b % 4]
        n = int((bar + (tail if b == bars - 1 else 0.1)) * JINGLE_RATE)
        for d in (deg, deg + 2, deg + 4):
            place(pad, pad_tone(midi_hz(note(d, 1)), n), b * bar)

    # Beat drops after the first bar
    bass_patterns = [[0, 3, 6, 10, 11], [0, 3, 7, 10, 14], [0, 2, 6, 8, 11, 14]]
    bass_pattern = bass_patterns[int(rng.integers(0, len(bass_patterns)))]
    for b in range(1, bars):
        start = b * bar
        deg = progression[b % 4]
        for step in bass_pattern:
            place(bass, square_bass(midi_hz(note(deg, 0)), int(s16 * 2.5 * JINGLE_RATE)), start + step * s16)
        for step in (0, 10):
            place(drums, hit("kick", 0.35), start + step * s16)
        place(drums, hit("snare", 0.3), start + 8 * s16)
        roll = b % 2 == 0 or b == bars - 1
        for step in range(0, 16, 2):
            if roll and step >= 12:
                for k in range(3):                 # triplet hat roll
                    place(drums, hit("hat", 0.06), start + (step + k * 2 / 3) * s16)
            else:
                place(drums, hit("hat", 0.08), start + step * s16)
    # Final hit on the downbeat after the last bar
    place(drums, hit("kick", 0.5), bars * bar)
    place(drums, hit("snare", 0.4, 0.7), bars * bar)
    place(bass, square_bass(midi_hz(note(0, 0)), int(1.2 * JINGLE_RATE)), bars * bar)

    mix = 0.30 * lead + 0.07 * reverb(pad) + 0.40 * bass + 0.55 * drums
    mix *= envelope(total, 0.02, tail * 0.8)
    mix = np.tanh(mix / (np.max(np.abs(mix)) or 1) * 1.6)   # light saturation
    mix = mix / (np.max(np.abs(mix)) or 1) * 0.75
    return (mix * 32767).astype(np.int16)

# ─── Grime loop (real recorded samples) ───────────────────────────────────────
# Everything except the whistle lead is a real recording from the Versilian
# Community Sample Library (VCSL, CC0 — https://github.com/sgossner/VCSL),
# downloaded on first use into podcast/music/kit/vcsl/. The loop is seamless:
# reverb and echo tails wrap around to the start, so it can play on repeat.

VCSL_BASE = "https://raw.githubusercontent.com/sgossner/VCSL/master/"
VCSL_KIT = {
    "kick":   "Membranophones/Struck Membranophones/Bass Drum 1/BDrumNew_hit_v7_rr1_Sum.wav",
    "snare":  "Membranophones/Struck Membranophones/Snare Drum, Modern 1/Snare2_HitSN_v7_rr1_Mid.wav",
    "clap":   "Idiophones/Struck Idiophones/Claps/Clap_rr2.wav",
    "hat":    "Idiophones/Struck Idiophones/Hi-Hat Cymbal/HiHat_HitC_v2_rr1_Mid.wav",
    "openhat": "Idiophones/Struck Idiophones/Hi-Hat Cymbal/HiHat_HitO_rr1_Mid.wav",
    "crash":  "Idiophones/Struck Idiophones/Suspended Cymbal 1/susCymb1_hit_f1.wav",
    "ratchet": "Idiophones/Struck Idiophones/Ratchet/Ratchet1_Crank_rr1_Mid.wav",
}
PIANO_NOTES = ["C", "D", "E", "F#", "G#", "A#"]   # Steinway B is sampled every whole tone
NOTE_PC = {"C": 0, "D": 2, "E": 4, "F#": 6, "G#": 8, "A#": 10}

_samples = {}

def vcsl_sample(project_dir, rel_path):
    from urllib.parse import quote
    if rel_path in _samples:
        return _samples[rel_path]
    local = Path(project_dir) / "podcast" / "music" / "kit" / "vcsl" / rel_path
    if not local.exists():
        local.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading {rel_path.split('/')[-1]} (VCSL, CC0)...")
        with urlopen(VCSL_BASE + quote(rel_path)) as r:
            local.write_bytes(r.read())
    _samples[rel_path] = load_sample(local)
    return _samples[rel_path]

def pitch_shift(audio, semitones):
    if semitones == 0:
        return audio
    ratio = 2 ** (semitones / 12)
    x = np.arange(0, audio.size - 1, ratio)
    return np.interp(x, np.arange(audio.size), audio)

def piano(project_dir, midi, sustain=True, velocity=3):
    """Real Steinway note: nearest sampled note, shifted by at most one semitone."""
    best = min(((n, o) for n in PIANO_NOTES for o in range(0, 8)),
               key=lambda no: abs((no[1] + 1) * 12 + NOTE_PC[no[0]] - midi))
    sampled = (best[1] + 1) * 12 + NOTE_PC[best[0]]
    kind = "Sus" if sustain else "NoSus"
    path = (f"Chordophones/Zithers/Grand Piano, Steinway B/{kind}/"
            f"JHPiano_{kind}_Close_{best[0]}{best[1]}_vl{velocity}_rr1.wav")
    return pitch_shift(vcsl_sample(project_dir, path), midi - sampled)

ORGAN_NOTES = {"C": 0, "D#": 3, "F#": 6, "A": 9}   # pipe organ pedal, sampled every minor third

def organ(project_dir, midi):
    """Real pipe-organ pedal note (VCSL), nearest sample shifted by at most one semitone."""
    best = min(((n, o) for n in ORGAN_NOTES for o in (1, 2, 3) if not (n == "A" and o == 3)),
               key=lambda no: abs((no[1] + 1) * 12 + ORGAN_NOTES[no[0]] - midi))
    sampled = (best[1] + 1) * 12 + ORGAN_NOTES[best[0]]
    path = f"Aerophones/Edge-blown Aerophones/Pipe Organ/Loud Pedal/Rode_Pedal_{best[0]}{best[1]}.wav"
    tone = vcsl_sample(project_dir, path)[int(0.3 * JINGLE_RATE):]   # skip the slow pipe attack
    tone = tone * envelope(tone.size, 0.008, 0.0)
    return pitch_shift(tone, midi - sampled)

# Bass riff, one entry per 16th-note hit: (step, scale degrees above the chord root, length in 16ths).
# Bars 1-3 groove on the chord; bar 4 walks down to the root of the next loop.
BASSLINE = [
    [(0, 0, 3), (3, 0, 1), (6, 7, 2), (8, 4, 2), (11, 2, 1), (12, 4, 2), (14, 7, 2)],
    [(0, 0, 3), (3, 0, 1), (6, 7, 2), (8, 4, 2), (11, 6, 1), (12, 4, 2), (14, 2, 2)],
    [(0, 0, 3), (3, 0, 1), (6, 7, 2), (8, 4, 2), (11, 2, 1), (12, 4, 2), (14, 7, 2)],
    [(0, 0, 3), (3, 0, 1), (6, 4, 2), (8, 4, 2), (10, 3, 2), (12, 2, 2), (14, 1, 2)],
]

def trim(audio, seconds, fade=0.04):
    n = min(int(seconds * JINGLE_RATE), audio.size)
    return audio[:n] * envelope(n, 0.0, fade)

def bitcrush(x, bits=8, hold=4):
    """Digital lo-fi: fewer amplitude steps and a sample-and-hold downsample."""
    peak = np.max(np.abs(x)) or 1
    levels = 2 ** (bits - 1)
    crushed = np.round(x / peak * levels) / levels * peak
    return np.repeat(crushed[::hold], hold)[:x.size]

def duck(x, key, depth=0.5, smooth=0.08):
    """Lower x while key (the whistle) is playing — keeps the lead on top."""
    k = int(smooth * JINGLE_RATE)
    env = np.convolve(np.abs(key), np.ones(k) / k, mode="same")
    env = env / (np.max(env) or 1)
    return x * (1 - depth * np.clip(env * 2, 0, 1))

def rms(x):
    return np.sqrt(np.mean(x ** 2)) or 1

def compose_grime_loop(project_dir, seed=0, bars=8, bpm=140, bed_level=1.0, bassline=0.0, bass_sound="piano"):
    """Seamless 140 bpm grime loop: the whistle lead on top of real drums, piano and FX."""
    rng = np.random.default_rng(seed)
    root = 40 + int(rng.integers(0, 4))           # same draws as compose_grime: same key and melody
    motif_index = int(rng.integers(0, 2))
    pattern_index = int(rng.integers(0, 3))
    beat = 60.0 / bpm
    bar = beat * 4
    s16 = beat / 4
    loop_len = int(bars * bar * JINGLE_RATE)
    total = loop_len + int(4 * JINGLE_RATE)       # room for tails, wrapped at the end
    dorian = [0, 2, 3, 5, 7, 9, 10]               # minor but not spooky: hip hop, not horror

    def note(deg, octave):
        return root + dorian[deg % 7] + 12 * (deg // 7 + octave)

    # User samples in podcast/music/kit/ (kick.*, snare.*, hat.*) override the VCSL ones
    user_kit = load_kit(Path(project_dir) / "podcast" / "music" / "kit")
    kit = {name: user_kit.get(name) if name in user_kit else vcsl_sample(project_dir, path)
           for name, path in VCSL_KIT.items()}
    kit["kick"] = trim(kit["kick"], 0.45, 0.15)
    kit["snare"] = trim(kit["snare"], 0.35, 0.12)
    kit["clap"] = trim(kit["clap"], 0.3, 0.1)
    kit["hat"] = trim(kit["hat"], 0.09, 0.04)
    kit["openhat"] = trim(kit["openhat"], 0.35, 0.15)
    kit["crash"] = trim(kit["crash"], 3.5, 1.5)
    kit["ratchet"] = trim(kit["ratchet"], 0.6, 0.1)

    lead, keys, bass, drums, fx, riff = (np.zeros(total) for _ in range(6))

    # Whistle lead (unchanged from the grime jingle), repeated every 4 bars: the mantra
    motifs = [
        [(4, 4), (7, 10), (9, 2), (8, 4), (7, 8), (5, 4), (8, 8), (7, 8), (1, 12)],
        [(7, 6), (4, 2), (8, 8), (7, 4), (9, 4), (8, 12), (5, 4), (8, 4), (7, 16)],
    ]
    for phrase_start in range(0, bars, 4):
        pos, prev = phrase_start * bar, None
        for deg, length in motifs[motif_index]:
            if pos >= min(phrase_start + 4, bars) * bar:
                break
            freq = midi_hz(note(deg, 2))
            n = int(length * s16 * JINGLE_RATE)
            place(lead, whistle_tone(freq, n, prev, vibrato_depth=0.003, glide=0.035), pos)
            pos, prev = pos + length * s16, freq
    # Digital delay: the echoes are bit-crushed, the dry whistle stays clean
    lead = lead + bitcrush(echo(lead, beat * 0.75, 0.38) - lead, bits=8, hold=2) * 0.75

    progression = [0, 3, 0, 6]                    # i - IV - i - bVII
    bass_patterns = [[0, 3, 6, 10, 11], [0, 3, 7, 10, 14], [0, 2, 6, 8, 11, 14]]
    for b in range(bars):
        start = b * bar
        deg = progression[b % 4]
        # Piano: 7th chord on the one, below the whistle's register
        chord = [note(deg, 1), note(deg + 2, 1), note(deg + 4, 1), note(deg + 6, 1)]
        for midi in chord:
            place(keys, trim(piano(project_dir, midi, velocity=2), bar, 0.2), start)
        if bassline:
            # Bass riff: replaces the fixed bass pattern, with its own level above the bed
            for step, rel, length in BASSLINE[b % 4]:
                midi = note(deg + rel, 0) - 12
                hit_len = s16 * length * 0.9
                if bass_sound == "organ":
                    tone = trim(organ(project_dir, midi), hit_len, 0.04)
                else:
                    low = trim(piano(project_dir, midi, sustain=False, velocity=4), hit_len, 0.04)
                    mid = trim(piano(project_dir, midi + 12, sustain=False, velocity=3), hit_len, 0.04)
                    tone = low + 0.5 * mid[:low.size]
                place(riff, tone, start + step * s16)
        # Piano bass: low octaves on the grime pattern
        for step in ([] if bassline else bass_patterns[pattern_index]):
            low = trim(piano(project_dir, note(deg, 0) - 12, sustain=False, velocity=4), s16 * 2.5, 0.05)
            mid = trim(piano(project_dir, note(deg, 0), sustain=False, velocity=4), s16 * 2.5, 0.05)
            place(bass, low + 0.6 * mid[:low.size] if mid.size >= low.size else low, start + step * s16)
        # Drums
        kicks = [0, 10] + ([14] if b % 4 == 3 else [])
        for step in kicks:
            place(drums, kit["kick"], start + step * s16)
        place(drums, kit["snare"] + 0.7 * np.pad(kit["clap"], (0, max(0, kit["snare"].size - kit["clap"].size)))[:kit["snare"].size],
              start + 8 * s16)
        for step in range(0, 16, 2):
            if b % 2 == 1 and step >= 12:
                for k in range(3):
                    place(drums, kit["hat"] * 0.8, start + (step + k * 2 / 3) * s16)
            elif b % 2 == 0 and step == 14:
                place(drums, kit["openhat"] * 0.6, start + step * s16)
            else:
                place(drums, kit["hat"] * (1.0 if step % 4 == 2 else 0.7), start + step * s16)

    # FX: light crash on the one, ratchet on the last bar
    place(fx, kit["crash"] * 0.3, 0)
    place(fx, kit["ratchet"] * 0.5, (bars - 1) * bar + 12 * s16)

    # Mix by loudness: whistle on top, everything else ducks under it
    bed = (0.55 * duck(drums, lead, 0.35) / rms(drums) + 0.20 * duck(keys, lead, 0.6) / rms(keys) +
           0.50 * duck(bass, lead, 0.3) / rms(bass) + 0.10 * fx / rms(fx))
    mix = 1.0 * lead / rms(lead) + bed_level * bed   # bed_level 0.4 ≈ instruments in the background
    if bassline:
        mix += bassline * duck(riff, lead, 0.25) / rms(riff)
    looped = mix[:loop_len].copy()
    tail = mix[loop_len:]
    looped[:tail.size] += tail[:loop_len]          # wrap tails: seamless on repeat
    looped = np.tanh(looped / (np.max(np.abs(looped)) or 1) * 1.2)
    looped = looped / (np.max(np.abs(looped)) or 1) * 0.85
    return (looped * 32767).astype(np.int16)


def jingle(project_dir, style=None, seconds=7.0, seed=None, drums="synth", bars=8, bpm=140, bed_level=1.0,
           bassline=0.0, bass_sound="piano"):
    project_dir = Path(project_dir)
    config = load_config(project_dir)
    style = style or PRESET_STYLES.get(config.get("preset", ""), "warm")
    extra = ("grime", "grime-loop")
    if style not in JINGLE_STYLES and style not in extra:
        raise SystemExit(f"Unknown style '{style}'. Available: {', '.join(list(JINGLE_STYLES) + list(extra))}")
    if seed is None:
        seed = sum(config.get("title", "").encode()) % 10000
    kit_dir = project_dir / "podcast" / "music" / "kit"
    if style == "grime-loop":
        audio = compose_grime_loop(project_dir, seed, bars, bpm, bed_level, bassline, bass_sound)
    elif style == "grime":
        audio = compose_grime(seconds, seed, drums, kit_dir)
    else:
        audio = compose_jingle(style, seconds, seed)
    out_dir = project_dir / "podcast" / "music"
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"-{drums}" if style == "grime" and drums != "synth" else ""
    if style == "grime-loop":
        suffix = (f"-{bpm}bpm" if bpm != 140 else "") + (f"-bed{bed_level:g}" if bed_level != 1.0 else "")
        if bassline:
            suffix += f"-bass-{bass_sound}{bassline:g}"
    out = out_dir / f"jingle-{style}-{seed}{suffix}.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(JINGLE_RATE)
        w.writeframes(audio.tobytes())
    print(f"🎵 {out}  ({audio.size / JINGLE_RATE:.1f} s, style={style}, seed={seed})")
    return out


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
    elif cmd == "jingle":
        opts = dict(zip(rest[::2], rest[1::2]))
        jingle(".", opts.get("--style"), float(opts.get("--seconds", 7)),
               int(opts["--seed"]) if "--seed" in opts else None, opts.get("--drums", "synth"),
               int(opts.get("--bars", 8)), int(opts.get("--bpm", 140)), float(opts.get("--bed", 1.0)),
               float(opts.get("--bassline", 0)), opts.get("--bass-sound", "piano"))
    else:
        print(__doc__)
