# Build your podcast

Guida pratica: dal libro scritto con Ghost Writer a un podcast narrato, pubblicato su Spotify, Apple Podcasts, YouTube Music, Amazon Music e le altre app.

**Costo: zero.** Voce sintetica offline ([Piper](https://github.com/OHF-Voice/piper1-gpl)), audio con ffmpeg, hosting gratuito (GitHub Pages). Nessuna API key, nessun servizio a pagamento.

---

## Il percorso in breve

| # | Fase | Comando | Tempo indicativo |
|---|---|---|---|
| 0 | Prerequisiti | `pip install piper-tts numpy` + ffmpeg | 5 min |
| 1 | Voce del narratore | `/ghost-writer:podcast voice` | 10 min |
| 2 | Jingle (opzionale) | `/ghost-writer:podcast jingle` | 5–15 min |
| 3 | Piano episodi | `/ghost-writer:podcast` | 2 min |
| 4 | Script per l'ascolto | `/ghost-writer:podcast script [capitolo]` | 5 min a episodio |
| 5 | Audio MP3 | `/ghost-writer:podcast build` | pochi minuti |
| 6 | Hosting + feed RSS | `/ghost-writer:site` + `/ghost-writer:podcast feed` | 15 min |
| 7 | Pubblicazione sulle piattaforme | (manuale, una volta sola) | 30 min |

`/ghost-writer:podcast` lancia l'intero flusso e riprende da dove ti eri fermato.

---

## 0. Prima di iniziare

**Il libro deve essere finito.** Il podcast parte da `manuscript/[titolo]-final.md` (generato da `/ghost-writer:manuscript-final`) oppure dai capitoli in `chapters/`. Se un capitolo è ancora `draft`, il plugin ti avvisa: conviene completare prima `demolish` → `integrate`.

Installa le dipendenze:

```bash
pip install piper-tts numpy
# ffmpeg
sudo apt install ffmpeg      # Linux
brew install ffmpeg          # macOS
winget install ffmpeg        # Windows
```

Al primo avvio il plugin genera `export_podcast.py` nella root del progetto e verifica tutto da solo. I tuoi capitoli **non vengono mai modificati**: gli script vivono in `podcast/scripts/`.

---

## 1. Scegli la voce

```
/ghost-writer:podcast voice
```

1. Il plugin elenca le voci Piper per la lingua del libro e ne consiglia 2–3 (per l'italiano: `it_IT-paola-medium`).
2. Genera un **campione con un passaggio vero del tuo libro** in `podcast/samples/`. Ascoltali e scegli.
3. Regola insieme al plugin:
   - **Velocità** (`speed`): `0.9` narrativa, `1.0` naturale, `1.1` manualistica.
   - **Pause** (`sentence_pause`, `paragraph_pause`): più lunghe = tono più letterario.

**Voci dei personaggi** (romanzi, favole, biografie): puoi dare una voce diversa ai personaggi principali. Di default il narratore legge tutto, come un audiolibro classico.

> **Licenze:** ogni voce Piper ha un proprio model card con la licenza del dataset. Se intendi monetizzare il podcast, controlla che la voce scelta ne consenta l'uso commerciale.

---

## 2. Jingle d'apertura (opzionale)

```
/ghost-writer:podcast jingle
```

Tre opzioni:

- **A. Jingle composto offline** (consigliato): sting originale di 6–9 secondi, nessun problema di diritti. Lo stile segue il genere (`warm`, `upbeat`, `mysterious`, `playful`, `grime`). Chiedi "un altro" per una nuova variazione.
- **B. Musica AI locale** con ACE-Step (open source, serve GPU ~8 GB o Mac Apple Silicon). Il plugin ti scrive il prompt.
- **C. Un tuo file** o musica CC0 (es. Freesound con filtro CC0).

La voce entra sulla coda del jingle (`intro_overlap`, default 1.5 s).

---

## 3. Piano degli episodi

Il plugin propone **un episodio per capitolo**: unisce i capitoli sotto ~800 parole e divide quelli oltre ~6.000 (~40 minuti) a un cambio di scena.

```
PODCAST PLAN — [titolo]
  Ep 1  Introduzione         ~1.900 parole · ~13 min
  Ep 2  Cap. 1 — [titolo]    ~3.400 parole · ~23 min
```

Confermi, e il piano finisce in `podcast/plan.md` con lo stato di ogni episodio (`todo` → `script` → `approved` → `rendered`).

---

## 4. Script scritti per l'orecchio

```
/ghost-writer:podcast script 1
```

Il testo resta il tuo: frasi, ritmo e lessico non cambiano. Si adatta solo ciò che non funziona all'ascolto:

- elenchi e tabelle → frasi parlate;
- "vedi sopra", "nella figura" → riscritti o eliminati;
- numeri, date, sigle → scritti per esteso ("€1.500" → "millecinquecento euro");
- frasi oltre ~45 parole → spezzate in un punto naturale;
- pause `[pause 1]` ai cambi di scena.

Ogni episodio ha un'apertura (titolo del libro, numero episodio, richiamo al precedente) e una chiusura che anticipa il successivo senza spoiler.

**Approvi tu ogni script.** Ti viene mostrato l'elenco compatto delle modifiche (es. `3.4 elenco → frase`). Nulla va in audio senza approvazione.

---

## 5. Genera l'audio

```
/ghost-writer:podcast build              # tutti gli episodi approvati
/ghost-writer:podcast build episode-02   # un solo episodio
```

Output: `podcast/episodes/episode-NN.mp3`, mono 96 kbps (lo standard per il parlato), con tag ID3. Un episodio da 40 minuti pesa circa 29 MB.

**Ascolta i primi 2 minuti dell'episodio 1** prima di pubblicare. Se una parola è pronunciata male, segnalala: il plugin corregge la grafia nello script, rigenera solo quell'episodio e salva la correzione in `podcast/plan.md` (sezione `## Pronunciation`) per gli episodi successivi.

---

## 6. Hosting e feed RSS

Le piattaforme non ospitano i tuoi file: leggono un **feed RSS** che punta agli MP3 pubblicati online. Servono quindi due cose: un posto pubblico per gli MP3 e il file `feed.xml`.

### Opzione consigliata: sito del libro su GitHub Pages

```
/ghost-writer:site
```

1. Il plugin crea il sito in `docs/` con una sezione podcast (player, episodi, link al feed).
2. Su GitHub: **Settings → Pages → Deploy from a branch → `main` / `docs`**.
3. Imposta in `book.config.json`:
   ```json
   "podcast": { "base_url": "https://<utente>.github.io/<repository>/episodes" }
   ```
4. Genera il feed e ricostruisci il sito:
   ```
   /ghost-writer:podcast feed
   python3 build_site.py
   ```
5. Commit e push di `docs/`.

L'URL del feed da dare alle piattaforme sarà:

```
https://<utente>.github.io/<repository>/feed.xml
```

> Limiti GitHub Pages: 100 MB per file, ~1 GB per sito. Bastano per un libro intero a 96 kbps (~30 ore di audio).

**Alternative gratuite:** GitHub Releases, Internet Archive (archive.org), il tuo sito.

### Checklist prima di pubblicare il feed

- [ ] **Copertina** quadrata, JPG o PNG RGB, **3000×3000 px** (minimo 1400×1400). Richiesta da Apple e Spotify.
- [ ] **Email del proprietario** nel feed (`itunes:owner` / `itunes:email`): Spotify e altre piattaforme ti mandano lì il codice di verifica.
- [ ] **Categoria** (`itunes:category`), **lingua** e flag `itunes:explicit` presenti.
- [ ] Gli URL degli MP3 si aprono nel browser.
- [ ] Feed validato con un validatore gratuito (es. [Podbase](https://podba.se/validate/) o [Cast Feed Validator](https://www.castfeedvalidator.com/)).
- [ ] Nella descrizione del podcast è indicato che la narrazione usa una **voce sintetica** (buona pratica e, su alcune piattaforme, richiesto per i contenuti generati con AI).

Se manca qualcosa, chiedi al plugin di aggiungerlo: `/ghost-writer:podcast feed`.

---

## 7. Pubblica sulle piattaforme

Lo fai **una volta sola**: da quel momento ogni nuovo episodio aggiunto al feed compare automaticamente ovunque.

| Piattaforma | Dove | Cosa fare | Tempi |
|---|---|---|---|
| **Spotify** | [creators.spotify.com](https://creators.spotify.com) | Accedi → *Ho già un podcast* → incolla l'URL del feed → inserisci il codice ricevuto via email | minuti–poche ore |
| **Apple Podcasts** | [podcastsconnect.apple.com](https://podcastsconnect.apple.com) | Accedi con Apple ID → **+** → *Aggiungi uno show* → *Usa un feed RSS* → incolla l'URL → invia per la revisione | 1–5 giorni |
| **YouTube / YouTube Music** | [studio.youtube.com](https://studio.youtube.com) | *Crea* → *Nuovo podcast* → *Invia feed RSS* → incolla l'URL e conferma i diritti | ore–qualche giorno |
| **Amazon Music / Audible** | [podcasters.amazon.com](https://podcasters.amazon.com) | Accedi → *Add your podcast* → incolla l'URL → verifica via email | 1–2 giorni |
| **Deezer** | [podcasters.deezer.com](https://podcasters.deezer.com) | Registrati → *Add podcast* → incolla l'URL | 1–3 giorni |
| **Podcast Index** | [podcastindex.org/add](https://podcastindex.org/add) | Incolla l'URL (alimenta Podcast Addict, Fountain, Podverse e molte altre app) | minuti |

**Senza fare nulla:** Overcast, Pocket Casts, Castro e Castbox leggono il catalogo Apple e Podcast Index, quindi il podcast compare lì poco dopo l'approvazione.

### Ordine consigliato

1. **Apple Podcasts** per primo: la revisione è la più lenta e molte app attingono al suo catalogo.
2. **Spotify**, subito dopo.
3. **YouTube**, **Amazon**, **Podcast Index**, **Deezer** nello stesso giorno.

---

## 8. Dopo il lancio

**Nuovo episodio** (es. pubblicazione a puntate):

```
/ghost-writer:podcast script 5
/ghost-writer:podcast build episode-05
/ghost-writer:podcast feed
python3 build_site.py
git add docs podcast && git commit -m "Episode 5" && git push
```

Le piattaforme rileggono il feed da sole (di solito entro qualche ora).

**Correggere un episodio già pubblicato:** rigenera l'MP3 con lo stesso nome file e fai push. Evita di rinominare file o cambiare gli URL: le app li usano come identificativi.

**Statistiche:** ogni piattaforma ha la sua dashboard (Spotify for Creators, Apple Podcasts Connect, YouTube Studio, Amazon).

**Promozione:** il sito del libro (`/ghost-writer:site`) mostra già player ed episodi. Per farlo conoscere alla community, pubblica il libro nella galleria con `/ghost-writer:gallery`.

---

## Problemi frequenti

| Problema | Soluzione |
|---|---|
| `ModuleNotFoundError: piper` | `pip install piper-tts numpy` |
| `ffmpeg: command not found` | Installa ffmpeg (vedi fase 0) |
| Una parola suona male | Segnalala al plugin: corregge lo script e rigenera solo quell'episodio |
| Spotify non manda il codice | Verifica che l'email sia nel feed (`itunes:email`) e controlla lo spam |
| Apple rifiuta il feed | Quasi sempre la copertina: deve essere quadrata, 1400–3000 px, RGB, JPG/PNG |
| Il nuovo episodio non compare | Controlla che `feed.xml` sia aggiornato online; attendi qualche ora |
| La piattaforma non riproduce l'MP3 | Apri l'URL dell'MP3 nel browser: deve partire il download o la riproduzione |

---

## Riepilogo comandi

```
/ghost-writer:podcast                  # flusso completo, con ripresa
/ghost-writer:podcast voice            # voce narratore e personaggi
/ghost-writer:podcast jingle           # jingle d'apertura
/ghost-writer:podcast script [cap]     # script di un episodio
/ghost-writer:podcast build [ep]       # audio MP3
/ghost-writer:podcast feed             # feed RSS
/ghost-writer:site                     # sito con player + hosting MP3
```
