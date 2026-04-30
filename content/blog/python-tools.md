+++
title = "Python tools I use"
date = 2024-01-10
draft = false
[taxonomies]
tags = ["Python", "Tooling"]
+++

As previously mentioned in this blog, Rust is becoming more and more used in Python libraries such as Pydantic and Polars. But recently we are also getting python tools written in Rust!

Few months ago, I followed the development of [Rye](https://rye-up.com/) as an alternative Python project and package manager. Later on, [Ruff](https://docs.astral.sh/ruff/) made its debut as a linter and formatter substituting the popular [flake-8](https://flake8.pycqa.org/en/latest/) and [black](https://black.readthedocs.io/en/stable/).

Thanks to their powerful backend written in Rust, these tools all provide a substantial upgrade in terms of performance and flexibility compared to the tools they are aiming to replace (up to 100x faster).

## Ruff

I found `ruff format` to be the easiest tool to replace. I often bind the reformat command to a shortcut or to reformat while saving. But more often, I tend to reformat the whole project before committing. The performance of Ruff allows me to confidently reformat thousands of lines knowing that I will not need to wait long.

Adopting `ruff format` together with `ruff check` in your pipelines can substantially reduces your actions time!

## Rye

Even before Astral's ruff and uv were available, I got Rye a try. Rye was the first attempt to implement a "Cargo for Python" - a 360-degree project and package management at your fingertips. I immediately found Rye very easy to use and, to some extent, similar to Poetry! However, the lack of implementations for VS Code or PyCharm (at the time of testing) made me reluctant to adopt it full time.

## Uv

Uv is the latest addition to the Rust-born Python family tools. It is the fastest package manager out there and is able to quickly resolve most of your package dependencies. It is also a replacement for `venv`, so you can quickly set up a new virtual environment for your Python project.

After Uv was released, Astral also announced the takeover of Rye and implemented uv as the core package manager for Rye.

## What I use, what I am not using and what's next

I now use ruff on a daily basis both at work and for private projects. It is so easy to use that I often forget it is running.

Due to the current lack of support for Pycharm (the IDE I use at work) I am not currently using either Rye nor Uv at work, but I am still using them on my local machine for personal projects.

![Ruff linter performance](/assets/img/ruff-graph-dark.svg)

I look forward to seeing what Astral is developing next - perhaps a "Clippy for Python" or a rust-based static type checker to substitute mypy? Everything seems to be possible at this point.

## My actual setup

For my daily workflow, I use:

- **ruff** — Enabled in all projects, bound to save in VS Code. Run `ruff check . && ruff format .` before every commit.
- **uv** — For new projects. `uv venv && uv sync` replaces the old `python -m venv && pip install -r requirements.txt` dance.
- **Poetry** — Still use this at work because PyCharm support is better than uv's right now.

The combination of fast tooling and good editor integration is what makes this workflow viable. If your IDE doesn't support the tool, the speed gains don't matter.

## Update: Rye

*January 2025 note:* After writing this post, I discovered that Rye's virtual environments work with most IDEs — they're just regular virtualenvs! I was wrong to dismiss it. I now use Rye full-time for personal projects.

My tip: always run `rye sync` after `rye add` — this installs the actual packages. Although I like this behavior, an option to default `rye sync` after every `rye add` (like `cargo add`) would be nice.
