# Guida alle skill di Ghost Writer

Una voce per ogni skill: **cosa fa**, **quali file legge e scrive**, **quando usarla** ed **esempi**.

Legenda file:
- 📖 = letto · ✏️ = creato o modificato
- Quasi tutte le skill leggono `book.config.json → language` per rispondere nella lingua del libro: non viene ripetuto ogni volta.
- **Sync del grafo**: le skill marcate con 🔗 eseguono a fine lavoro la procedura *Sync* di `/ghost-writer:graph` se un capitolo diventa `status: complete` o cambia `version` (aggiornano `graph/` e, se esiste `site.yaml`, rigenerano `docs/index.html`).

## Indice

| Fase | Skill |
|---|---|
| Setup | [check](#check) · [wizard](#wizard) · [start](#start) · [setup-author](#setup-author) · [setup-book](#setup-book) · [setup-voice](#setup-voice) |
| Scrittura | [chapter](#chapter) · [ask-before-writing](#ask-before-writing) · [freeflow](#freeflow) · [write](#write) · [demolish](#demolish) · [demolish-persona](#demolish-persona) · [integrate](#integrate) |
| Revisione e qualità | [review](#review) · [consistency-check](#consistency-check) · [proofread](#proofread) · [revise](#revise) · [rules](#rules) · [corrections](#corrections) · [retune](#retune) · [character-interview](#character-interview) · [character-check](#character-check) · [graph](#graph) |
| Chiusura | [finish](#finish) · [write-opening](#write-opening) · [write-closing](#write-closing) · [manuscript-final](#manuscript-final) |
| Export | [export-pdf](#export-pdf) · [export-epub](#export-epub) · [export-docx](#export-docx) · [podcast](#podcast) |
| Pubblicazione | [site](#site) · [gallery](#gallery) |
| Stato e utilità | [session-start](#session-start) · [resume](#resume) · [status](#status) · [help](#help) · [longform-upgrade](#longform-upgrade) |

## Mappa rapida: file → chi lo scrive

| File | Scritto da |
|---|---|
| `book.config.json` | wizard, setup-author, setup-book, setup-voice, retune, longform-upgrade, podcast, gallery, site (`podcast.base_url`) |
| `outline.md` | wizard, setup-book, write, longform-upgrade |
| `chapters/*.md` | write, freeflow, integrate, retune, revise, proofread*, corrections, write-opening, write-closing, demolish / demolish-persona (Demolition Log) |
| `book-memory.md` | write, integrate, revise, corrections, consistency-check, character-interview, session-start (Session Log), write-closing, longform-upgrade |
| `memory/part-N.md` | longform-upgrade (poi write/revise in modalità longform) |
| `demolition-history.md` | demolish, demolish-persona |
| `voice-sample.md` | write, integrate (silenziosamente) |
| `style-rules.md` | rules, revise, corrections |
| `characters/*.md` | character-interview, character-check |
| `personas/*.md` | demolish-persona (persona custom) |
| `sessions/*.md` | start, chapter, review, finish |
| `project-state.md` | session-start |
| `corrections.md`, `manuscript/review-map.json` | corrections |
| `manuscript/*-final.{md,pdf,epub,docx}` | manuscript-final, export-* |
| `podcast/**` | podcast |
| `graph/**` | graph (Sync) |
| `site.yaml`, `docs/index.html` | site |

\* solo dopo conferma esplicita dell'autore.

---

## Setup

### check
**Cosa fa:** verifica in ~60 secondi che plugin e progetto siano installati correttamente. Genera una frase di prova nella voce dell'autore. Sola lettura.
**File:** 📖 `.claude-plugin/plugin.json`, `presets/*.md`, `book.config.json`, `outline.md`, `book-memory.md`, `demolition-history.md`, `site.yaml` (con `build_site.py --check`), `graph/` (con `graph.py validate`/`check`). ✏️ nessuno.
**Quando:** subito dopo l'installazione, o quando "qualcosa non va".
**Esempi:**
- Plugin appena installato → `/ghost-writer:check` per confermare che i preset sono leggibili.
- Il sito non si aggiorna → `/ghost-writer:check` segnala cover mancante o `podcast.base_url` vuoto.

### wizard
**Cosa fa:** setup conversazionale per chi non sa da dove iniziare. L'autore descrive l'idea a parole sue; il wizard deduce genere, voce, premessa e lettore senza mai parlare di preset o file.
**File:** ✏️ `book.config.json` (creato), `outline.md` (bozza con 3-5 capitoli).
**Quando:** progetto nuovo, autore non tecnico o con idea ancora vaga.
**Esempi:**
- "Voglio scrivere qualcosa sulla mia esperienza da agente di commercio, ma non so se è un saggio o una biografia" → `/ghost-writer:wizard`.
- Cliente che ti detta l'idea a voce in una call: incolli la trascrizione nel wizard.

### start
**Cosa fa:** macro di onboarding completo: setup-author → setup-book → setup-voice, con ripresa se interrotto.
**File:** ✏️ `sessions/start.md` (stato dell'onboarding) + tutto ciò che scrivono le tre skill di setup.
**Quando:** progetto nuovo, autore disposto a un onboarding strutturato (alternativa più rigorosa al wizard).
**Esempi:**
- Prima sessione di lavoro su un manuale tecnico → `/ghost-writer:start`.
- Interrotto dopo setup-book → rilanci `/ghost-writer:start` e riparte da setup-voice.

### setup-author
**Cosa fa:** intervista l'autore su background, competenze, visione del mondo e rapporto col lettore.
**File:** ✏️ `book.config.json → author_profile`.
**Quando:** primo passo dell'onboarding, o per rifare solo il profilo autore.
**Esempi:**
- L'autore ha cambiato ruolo professionale e vuole riflettere la nuova autorevolezza → `/ghost-writer:setup-author`.

### setup-book
**Cosa fa:** definisce il libro: tesi centrale, struttura, lettore target, scopo e **preset di genere** (essay, biography, fiction, fable, manual, childrens-book).
**File:** 📖 `presets/[preset].md`. ✏️ `book.config.json → preset`, `preset_digest`, `book_profile`; `outline.md` (prima bozza).
**Quando:** dopo setup-author; o per ripensare struttura/genere.
**Esempi:**
- Libro "come fare lead generation su LinkedIn" → preset `manual`.
- Raccolta di storie aziendali con morale → preset `fable`.

### setup-voice
**Cosa fa:** crea il *Voice Fingerprint* dell'autore da intervista + analisi di campioni di scrittura.
**File:** ✏️ `book.config.json → author_voice`.
**Quando:** dopo setup-book; da qui in poi il plugin può scrivere.
**Esempi:**
- Incolli 3 post LinkedIn e una newsletter dell'autore → `/ghost-writer:setup-voice`.

---

## Scrittura

### chapter
**Cosa fa:** macro del ciclo completo di un capitolo: ask-before-writing → write → demolish → integrate. Supporta la ripresa. 🔗
**File:** 📖 `book.config.json`, `book-memory.md`, `outline.md`. ✏️ `sessions/chapter-[NN]-[slug].md` + tutto ciò che scrivono le skill interne.
**Quando:** è il modo standard di scrivere un capitolo.
**Esempi:**
- "Scriviamo il capitolo 3" → `/ghost-writer:chapter`.
- Ti sei fermato dopo la bozza → `/ghost-writer:chapter` propone "Resume 3" dal passo *demolish*.

### ask-before-writing
**Cosa fa:** dialogo strutturato per chiarire cosa l'autore vuole dire, prima di scrivere. Le domande cambiano in base al genere.
**File:** 📖 `book.config.json`, `presets/[preset]-dialogue.md`, `book-memory.md` (termini definiti, promesse aperte, riassunti). ✏️ nessuno (il riepilogo confermato passa a write).
**Quando:** prima di ogni write, se non usi chapter.
**Esempi:**
- Hai solo il titolo del capitolo "Il funnel è morto" → `/ghost-writer:ask-before-writing` per estrarre la tesi.

### freeflow
**Cosa fa:** l'autore scarica tutto in modo disordinato (testo, note vocali trascritte); la skill estrae struttura, tesi e materiale usabile. Può produrre una bozza con sezioni `[FROM DUMP]`.
**File:** 📖 `book.config.json`. ✏️ `chapters/[NN]-[sezione].md` con `status: freeflow-draft` (solo se scegli di generare la bozza).
**Quando:** blocco dello scrittore, idee non organizzate.
**Esempi:**
- 10 minuti di vocale su WhatsApp trascritto → `/ghost-writer:freeflow`.
- Appunti sparsi da Notion su un capitolo → freeflow, poi demolish.

### write
**Cosa fa:** genera una sezione del libro dall'outline, nella voce dell'autore.
**File:** 📖 `book.config.json`, `outline.md`, `book-memory.md`, `voice-sample.md`, `style-rules.md`. ✏️ `chapters/[NN]-[slug].md`, `outline.md` (status → `draft`), `book-memory.md` (o `memory/part-N.md` in longform), `voice-sample.md` (silenzioso).
**Quando:** dopo ask-before-writing confermato.
**Esempi:**
- `/ghost-writer:write 04-pricing` dopo aver chiarito il contenuto del capitolo 4.

### demolish
**Cosa fa:** critica ostile della bozza: trova debolezze strutturali, falle logiche, concetti non definiti, contraddizioni. Un problema alla volta.
**File:** 📖 capitolo, `outline.md`, `demolition-history.md` (sezioni attive). ✏️ *Demolition Log* in fondo al capitolo, `demolition-history.md` (log, contatori, archiviazione capitoli completi).
**Quando:** quando esiste una bozza.
**Esempi:**
- `/ghost-writer:demolish chapters/02-attribution.md` prima di mandare il capitolo al cliente.

### demolish-persona
**Cosa fa:** demolizione dal punto di vista di un lettore specifico: `target-reader`, `hostile-reader`, `domain-expert`, `editor`, `out-of-target` o una persona custom.
**File:** 📖 `personas/[persona].md` (di default solo *Quick Summary*), `book.config.json → target_reader` / `book_profile`. ✏️ Demolition Log del capitolo, `demolition-history.md`, opzionale `personas/[nome].md` (persona custom).
**Quando:** dopo demolish, o per una prova mirata.
**Esempi:**
- Libro per CMO → `/ghost-writer:demolish-persona domain-expert chapters/05-mmm.md`.
- Persona custom "titolare di PMI non tecnico" salvata in `personas/` e riusata per ogni capitolo.

### integrate
**Cosa fa:** traduce le risposte dell'autore alla demolizione in modifiche precise al testo. Nulla cambia senza approvazione, una modifica alla volta. 🔗
**File:** 📖 `style-rules.md`, `book.config.json`. ✏️ capitolo (testo, `version`, eventuale `status: complete`, Demolition Log → `integrated`), `book-memory.md`, `voice-sample.md` (se ≥3 paragrafi riscritti).
**Quando:** subito dopo demolish / demolish-persona / review.
**Esempi:**
- Hai risposto a 6 obiezioni del demolish → `/ghost-writer:integrate` le applica una per una.
- "Questa è la versione finale" → integrate imposta `status: complete` e sincronizza il grafo.

---

## Revisione e qualità

### review
**Cosa fa:** macro: demolizione con tutte e 5 le persona in sequenza (editor → target-reader → hostile-reader → domain-expert → out-of-target), poi integrate. Supporta la ripresa. 🔗
**File:** 📖 capitolo, `demolition-history.md`. ✏️ `sessions/review-[slug].md` + quanto scrivono demolish-persona e integrate.
**Quando:** revisione profonda di un capitolo chiave.
**Esempi:**
- Capitolo d'apertura prima di presentarlo a un editore → `/ghost-writer:review chapters/01-intro.md`.

### consistency-check
**Cosa fa:** audit tra capitoli: deriva dei termini, tono incoerente, promesse non mantenute, affermazioni contraddette, esempi ripetuti. Produce una lista prioritizzata.
**File:** 📖 tutti i capitoli, `book-memory.md`, `demolition-history.md`, `graph/INDEX.md` e card (se esiste il grafo). ✏️ `book-memory.md` (solo quando risolvi una correzione).
**Quando:** ogni 3-4 capitoli.
**Esempi:**
- Al cap. 2 dici "customer journey", al cap. 6 "percorso cliente" → consistency-check lo segnala.

### proofread
**Cosa fa:** controllo grammatica e stile: errori, ripetizioni, ritmo, frasi vietate dal profilo voce.
**File:** 📖 `book.config.json → author_voice`, capitolo. ✏️ capitolo solo dopo conferma esplicita.
**Quando:** prima dell'integrate finale o della bozza definitiva.
**Esempi:**
- `/ghost-writer:proofread chapters/03-the-shift.md`.

### revise
**Cosa fa:** passata editoriale: grammatica, punteggiatura e regole di `style-rules.md`, timeline degli eventi, dettagli dei personaggi, continuità di oggetti/luoghi/date/numeri. Propone ogni fix, non applica senza conferma. 🔗
**File:** 📖 `style-rules.md`, `book-memory.md` / `memory/part-*.md`, `characters/*.md`, grafo. ✏️ capitolo, `book-memory.md` (Continuity Ledger), `style-rules.md` (convenzioni dedotte o nuove regole).
**Quando:** su un capitolo dopo integrate, o su tutto il libro prima di manuscript-final.
**Esempi:**
- `/ghost-writer:revise chapters/07-case-study.md`.
- `/ghost-writer:revise --all` prima dell'assemblaggio finale.

### rules
**Cosa fa:** gestisce le regole di scrittura del libro (punteggiatura e regole custom). Applicate da write, integrate e revise.
**File:** ✏️ `style-rules.md` (creato dal template se manca). 📖 `book.config.json → language` per i default.
**Quando:** quando hai una convenzione da imporre a tutto il libro.
**Esempi:**
- `/ghost-writer:rules add "sempre virgolette basse « » per i dialoghi"`.
- `/ghost-writer:rules infer` per dedurre le regole dai capitoli già scritti; `/ghost-writer:rules remove R3`.

### corrections
**Cosa fa:** raccoglie e applica le correzioni fatte rileggendo lontano dal PC: PDF di revisione con ID paragrafo (3.12 = cap. 3, par. 12), import di annotazioni PDF, note libere (vocali, foto di pagine stampate). 🔗
**File:** ✏️ `corrections.md`, `manuscript/review-map.json`, capitoli, `book-memory.md` (Continuity Ledger), `style-rules.md` (se una correzione diventa regola). Script: `review_pdf.py` (richiede `reportlab`, `pymupdf`).
**Quando:** fase di rilettura su carta / tablet.
**Esempi:**
- `/ghost-writer:corrections print 1-4` → PDF da leggere sull'iPad.
- `/ghost-writer:corrections import annotated.pdf` dopo averlo evidenziato.
- Incolli una nota vocale "al 5.8 togli 'sostanzialmente'" → `/ghost-writer:corrections`.

### retune
**Cosa fa:** riallinea un capitolo alla voce reale dell'autore quando dice "non suono così", partendo da una sua riscrittura o nota. 🔗
**File:** ✏️ capitolo (+ `version`), `book.config.json → author_voice` (nuove frasi tipiche, pattern).
**Quando:** dopo aver letto una bozza che "non è mia".
**Esempi:**
- L'autore riscrive a modo suo il primo paragrafo → `/ghost-writer:retune` lo usa per riallineare tutto il capitolo e aggiornare il profilo voce.

### character-interview
**Cosa fa:** intervista profonda su psicologia, comportamento, contraddizioni e voce di un personaggio (reale o di finzione).
**File:** ✏️ `characters/[nome].md` (cartella creata se manca), `book-memory.md → ## Characters`.
**Quando:** una volta per personaggio, prima di scriverne le scene.
**Esempi:**
- Biografia di un fondatore → `/ghost-writer:character-interview socio-fondatore`.

### character-check
**Cosa fa:** verifica che il personaggio si comporti coerentemente col suo profilo in un capitolo.
**File:** 📖 `characters/[nome].md`, capitolo, grafo. ✏️ `characters/[nome].md` (sezioni *Notes* / *Arc Moments*).
**Quando:** dopo ogni capitolo con personaggi profilati.
**Esempi:**
- `/ghost-writer:character-check marco chapters/06-crisi.md`.

### graph
**Cosa fa:** grafo del libro (personaggi, organizzazioni, luoghi, concetti, termini, eventi) collegati alla riga esatta del capitolo. Si alimenta solo dai capitoli `complete`; le altre skill ne chiamano il *Sync*.
**File:** ✏️ `graph/cards/**/*.yaml` (a mano/da skill), `graph/INDEX.md`, `graph/graph.json`, `graph/view/`, `graph/snapshots/`, `graph/chapters.yaml` (generati da `graph.py`); `docs/index.html` se esiste `site.yaml`.
**Quando:** per cercare qualcosa, forzare un sync o migrare un grafo vecchio.
**Esempi:**
- `/ghost-writer:graph find "attribution model"` → dove è definito e usato.
- `/ghost-writer:graph check` per i capitoli in attesa di sync.

---

## Chiusura

### finish
**Cosa fa:** macro di chiusura: introduzione → conclusione → audit dell'arco → assemblaggio. Salta i passi già fatti e supporta la ripresa.
**File:** ✏️ `sessions/finish.md`, `chapters/00-introduction.md`, `chapters/99-conclusion.md`, `manuscript/[titolo]-final.md`.
**Quando:** tutti i capitoli sono completi.
**Esempi:**
- Ultimo capitolo integrato → `/ghost-writer:finish`.

### write-opening
**Cosa fa:** scrive l'introduzione **per ultima**, perché può promettere solo ciò che il libro mantiene.
**File:** 📖 tutto il libro, `book-memory.md`, `outline.md`, `demolition-history.md`. ✏️ `chapters/00-introduction.md`.
**Quando:** dopo tutti i capitoli.
**Esempi:**
- `/ghost-writer:write-opening` per un ebook lead magnet appena completato.

### write-closing
**Cosa fa:** scrive la conclusione che chiude l'arco aperto dall'introduzione (non riassume: atterra).
**File:** 📖 tutto il libro, `chapters/00-introduction.md`. ✏️ `chapters/99-conclusion.md`, `book-memory.md → Open Promises` (marcate risolte).
**Quando:** dopo l'introduzione.

### manuscript-final
**Cosa fa:** audit finale (arco, promesse mantenute, corrispondenza apertura-chiusura) e assemblaggio del manoscritto pulito.
**File:** 📖 tutti i capitoli, `outline.md`, `book-memory.md`, `demolition-history.md`. ✏️ `manuscript/[titolo]-final.md`, opzionale `manuscript/process-note.md`.
**Quando:** ultimo passo prima dell'export.

---

## Export

### export-pdf
**Cosa fa:** PDF leggibile con copertina, indice e layout capitoli (ReportLab).
**File:** 📖 `book.config.json`, `manuscript/[titolo]-final.md`. ✏️ `manuscript/[titolo]-final.pdf`, `export_pdf.py` (generato se manca).
**Esempi:** PDF per i beta reader o come lead magnet da scaricare dalla landing.

### export-epub
**Cosa fa:** EPUB compatibile con Kindle, Kobo, Apple Books.
**File:** 📖 come sopra. ✏️ `manuscript/[titolo]-final.epub`, `export_epub.py`.
**Esempi:** pubblicazione self-publishing su Amazon KDP.

### export-docx
**Cosa fa:** DOCX con stili puliti per editor, agenti, editori.
**File:** 📖 come sopra. ✏️ `manuscript/[titolo]-final.docx`, `export_docx.py`.
**Esempi:** consegna al correttore di bozze che lavora in Word con revisioni.

### podcast
**Cosa fa:** trasforma il libro in podcast narrato, un episodio per capitolo: scelta voce con campioni, copioni scritti "per l'orecchio" (approvati dall'autore), MP3 e feed RSS. Gratuito e offline (Piper TTS + ffmpeg).
**File:** 📖 capitoli, `style-rules.md`. ✏️ `book.config.json → podcast`, `podcast/plan.md`, `podcast/scripts/episode-NN.md`, `podcast/episodes/episode-NN.mp3`, `podcast/feed.xml`, `podcast/voices/`, `export_podcast.py`.
**Quando:** libro completo (o capitoli completi) da riusare come contenuto audio.
**Esempi:**
- `/ghost-writer:podcast voice` → scegli la voce. `/ghost-writer:podcast script 3` → copione cap. 3.
- `/ghost-writer:podcast build 3` → MP3; `/ghost-writer:podcast feed` → RSS per Spotify/Apple.
- `/ghost-writer:podcast jingle` → sigla.

---

## Pubblicazione

### site
**Cosa fa:** genera il sito del libro (pagina unica, mobile first, per GitHub Pages): copertina, download, personaggi/idee chiave, episodi podcast, grafo esplorabile.
**File:** 📖 `graph/cards/**/*.yaml`, `podcast/**`, `manuscript/*.pdf|epub`, `cover.jpg/png`. ✏️ `site.yaml`, `docs/index.html` (+ asset copiati), `build_site.py`, `book.config.json → podcast.base_url`.
**Quando:** a libro pronto da promuovere.
**Esempi:**
- Landing gratuita per il libro con PDF scaricabile → `/ghost-writer:site`, poi push di `docs/`.

### gallery
**Cosa fa:** prepara la scheda del libro per la gallery di claudeghostwriter.com, la valida e apre una PR (o una issue precompilata). Nulla viene inviato senza OK esplicito.
**File:** 📖 `book.config.json`, `site.yaml`. ✏️ `book.config.json → gallery` (slug, URL PR/issue, data).
**Esempi:** dopo aver pubblicato il sito → `/ghost-writer:gallery`.

---

## Stato e utilità

### session-start
**Cosa fa:** briefing di inizio sessione: dove eri rimasto, cosa è in sospeso, cosa fare oggi. A fine giornata registra la sessione.
**File:** 📖 `project-state.md` (fast path se < 7 giorni), `book.config.json`, `book-memory.md`, `outline.md`, `demolition-history.md`. ✏️ `project-state.md` (rigenerato), `book-memory.md → ## Session Log`; esegue i sync del grafo in attesa.
**Esempi:** lunedì mattina, riapri il progetto dopo una settimana → `/ghost-writer:session-start`.

### resume
**Cosa fa:** una riga di stato + una sola raccomandazione sul prossimo passo. Scansione veloce, sola lettura.
**File:** 📖 `book.config.json`, `outline.md`, `sessions/`, `demolition-history.md`, ultimo file modificato in `chapters/`. ✏️ nessuno.
**Esempi:** hai 15 minuti e vuoi sapere cosa fare → `/ghost-writer:resume`.

### status
**Cosa fa:** panoramica completa: capitoli completi, in bozza, da scrivere; suggerisce il passo successivo.
**File:** 📖 `book.config.json`, `outline.md`, grafo. ✏️ nessuno.
**Esempi:** report di avanzamento da girare al cliente.

### help
**Cosa fa:** elenco di tutti i comandi per fase, con suggerimento del prossimo passo. Sola lettura.
**File:** 📖 `book.config.json` (se esiste). ✏️ nessuno.

### longform-upgrade
**Cosa fa:** attiva la modalità long-form (10+ capitoli): divide in parti, separa la memoria per parte, aggiunge riassunti ai capitoli, abilita la lettura "lazy" per tutte le skill.
**File:** ✏️ `outline.md` (header di parte), `book-memory.md` (diventa indice globale), `memory/part-N.md`, `book.config.json` (`longform_mode`), grafo.
**Quando:** automaticamente al 10° capitolo completato, o a mano.
**Esempi:** manuale da 14 capitoli che rallenta le sessioni → `/ghost-writer:longform-upgrade`.

---

## Flussi tipici

| Obiettivo | Sequenza |
|---|---|
| Nuovo libro da zero | `check` → `wizard` (o `start`) → `chapter` × N → `finish` → `export-pdf` |
| Capitolo da appunti disordinati | `freeflow` → `ask-before-writing` → `write` → `demolish` → `integrate` |
| Capitolo chiave da blindare | `chapter` → `review` → `character-check` → `proofread` |
| Rilettura su carta | `corrections print` → (annoti) → `corrections import` → `revise --all` |
| Riuso multicanale | `manuscript-final` → `export-pdf/epub` → `podcast` → `site` → `gallery` |
