#!/usr/bin/env python3
"""Generate 1200x630 og:image cards for blog posts without a cover.

Run from anywhere: python scripts/gen-og-cards.py
Re-run whenever a post is added or retitled.
"""

import subprocess
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "scripts" / "fonts"
OUT = ROOT / "static" / "og"

BG = "#1a1815"
TEXT = "#e8e5e0"
MUTED = "#94908a"
ACCENT = "#e8a068"


def render(slug: str, title: str, date: str, cover: str | None = None, focus: str = "center") -> None:
    dest = OUT / f"{slug}.png"
    footer = f"luciano.live :: blog :: {date}"

    # With a cover the photo fills the right side and text gets a narrower column
    title_box, title_pt = ("560x330", "54") if cover else ("1020x330", "68")

    cmd = ["magick", "-size", "1200x630", f"xc:{BG}"]
    if cover:
        cover_path = ROOT / "static" / cover.lstrip("/")
        cmd += [
            "(",
            str(cover_path),
            "-resize",
            "480x630^",
            "-gravity",
            focus,
            "-extent",
            "480x630",
            ")",
            "-gravity",
            "northwest",
            "-geometry",
            "+720+0",
            "-composite",
            # accent seam between text and photo
            "-fill",
            ACCENT,
            "-draw",
            "rectangle 714,0 720,630",
        ]
    cmd += [
        "-fill",
        ACCENT,
        "-draw",
        "rectangle 0,0 10,630",
        # mark
        "(",
        "-background",
        "none",
        "-fill",
        ACCENT,
        "-font",
        str(FONTS / "GeistMono.ttf"),
        "-pointsize",
        "36",
        "label:[/////]",
        ")",
        "-gravity",
        "northwest",
        "-geometry",
        "+80+70",
        "-composite",
        # title, wrapped
        "(",
        "-background",
        "none",
        "-fill",
        TEXT,
        "-font",
        str(FONTS / "Newsreader.ttf"),
        "-size",
        title_box,
        "-pointsize",
        title_pt,
        f"caption:{title}",
        ")",
        "-geometry",
        "+80+180",
        "-composite",
        # footer
        "(",
        "-background",
        "none",
        "-fill",
        MUTED,
        "-font",
        str(FONTS / "GeistMono.ttf"),
        "-pointsize",
        "26",
        f"label:{footer}",
        ")",
        "-geometry",
        "+80+540",
        "-composite",
        # keep cards small: strip metadata, max compression, palette for photo cards
        "-strip",
        "-depth",
        "8",
        "-define",
        "png:compression-level=9",
        *(["-colors", "256"] if cover else []),
        str(dest),
    ]
    subprocess.run(cmd, check=True)
    print(f"generated og/{dest.name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for md in sorted((ROOT / "content" / "blog").glob("*.md")):
        if md.name == "_index.md":
            continue
        # Posts synced by stage.py use YAML (---); older ones may still be TOML (+++)
        text = md.read_text()
        if text.startswith("---"):
            fm = yaml.safe_load(text.split("---")[1])
        else:
            fm = tomllib.loads(text.split("+++")[1])
        if fm.get("draft"):
            continue
        render(
            md.stem,
            fm["title"],
            str(fm.get("date", "")).replace("-", "."),
            fm.get("extra", {}).get("cover"),
            # which part of a wide cover to keep in the narrow card column
            fm.get("extra", {}).get("cover_focus", "center"),
        )


if __name__ == "__main__":
    main()
