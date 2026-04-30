+++
title = "I was wrong about Rye"
date = 2024-03-14
draft = false
tags = ["Python"]
+++

While talking about Rye in my post on Python tools, I wrote that the lack of implementations for VS Code or PyCharm made me reluctant to adopt it full time.

By that I meant there was no Python environment finder suited for Rye's virtual environment. I probably didn't use Rye properly the first time, since Rye's virtual env is *literally* a Virtualenv, and so it can be discovered by all major IDEs. Somehow I thought Rye had its own virtual environment type!

Since finding this out, I now use it full-time for personal projects.

## My tips for using Rye

1. **Always run `rye sync` after `rye add`** — The `add` command only updates your project configuration. It doesn't install packages. Run `rye sync` afterward to actually install them. I wish there was an option to make this the default behavior (like `cargo add`).

2. **Enable uv integration** — It doesn't come enabled by default. Add this to your global Rye config:

```toml
[global]
use-uv = true
```

This makes package installation much faster.

## What I was wrong about

The core mistake was assuming that "custom virtual environment format" meant "incompatible with everything." I should have tested it in my IDE first before writing it off.

The lesson: Don't assume — test.