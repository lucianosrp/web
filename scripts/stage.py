#!/usr/bin/env python3
"""Sync a post from the Obsidian vault into content/blog/, translating Obsidian
markdown into what Zola expects.

    python scripts/stage.py "Programming has changed (again)"   # by title / filename (fuzzy)
    python scripts/stage.py --all                               # every vault post already in content/blog
    python scripts/stage.py NAME --publish                      # also flip draft: false (vault + site) and tick blog/TODO.md
    python scripts/stage.py NAME --dry-run                      # show what would be written

Vault front matter (plain Obsidian YAML, all optional except title):

    ---
    title: Post title
    date: 2026-09-17
    draft: true
    description: One-liner for the post list / <meta description> / social cards
    tags: [AI, Python]
    cover: /assets/img/<slug>/hero.webp
    cover_alt: Alt text for the cover
    updated: 2026-10-01
    slug: custom-slug          # default: slugified title
    ---

What gets translated:
  {reviewer notes}            removed (single curly braces = notes for the LLM reviewer)
  %% obsidian comments %%     removed
  #tag in the body            -> [#tag](/tags/tag/)  and added to the post's tags
  [[#Heading]] / [[#H|text]]  -> [text](#heading-slug)
  [[Other post]]              -> [Other post](/blog/other-post/)   (when it is another blog post)
  ![[image.png|alt]]          -> copied to static/assets/img/<slug>/ (png/jpg -> webp) and rendered
                                 with the `img` component (intrinsic width/height)
  ![alt](/assets/...)         -> `img` component (svg stays plain markdown)
  > [!note] Title             -> blockquote with a bold title
  ==highlight==               -> <mark>highlight</mark>
  tags / cover / cover_alt    -> taxonomies.tags / extra.cover / extra.cover_alt
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "blog"
ASSETS = ROOT / "static" / "assets" / "img"
VAULT = Path(os.environ.get("VAULT_BLOG", "~/notes/blog")).expanduser()
TRACKER = VAULT / "TODO.md"
VAULT_SKIP = {"TODO.md", "_index.md"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}
TO_WEBP = {".png", ".jpg", ".jpeg"}


# ---------------------------------------------------------------- helpers
def slugify(text: str) -> str:
    """Approximation of Zola's slugifier (for headings, tags and filenames)."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_]+", "-", text).strip("-")


def split_front_matter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]


def warn(msg: str) -> None:
    print(f"  ! {msg}", file=sys.stderr)


class Protect:
    """Swap fenced / inline code for placeholders so transforms leave code alone."""

    def __init__(self) -> None:
        self.saved: list[str] = []

    def hide(self, text: str) -> str:
        def stash(m: re.Match) -> str:
            self.saved.append(m.group(0))
            return f"\x00{len(self.saved) - 1}\x00"

        text = re.sub(r"```.*?```", stash, text, flags=re.S)
        return re.sub(r"`[^`\n]+`", stash, text)

    def restore(self, text: str) -> str:
        return re.sub(r"\x00(\d+)\x00", lambda m: self.saved[int(m.group(1))], text)


# ---------------------------------------------------------------- vault lookup
def vault_posts() -> list[Path]:
    return sorted(p for p in VAULT.glob("*.md") if p.name not in VAULT_SKIP)


def post_meta(path: Path) -> tuple[dict, str]:
    fm, body = split_front_matter(path.read_text())
    return fm, body


def post_slug(fm: dict, path: Path) -> str:
    """Explicit slug > vault filename that already is a slug (published posts) > slugified title."""
    if fm.get("slug"):
        return fm["slug"]
    if path.stem == slugify(path.stem):
        return path.stem
    return slugify(fm.get("title") or path.stem)


def find_post(name: str) -> Path:
    key = name.lower().removesuffix(".md")
    posts = vault_posts()
    for p in posts:  # exact filename / title
        fm, _ = post_meta(p)
        if key in {p.stem.lower(), str(fm.get("title", "")).lower(), post_slug(fm, p)}:
            return p
    hits = [p for p in posts if key in p.stem.lower() or key in str(post_meta(p)[0].get("title", "")).lower()]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        sys.exit(f"no vault post matches {name!r}")
    sys.exit("ambiguous name, matches: " + ", ".join(p.name for p in hits))


