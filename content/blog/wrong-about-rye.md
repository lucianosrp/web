+++
title = "I was wrong about Rye"
date = 2024-03-14
draft = false
+++

While talking about Rye, in the previous post I wrote that the lack of implementations for VScode or Pycharm had made me reluctant to adopt it full time.

By "lack of implementations" I meant that there was no python environment finder suited for Rye's virtual environment. I probably did not use Rye properly in the first time, since Rye's virtual env is *literally* a Virtualenv, and so it can be discovered by all majors IDEs.

Somehow, I first thought Rye had its own virtual environment type!

Since finding this out, I now intend to use it full-time and will post more about it whenever needed.

My tips for using it is to make sure to `rye sync` after every `rye add` since this last command does not install the actual packages that will be listed on the project configuration itself. Although I like this behaviour, I would love to have an option to default `rye sync` after every `rye add` (similar to `cargo add`).

Also, `uv` integration does not come as a default. It needs to be enabled in the global rye configurations!
