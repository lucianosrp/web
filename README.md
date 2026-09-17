# luciano.live

Personal blog, built with [Zola](https://www.getzola.org/) (`zola 0.23+`).

## Writing

Posts are written in the Obsidian vault (`~/notes/blog/`) as plain Obsidian markdown and synced
here with one command (run from this repo):

```bash
python scripts/stage.py "Post title"            # vault -> content/blog/<slug>.md
python scripts/stage.py "Post title" --publish  # also draft: false + tick the vault tracker
python scripts/stage.py --all                   # re-sync every published post
```

Vault front matter is ordinary Obsidian YAML:

```yaml
---
title: Post title
date: 2026-01-31
draft: true                 # hidden from production builds
description: One line for the post list, <meta description> and social cards.
tags: [Python, AI]
cover: /assets/img/<slug>/hero.webp   # optional hero + list thumbnail + og card photo
cover_alt: Alt text for the hero
updated: 2026-02-10         # optional, shows "updated" in post-meta
slug: custom-slug           # optional, default is the slugified title
---
```

`stage.py` translates Obsidian syntax on the way in: `{reviewer notes}` and `%% comments %%` are
removed, inline `#tags` become tag links (and are added to the post's tags), `[[#Heading]]` /
`[[Other post]]` become links, `![[image.png]]` is copied to `static/assets/img/<slug>/`
(png/jpg → webp) and rendered with the `img` component, `> [!note]` callouts become blockquotes,
`==text==` becomes `<mark>`. Content is Tera-templated (Zola 0.23), so literal `{{`/`{%` are escaped.

Notes:

- Slug = filename in `content/blog/`, derived from the title.
- SVGs stay plain markdown (`get_image_metadata` can't read them).
- Footnotes (`[^1]`) are collected at the bottom of the post and get a hover preview.
- A table of contents is generated automatically when a post has more than one heading.

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