def find_attachment(name: str) -> Path | None:
    for root, dirs, files in os.walk(VAULT.parent):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        if name in files:
            return Path(root) / name
    return None


# ---------------------------------------------------------------- body transforms
def convert_body(body: str, slug: str, tags: list[str], titles: dict[str, str], dry: bool) -> str:
    prot = Protect()
    body = prot.hide(body)

    # reviewer notes {like this} and obsidian %% comments %%
    body = re.sub(r"%%.*?%%", "", body, flags=re.S)
    body = re.sub(r"(?<!\{)\{(?![{%])[^{}\n]*\}(?!\})", "", body)

    # anything that still looks like Tera must be neutralised
    if "{{" in body or "{%" in body:
        warn("literal '{{' or '{%' in the text — escaped for Tera")
        body = body.replace("{{", '{{ "{{" }}').replace("{%", '{{ "{%" }}')

    # ==highlight==
    body = re.sub(r"==([^=\n]+)==", r"<mark>\1</mark>", body)

    # > [!note] Title  -> blockquote with a bold first line
    def callout(m: re.Match) -> str:
        kind, title = m.group(1), (m.group(2) or "").strip()
        return f"> **{title or kind.capitalize()}**"

    body = re.sub(r"^> \[!(\w+)\][+-]?(.*)$", callout, body, flags=re.M)

    # ![[file|alt]] embeds
    def embed(m: re.Match) -> str:
        name, alt = m.group(1).strip(), (m.group(2) or "").strip()
        src = find_attachment(name)
        if not src:
            warn(f"attachment not found in vault: {name}")
            return f"![{alt}](MISSING:{name})"
        ext = src.suffix.lower()
        if ext not in IMAGE_EXT:
            warn(f"non-image embed left as a link: {name}")
            return f"[{alt or name}]({name})"
        dest_dir = ASSETS / slug
        if ext in TO_WEBP and shutil.which("magick"):
            dest = dest_dir / (src.stem + ".webp")
            if not dry:
                dest_dir.mkdir(parents=True, exist_ok=True)
                subprocess.run(["magick", str(src), "-resize", "1600x>", "-quality", "85", str(dest)], check=True)
        else:
            dest = dest_dir / src.name
            if not dry:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
        print(f"  + image {src.name} -> {dest.relative_to(ROOT)}")
        return f"![{alt}](/assets/img/{slug}/{dest.name})"

    body = re.sub(r"!\[\[([^\]|]+)(?:\|([^\]]*))?\]\]", embed, body)

    # [[#Heading|text]], [[Post]], [[Post#Heading|text]]
    def wikilink(m: re.Match) -> str:
        target, heading, label = m.group(1), m.group(2), m.group(3)
        if not target:  # same-page heading
            return f"[{label or heading}](#{slugify(heading)})"
        other = titles.get(target.lower())
        anchor = f"#{slugify(heading)}" if heading else ""
        if other:
            return f"[{label or target}](/blog/{other}/{anchor})"
        warn(f"wikilink to a non-blog note left as text: [[{target}]]")
        return label or target

    body = re.sub(r"\[\[([^\]#|]*)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]", wikilink, body)

    # inline #tags (not headings, not colours, not anchors/urls)
    def tag(m: re.Match) -> str:
        name = m.group(1)
        if re.fullmatch(r"[0-9a-fA-F]{3}|[0-9a-fA-F]{6}", name):
            return m.group(0)
        if slugify(name) not in {slugify(t) for t in tags}:
            tags.append(name)
        return f"[#{name}](/tags/{slugify(name)}/)"

    body = re.sub(r"(?<![\w&/#\[(])#([A-Za-z][\w/-]*)", tag, body)

    # local images -> img component (svg has no readable metadata, stays markdown)
    def image(m: re.Match) -> str:
        alt, src = m.group(1).replace('"', "'"), m.group(2)
        if src.lower().endswith(".svg"):
            return m.group(0)
        return f'{{{{ <img src="{src}" alt="{alt}" /> }}}}'

    body = re.sub(r"!\[([^\]]*)\]\((/assets/[^)\s]+)\)", image, body)

    return prot.restore(body)


