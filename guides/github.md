# Ghost Writer + GitHub — guida pratica

Come usare GitHub con il plugin Ghost Writer: perché conviene, come collegarlo a Claude (Desktop e Code) e quali funzioni di GitHub usare per il sito del libro.

---

## 1. Perché conviene usare GitHub

Un libro scritto con Ghost Writer è una cartella di file di testo (`chapters/`, `book.config.json`, `book-memory.md`, `outline.md`, `graph/`, `podcast/`…). Metterla su GitHub ti dà:

| Vantaggio | Cosa significa per l'autore |
|---|---|
| **Storico di ogni versione** | Ogni `demolish` → `integrate` cambia il testo. Con git puoi rivedere o recuperare qualsiasi versione precedente di un capitolo, anche mesi dopo. |
| **Backup automatico** | Il libro non vive solo sul tuo computer. Se il disco si rompe, fai `git clone` e riparti. |
| **Lavoro da più dispositivi** | Scrivi su Claude Desktop a casa, rivedi con Claude Code sul portatile, oppure da claude.ai/code nel browser: stessa cartella, sempre aggiornata. |
| **Collaborazione** | Co-autori, editor e beta reader possono proporre modifiche (pull request) o lasciare note (issue) senza toccare il testo principale. |
| **Sito gratuito** | `/ghost-writer:site` genera un sito pronto per **GitHub Pages**: hosting gratis, HTTPS incluso. |
| **Distribuzione** | PDF, EPUB e MP3 del podcast possono stare nelle **Releases** di GitHub, con un link stabile per ogni versione. |
| **Gallery** | `/ghost-writer:gallery` apre una pull request su claudeghostwriter.com per pubblicare il libro nella gallery del sito. Senza account GitHub si usa un form, con l'account è tutto automatico. |

**Repository privato o pubblico?** Le bozze di norma stanno in un repo **privato**. Attenzione: GitHub Pages su repo privato richiede un piano a pagamento (GitHub Pro). Soluzione gratuita: repo privato per il libro + repo pubblico solo per il sito (vedi §3.5).

---

## 2. Configurazione

### 2.1 Prerequisiti (una volta sola)

