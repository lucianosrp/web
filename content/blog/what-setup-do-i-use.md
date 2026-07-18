+++
title = "What setup do I use?"
date = 2026-07-17
draft = false
tags = ["Programming"]

[extra]
cover = "/assets/img/setup/setup.webp"
cover_alt = "My desk setup"
+++

I have often talked about Zellij (my last two talks, at the Rust Meetup and OpenSource Hong Kong, were about it), but I never showed my actual setup.

Since early this year, I have substantially changed my setup, and I have now reached a point where I am quite satisfied with it — so much so that I think it is now time to finally "unveil" it to the public. I believe some people might also be interested in my decision-making process, so I will make my best attempt at describing it too.

As always, this is definitely not a perfect setup and it is definitely not for everyone — I might be changing this setup moving forward as I discover new things.

I will divide this post into two parts: the hardware and the software. In each part, I will also describe each component.

## My design philosophy

Before diving in, it helps to know that everything I picked follows the same three principles:

- **Portable** — I travel a lot, so everything has to come with me: the hardware in a backpack, the software on any machine I happen to land on.
- **Lightweight** — no bloatware, no heavy GUIs, nothing that eats storage or memory for services I don't need.
- **Easy to run** — good defaults, little to no configuration, and quick to install. I don't want to keep track of every single configuration file.

If you notice the same words coming back throughout this post — that's the point. Every component below earned its place by ticking these three boxes.

## Hardware

This is definitely the part which will change from person to person, as I know some people have very clear preferences compared to others.

Personally, I don't have any hard preferences when it comes to hardware. For now I'm sticking to this setup — I might change my mind later. When it comes to hardware, I don't have many requirements, but I generally like it to be:

- Durable
- Portable
- Affordable

Getting all three of these is not always easy!

### PC

I currently use an ASUS G14 laptop. To me, it provides the best balance between performance and portability — the latter being the most important point, since I will usually bring it around while travelling.

The only downside is the battery, which can last just a couple of hours, or even less on the highest performance profile.

### Keyboard

I use a "cheap" Corne V4.1, which is a small split keyboard. I have been using it for about 6 months now, and I have to say: it definitely took me a while to learn to use it properly. The keyboard comes in a very small form factor, which means that many keys are actually missing! To access those symbols (such as the number keys), I need to press a combination of activation keys which unveil multiple layers. This brings two advantages: the keyboard stays small, and your fingers usually stay in the same place. But it also comes with a very steep and frustrating learning curve.

### Display

This is the bit I am the most "satisfied" with. I am using a portable Ugreen AP16 screen: a 500-nit, 2.5K, 165Hz, 16-inch display.

I am very happy with how it looks; the display is very well built, so much so that it resembles an *Apple* product. It is very easy to carry around and comes with a magnetic stand.

### Mouse

I don't usually use a mouse, but when I have to, I like to use Logitech's MX Master 3S — which, I believe, provides the best ergonomics, and it is also very lightweight!

## Software

Here is where the fun part comes. I am generally not too strict with the hardware — I could really use just about anything with my current setup! (Continue reading to find out why.) But when it comes to software, I usually stick to the same set of applications, no matter which platform.

The three principles above translate into two hard requirements for any software I install:

- No bloatware

> When I download something on my laptop, I am sacrificing some valuable amount of storage for it (and some memory too, if it needs to run in the background). Therefore, I want each byte of it to be dedicated to the sole purpose of the software itself. This means that I will usually avoid software that offers a full-blown GUI if it's just offering some basic services. I won't name-call any particular software here, but I generally like to avoid Electron apps, which often take more space than they should. Lightweight software also tends to be portable and easy to install — the principles reinforce each other.

- Easy to configure, or no configuration at all

> I love software that comes with a good set of default options. I don't generally like having to spend time re-configuring applications every time I install them, and I don't like keeping track of every single configuration file. Having good "ready to use" software is really important, and it is useful to keep a good peace of mind.

### Arch Linux

I used Fedora for a couple of years before moving to Arch. Fedora is great, and I really enjoyed using it, but what mainly brings me to Arch is the AUR, where I can always find the latest and greatest software without having to struggle too much. I also enjoy the fact that it is now easy to install Arch, and that it can come with very few dependencies.

### Zellij

This has now become a must for me. I usually work on remote machines, so I will usually download Zellij there and remote into it.

It is great; the default settings are already optimal for me — no configuration needed, exactly how I like it. I will have multiple Claude Code sessions in it, and I don't have to worry too much about being suddenly disconnected!

### Claude Code

To me, this remains one of the best harnesses (also because I am forced to use it, since I mainly use Anthropic's models). But I do like its simplicity.

### OpenCode

I sometimes jump back into OpenCode whenever I want to test new LLMs using OpenRouter.

### Obsidian

This is the main note-taking app that I use. I think it's great because it's very lightweight, and I love the simplicity of just having markdown files, which I can carry over to any machine and which I'm sure will always be portable. I also love the fact that it comes with no subscriptions and no extra costs, and that it works offline. And I especially like the fact that there's no AI in it.

### Nvim

With the advent of AI agents, I believe that IDEs are now becoming less and less relevant. And since I've been working on remote machines, I think Neovim is now a must for me. It is simple, easy to configure, and very lightweight — it opens my projects almost instantly. Nowadays I mainly use it when reviewing code, or simply as a better Git diff viewer.

### Honorable mentions

- **Zed** — This was the first IDE that I really enjoyed using. I sometimes go back to it, but I stopped using it as I started to use TUI harnesses more and more. It is still a really good project, and I really recommend everyone to try it.

## Bringing it all together

So here's where the fun part begins. As I said before, I normally SSH into my remote machine with Zellij and start running various Claude Code sessions. I usually name each session based on what I'm doing in it, and I usually don't use multiple panes per tab — just one pane per tab. Sometimes I use two stacked panes: one for the Claude Code session and the other one for Neovim, checking the diff between branches.

I have a command that automatically SSHes into my default remote machine and attaches to the Zellij session. This really takes very few seconds — even less than a second to get connected and resume the Claude Code sessions. And when I'm done, I can even turn off my laptop and forget about it. Whenever I have to work at home, I can get back into my sessions almost instantly.

Having Neovim there is also very nice, because it means I never need to leave the terminal to review my code. I used to use Zed, which does have support for remote machines. However, I found it a bit frustrating to jump between it and the terminal. Even though I'm aware that I could have achieved everything in Zed, I found the Zellij setup much more lightweight and easier to reconnect — sometimes when Zed loses connection to the remote machine, it can take some time to reconnect.

## Recap

| Component | My pick | Why |
|-----------|---------|-----|
| Laptop | ASUS G14 | Performance and portability |
| Keyboard | Corne V4.1 | Small, split, fingers never move |
| Display | Ugreen AP16 | 2.5K/165Hz, well built, magnetic stand |
| Mouse | Logitech MX Master 3S | Ergonomics (when I need one at all) |
| OS | Arch Linux | AUR, few dependencies |
| Multiplexer | Zellij | Great defaults, survives disconnections |
| AI harness | Claude Code | Simple, works in the terminal |
| Editor | Neovim | Instant, lightweight, great diff viewer |
| Notes | Obsidian | Plain markdown, offline, no AI |

The setup boils down to this: the laptop is just a window into a remote machine, and everything I run there is portable, lightweight, and easy to run. If my laptop died tomorrow, I could be back to work from any machine in minutes — and that, more than any single component, is the whole point.
