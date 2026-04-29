+++
title = "How Rust tools are taking over the Python dev ecosystem"
date = 2024-03-03
draft = false
+++

As previously mentioned in this blog, Rust is becoming more and more used in Python libraries such as Pydantic and Polars. But recently we are also getting python tools written in Rust!

Few months ago, I followed the development of [Rye](https://rye-up.com/) as an alternative Python project and package manager. Later on, [Ruff](https://docs.astral.sh/ruff/) made its debut as a linter and formatter substituting the popular [flake-8](https://flake8.pycqa.org/en/latest/) and [black](https://black.readthedocs.io/en/stable/).

Thanks to their powerful backend written in Rust, these tools all provide a substantial upgrade in terms of performance and flexibility compared to the tools they are aiming to replace (up to 100x faster).

## Ruff

I found `ruff format` to be the easiest tool to replace. I often bind the reformat command to a shortcut or to reformat while saving. But more often, I tend to reformat the whole project before committing. The performance of Ruff allows me to confidently reformat thousands of lines knowing that I will not need to wait long.

Adopting `ruff format` together with `ruff check` in your pipelines can substantially reduces your actions time!

## Rye

Even before Astral's ruff and uv were available, I got Rye a try. Rye was the first attempt to implement a "Cargo for Python" - a 360 degrees project and package management at your fingertips. I immediately found Rye very easy to use and, to some extent, similar to Poetry! However, the lack of implementations for VScode (at the time of testing) or Pycharm had made me reluctant to adopt it full time.

## Uv

Uv is the latest addition to the Rust-born Python family tools. It is the fastest package manager out there and is able to quickly resolve most of your painful package dependencies. It is also a replacement for `venv`, so you can quickly set up a new virtual environment for your Python project.

After Uv was released, Astral also announced the takeover of Rye and implemented uv as the core package manager for Rye.

## What I use, what I am not using and what's next

I now fully use ruff on a daily basis both at work and for private projects. It is so easy to use that I often forget it is running.

Due to the current lack of support for Pycharm (the IDE I use at work) I am not currently using either Rye nor Uv at work, but I am still using them on my local machine for personal projects.

I look forward to see what Astral is developing next - perhaps a "Clippy for Python" or a rust-based static type checker to substitute mypy? Everything seems to be possible at this point.
