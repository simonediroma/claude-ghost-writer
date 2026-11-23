# claudeghostwriter.com

Static site, no build. Deployed to GitHub Pages by `.github/workflows/pages.yml` on every push to `main` that touches `website/`.

## Add a book to the gallery

Append an entry to `books.json`:

```json
{
  "title": "Book title",
  "author": "Author name",
  "genre": "fiction",
  "language": "it",
  "year": 2026,
  "description": "One or two sentences.",
  "cover": "assets/covers/book-title.jpg",
  "links": [{ "label": "Read", "url": "https://..." }]
}
```

`genre` = one of the presets (essay, fiction, manual, biography, fable, childrens-book). `cover` is optional (2:3 ratio, put the file in `assets/covers/`); without it a generated cover is shown.

## Preview locally

```bash
cd website && python3 -m http.server 8000
```

## Domain setup (once)

1. Repo **Settings → Pages → Source: GitHub Actions**; Custom domain: `claudeghostwriter.com`, then **Enforce HTTPS**.
2. At the DNS provider:
   - `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` for `www` → `simonediroma.github.io`