1. Crea un account su [github.com](https://github.com).
2. Installa **git** ([git-scm.com](https://git-scm.com)) e la **GitHub CLI** ([cli.github.com](https://cli.github.com)).
3. Accedi da terminale:

   ```bash
   gh auth login        # GitHub.com → HTTPS → login con browser
   gh auth setup-git    # git usa le credenziali di gh
   ```

4. Trasforma la cartella del libro in un repository:

   ```bash
   cd il-mio-libro
   git init
   git add .
   git commit -m "Inizio del libro"
   gh repo create il-mio-libro --private --source . --push
   ```

Il plugin include già un `.gitignore` che esclude le voci Piper, i campioni audio e i kit musicali (file pesanti e rigenerabili).

### 2.2 Claude Code (terminale, IDE, app desktop)

Claude Code usa direttamente `git` e `gh` installati sul tuo computer: dopo il §2.1 non serve altro.

**Installa il plugin da GitHub:**

```bash
/plugin marketplace add simonediroma/claude-ghost-writer
/plugin install ghost-writer@simonediroma-ghost-writer
/ghost-writer:check
```

**Aggiornare il plugin** quando esce una nuova versione:

```bash
/plugin marketplace update simonediroma-ghost-writer
```

**Uso quotidiano** — basta chiederlo in linguaggio naturale:

- *"Fai commit del capitolo 3 con un messaggio che riassuma l'integrazione"*
- *"Mostrami cosa è cambiato nel capitolo 5 rispetto a ieri"*
- *"Riporta il capitolo 2 alla versione di prima della demolizione"*
- *"Push su GitHub"*

Abitudine consigliata: un commit alla fine di ogni ciclo `/ghost-writer:chapter` e dopo ogni `integrate`.

**Opzionale — Claude dentro GitHub.** Con `/install-github-app` installi la GitHub App di Claude sul repo: potrai scrivere `@claude` in una issue o pull request (es. *"@claude applica le correzioni di questa issue al capitolo 4"*).

**Claude Code sul web (claude.ai/code).** Collega GitHub dalle impostazioni e scegli il repo del libro: Claude lavora su una copia nel cloud e fa push su un branch. Utile per lavorare dal telefono o da un computer senza niente installato.

### 2.3 Claude Desktop (Chat e Cowork)

**Installa il plugin:**
- in un clic dalla [directory dei plugin di Claude](https://claude.ai/customize/plugins/id/4b831b3b-c718-4a20-b786-598ed6566696%40anthropic-plugin-directory) (si sincronizza su Claude Code e Cowork), oppure
- scarica il file `.plugin` da [claudeghostwriter.com](https://claudeghostwriter.com) e trascinalo nell'app (o caricalo da **Impostazioni → Plugin**).

**Collega GitHub:**
1. **Impostazioni → Connettori → GitHub → Connetti** e autorizza l'accesso.
2. In una chat o in un Progetto: pulsante **+** → **Aggiungi da GitHub** → scegli il repo e i file (es. `outline.md`, `book-memory.md`, i capitoli).

Il connettore serve a dare a Claude il **contesto** del libro (leggere capitoli, outline, memoria) per discuterne, fare brainstorming o rivedere. Per **scrivere** sui file e fare commit usa Cowork sulla cartella locale del libro, oppure la scheda **Code** dell'app Desktop (è Claude Code, e funziona come al §2.2).

Flusso tipico misto: scrivi e committi con Claude Code / Cowork → in Chat, con il connettore GitHub, discuti il capitolo appena pushato.

---

## 3. Le funzioni di GitHub per il sito

`/ghost-writer:site` genera `docs/index.html`: una pagina unica, senza dipendenze esterne, con copertina, presentazione, download, personaggi/idee chiave, podcast e grafo del libro.

### 3.1 GitHub Pages — l'hosting (gratis)

Metodo più semplice, senza configurazione:

1. Commit e push di `docs/`.
2. Repo → **Settings → Pages → Build and deployment → Deploy from a branch** → branch `main`, cartella `/docs` → **Save**.
3. Dopo circa un minuto il sito è online su `https://<utente>.github.io/<repo>/`.

Limiti: 1 GB per sito, 100 MB per file, circa 100 GB di traffico al mese. Un episodio a 96 kbps pesa circa 0,7 MB al minuto.

### 3.2 Dominio personalizzato

1. **Settings → Pages → Custom domain** → `www.ilmiolibro.it` → Save (GitHub crea il file `CNAME`).
2. Dal tuo provider DNS: record `CNAME` da `www` a `<utente>.github.io`.
3. Spunta **Enforce HTTPS** quando diventa disponibile.

### 3.3 GitHub Actions — sito sempre aggiornato

Invece di ricostruire e pushare `docs/` a mano, lascia che GitHub lo rigeneri a ogni push. Crea `.github/workflows/site.yml`:

```yaml
name: Sito del libro
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pyyaml pillow
      - run: python3 build_site.py
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Poi **Settings → Pages → Source: GitHub Actions**. Da quel momento ogni push (nuovo capitolo, sync del grafo, nuovo episodio) aggiorna il sito da solo, e `docs/` non serve più committarlo.

### 3.4 Releases — PDF, EPUB e podcast

Le Releases accettano file fino a 2 GB, non pesano sul limite di 1 GB di Pages e danno un link stabile per ogni versione del libro:

```bash
gh release create v1.0 manuscript/il-mio-libro.pdf manuscript/il-mio-libro.epub \
  --title "Prima edizione" --notes "Capitoli 1–12"
```

Link diretto al file: `https://github.com/<utente>/<repo>/releases/download/v1.0/il-mio-libro.pdf`. Usalo come `book.download` in `site.yaml`, oppure carica gli MP3 in una release e usa quell'indirizzo come `podcast.base_url` (vedi `/ghost-writer:podcast`). Conviene quando il podcast supera qualche centinaio di MB.

### 3.5 Libro privato, sito pubblico

Se il repo del libro è privato e non hai GitHub Pro:

1. Crea un secondo repo **pubblico**, ad esempio `il-mio-libro-sito`.
2. Copia lì il contenuto di `docs/` dopo ogni build (o chiedilo a Claude: *"copia docs/ nel repo del sito e fai push"*).
3. Attiva Pages sul repo pubblico (§3.1).

Bozze, demolizioni e memoria restano private: online va solo quello che hai approvato in `site.yaml`.

### 3.6 Issues e Discussions — feedback dei lettori

- **Issues**: apri una issue per capitolo e chiedi ai beta reader di commentare lì. Poi incolla il testo in `/ghost-writer:corrections import` per trasformarlo in correzioni.
- **Discussions** (Settings → Features): uno spazio pubblico per i lettori del sito. Aggiungi il link in `site.yaml` o nel footer.

### 3.7 Gallery di claudeghostwriter.com

Quando il sito è online, `/ghost-writer:gallery` prepara la scheda del libro e, con `gh` autenticato, apre la pull request sul repo del sito ufficiale (fork + branch + PR). Senza `gh` genera il link a un form di issue precompilato. Non viene inviato niente senza il tuo OK.

---

## Riepilogo veloce

| Obiettivo | Strumento |
|---|---|
| Versioni e backup del libro | repo privato + commit dopo ogni `integrate` |
| Scrivere con Claude | Claude Code (CLI, IDE, scheda Code) o Cowork |
| Discutere il libro in chat | Claude Desktop + connettore GitHub |
| Sito gratuito | `/ghost-writer:site` + GitHub Pages |
| Sito che si aggiorna da solo | GitHub Actions |
| Download e podcast pesanti | GitHub Releases |
| Feedback dei lettori | Issues / Discussions |
| Vetrina pubblica | `/ghost-writer:gallery` |