# ---------------------------------------------------------------- front matter
def zola_front_matter(fm: dict, tags: list[str]) -> str:
    out: dict = {}
    for key in ("title", "date", "updated", "draft", "description", "slug"):
        if key in fm and fm[key] not in (None, ""):
            out[key] = fm[key]
    out.setdefault("draft", True)
    if tags:
        out["taxonomies"] = {"tags": tags}
    extra = {k: fm[k] for k in ("cover", "cover_alt") if fm.get(k)}
    if extra:
        out["extra"] = extra
    return "---\n" + yaml.safe_dump(out, sort_keys=False, allow_unicode=True, default_flow_style=None) + "---\n\n"


def set_vault_draft(path: Path, value: bool) -> None:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = m.group(1)
    fm = re.sub(r"^draft:.*$", f"draft: {str(value).lower()}", fm, flags=re.M) if re.search(r"^draft:", fm, re.M) \
        else fm + f"\ndraft: {str(value).lower()}"
    path.write_text(f"---\n{fm}\n---\n" + text[m.end():])


def tick_tracker(title: str) -> None:
    if not TRACKER.exists():
        return
    lines = TRACKER.read_text().splitlines()
    try:
        i = next(i for i, l in enumerate(lines) if l.strip() == f"- [ ] {title}")
    except StopIteration:
        return
    lines.pop(i)
    try:
        pub = next(i for i, l in enumerate(lines) if l.strip() == "## Published")
        j = pub + 1
        while j < len(lines) and (lines[j].startswith("- [x]") or not lines[j].strip()):
            j += 1
        # insert after the last published item
        k = j - 1
        while k > pub and not lines[k].strip():
            k -= 1
        lines.insert(k + 1, f"- [x] {title}")
    except StopIteration:
        lines.append(f"- [x] {title}")
    TRACKER.write_text("\n".join(lines) + "\n")
    print(f"  ✓ ticked in {TRACKER.name}")


# ---------------------------------------------------------------- main
def stage(path: Path, titles: dict[str, str], publish: bool, dry: bool) -> None:
    fm, body = post_meta(path)
    if "title" not in fm:
        sys.exit(f"{path.name}: needs YAML front matter with at least a title")
    if publish:
        fm["draft"] = False
    slug = post_slug(fm, path)
    tags = list(fm.get("tags") or [])
    print(f"{path.name} -> content/blog/{slug}.md")
    out = zola_front_matter(fm, tags) if not tags else None  # placeholder, tags may grow below
    new_body = convert_body(body.lstrip("\n"), slug, tags, titles, dry)
    out = zola_front_matter(fm, tags) + new_body.rstrip("\n") + "\n"
    if dry:
        print(out)
        return
    CONTENT.mkdir(parents=True, exist_ok=True)
    (CONTENT / f"{slug}.md").write_text(out)
    if publish:
        set_vault_draft(path, False)
        tick_tracker(fm["title"])
        print("  ✓ draft: false — run scripts/gen-og-cards.py before deploying")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?", help="post title, filename or slug (fuzzy)")
    ap.add_argument("--all", action="store_true", help="re-sync every vault post already present in content/blog")
    ap.add_argument("--publish", action="store_true", help="set draft: false in vault and site, tick TODO.md")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not (args.name or args.all):
        ap.error("give a post name or --all")

    posts = vault_posts()
    titles = {}
    for p in posts:
        fm, _ = post_meta(p)
        s = post_slug(fm, p)
        for key in {p.stem, str(fm.get("title", "")), s}:
            if key:
                titles[key.lower()] = s

    if args.all:
        targets = [p for p in posts if (CONTENT / f"{post_slug(post_meta(p)[0], p)}.md").exists()]
    else:
        targets = [find_post(args.name)]
    for p in targets:
        stage(p, titles, args.publish, args.dry_run)


if __name__ == "__main__":
    main()
