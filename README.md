# luciano.live

Personal blog, built with [Zola](https://www.getzola.org/) (`zola 0.23+`).

## Writing

Posts are drafted in the Obsidian vault (`~/notes/blog/`, the staging area) and
synced here when ready. Front matter:

```toml
+++
title = "Post title"
date = "2026-01-31"
draft = true                      # hides the post from production builds
description = "One line shown in the post list, <meta description> and social cards."
updated = "2026-02-10"            # optional, shows "updated" in post-meta
[taxonomies]
tags = ["Python", "AI"]
[extra]
cover = "/assets/img/<slug>/hero.webp"   # optional hero + list thumbnail + og card photo
cover_alt = "Alt text for the hero"
+++
```

Conventions:

- Slug = filename (`kebab-case.md`).
- Local images go in `static/assets/img/<slug>/`, preferably **webp**. Use the `img` component so
  the browser knows the dimensions (no layout shift):
  `{{ <img src="/assets/img/<slug>/pic.webp" alt="..." caption="optional" /> }}`
  (SVGs: plain markdown `![alt](/assets/...)`, `get_image_metadata` doesn't read them.)
- Footnotes (`[^1]`) are collected at the bottom of the post and get a hover preview.
- Headings get a table of contents automatically when there is more than one.
- Same-page links: `[text](#heading-slug)`.
- Content is Tera-templated (Zola 0.23): literal `{{`/`{%` in a post must be wrapped in `{% raw %}…{% endraw %}`.

## Social cards

`scripts/gen-og-cards.py` renders a 1200×630 `static/og/<slug>.png` for every non-draft
post (needs ImageMagick `magick`). Re-run after adding, retitling or un-drafting a post.

## Commands

```bash
zola serve --drafts   # local preview with drafts, http://127.0.0.1:1111
zola build            # production build to public/
zola check            # validate internal/external links
python scripts/gen-og-cards.py
```

## Layout

- `config.toml` — site settings; `[markdown]` has highlighting, footnotes, anchors.
- `templates/` — Tera templates (`base.html` handles all `<head>` metadata).
- `templates/components.html` — Tera components (the `img` figure).
- `static/style.css` — all styling; colors are CSS variables in `:root` with a
  `prefers-color-scheme: dark` override. Prose is Newsreader (serif), site chrome and code are
  Geist Mono.
- `static/fonts/` — self-hosted woff2 subsets, generated from `scripts/fonts/*.ttf` with
  `fonttools varLib.instancer` (wght 400–600) + `pyftsubset --flavor=woff2`.
- `static/og/` — generated social cards (see above).

## Deployment

`public/` is the built site; publish it to the hosting branch / Pages workflow.
