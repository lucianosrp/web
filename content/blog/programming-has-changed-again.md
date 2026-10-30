---
title: Programming has changed (again)
date: 2026-10-30
draft: false
description: The developer is becoming an editor — some thoughts, following my appearance
  on the ExpressVPN Research Engineering Podcast, on how agentic coding is changing
  what programming means.
taxonomies:
  tags: [AI, Programming]
extra: {cover: /assets/img/programming-has-changed-again/cover.webp, cover_alt: 'Collage
    of me and Pete talking at the podcast mics, over code, film strips and scissors
    on orange shapes', cover_focus: west}
---

I always wanted to write about my thoughts on how the way we program has drastically changed in the past year.
This can be considered an extension of [episode #2 of the ExpressVPN Research Engineering Podcast](https://open.spotify.com/episode/6gMsXH0CLYiTqSDCKi3LZM), to which I was honored to be invited.

{{ <img src="/assets/img/programming-has-changed-again/expressvpn-podcast.webp" alt="Recording episode #2 of the ExpressVPN Research Engineering Podcast" /> }}

In this post, I am trying to put together some thoughts I have had over the past month. Giving them a consistent narrative was not easy, since the "narrative" itself on this topic has been changing rapidly — and I am not able to write about it as fast as I would like. 
Some parts of this post may be controversial and I accept that. I understand that people have different points of view and I'm happy to compare mine with others'. These are my own views at the time of writing, and they might change as things evolve. 

## Is the developer an editor? 
Programming has already evolved through several abstractions. Each abstraction removed manual work while increasing the amount of intent expressed.
Today, you can write some slim Python code without having to worry about memory management, compiling the code, etc. 
What else should we not worry about tomorrow? Would writing code still be a required thing? 

In this section I am going to talk about some reasons why I think we should be outsourcing most of today's (or yesterday's) developer's work to the latest Large Language Models — and why doing so doesn't make us less of a developer, but turns us into something closer to an editor: someone who stops writing every line and starts deciding which lines make the cut.

### Writing code is no longer where most value is created
What is an editor? The editor is not a proof-reader. When talking about "agentic coding" or "vibe coding" some people might see it in a negative way, seeing the "coder" as a low-skilled proof-reader that will just press "accept edits" for hours to then ship a half-baked product. When we look at "editors" in other fields, let's say in the movie industry, the role of the editor is an actual highly-skilled and respected profession. The editor is not shooting the scenes, the editor is not acting, the editor edits each scene and often decides which scene goes on and which scene gets discarded. You can have different versions of the same movie just by changing the edits. As I mentioned in the episode, the style of editing can even change the genre: the same footage can become a horror movie or an action movie, depending on how it's cut. Code works the same way now: an agent can give you multiple valid versions of the same feature, and your job is to pick the one that fits your design, your team and your users. The developer is now becoming an editor: each code block is no longer a polished ensemble of carefully human hand-written lines of code, but the result of an iterative session with one or more advanced agents. Of course, not every film is cut the same way. As I said in the episode, it depends on where your code sits between a hobby project and pacemaker firmware — the same spectrum [Theo Browne uses](https://youtu.be/434cG4g5KLE), going from a "slop website with one viewer" to code whose failure can kill someone. For critical code, you still want to own every single line, but I believe most of us sit much closer to the hobby end than we like to admit.

### The boring stuff still exists
While coding can be a gratifying exercise, there are still some tasks that can often be boring. For example, you are given an ad-hoc research task or analysis that would require a custom program. In the old days, you might need a few hours to put these ideas into code, run the code, find out that there are a few caveats that need to be considered, re-write parts of the code, re-run the code, get the output in place, write an email attaching the results and summarizing your process. Today, I can let an agent do this side-quest. The agent might go through the same "run the code, check mistakes and caveats and re-write the code" loop, but sometimes it won't: it gets it right on the first pass. Either way, that loop is no longer consuming *my* hours: while the agent grinds through it, I am free to work on something that actually needs me. My job in this side-quest is reduced to what it should have always been — checking that the results make sense and deciding what to do with them. And if the team then decides to go in a different direction, I have lost 20 minutes instead of 3 hours.

### Control the ideas, not the code
Letting the agent run the loop while I judge the result is, in a way, a small-scale version of what Antirez argues in his controversial post[^1], which I mostly agree with. If you haven't read it yet, I strongly suggest you do. I will not waste time rephrasing what the post already says. Instead, I will just mention the bits and concepts I find myself most in line with. 

> "You can now generate a lot of code [...] How are you supposed to review 5k lines of code every day?"

This is becoming more and more true every day. I just want to add that this extra code that gets generated doesn't necessarily need to be part of your core infrastructure. As [Theo Browne points out](https://youtu.be/434cG4g5KLE), we can now generate more testing code, more ad-hoc scripts to evaluate our ideas, or to test a specific edge case. With AI agents, we can now create ad-hoc environments to make our core code even more bullet-proof.

And generating all this extra code has never been cheaper. Most of us are using LLM subscriptions that give out tokens to use within a specific usage window (usually a 5-hour limit plus a weekly limit). For a 200 USD a month subscription, power users report getting anywhere from 1000 to 5000+ USD worth of API-equivalent tokens if they max out their usage (_tokenmaxing_).[^2] At that price, a throwaway script or an extra test suite costs next to nothing, and writing code we may never ship stops being a waste and becomes part of the process.

## What is left for us
If writing code is becoming this cheap and the developer is turning into an editor, why are so many developers still resisting it? I think we need to start accepting the fact that frontier-level Large Language Models generally write better code than the average programmer. While talking with developers here in Hong Kong, I can clearly see that, for many, it is very hard to accept that they are average (myself included) — most seem to see themselves above it. Many developers tell me, "Well, I believe these models are great, but they are not so good for what I do", which could arguably be the case, but it is strange that so many developers are ready to say so. In a room full of developers, I would expect maybe 10% of them to be exceptionally skilled and doing very specific work that modern AI can't really help with, but, from what I see, it is actually about 60% of the developers I meet who claim they just can't use it for their work! Either I keep meeting above-average programmers or not everyone is being honest about the capabilities of the latest models. I also feel this way because many highly-skilled programmers I follow have already taken the AI pill, like Salvatore Sanfilippo (a.k.a. Antirez), the creator of Redis (whom I mentioned earlier)[^3], David Heinemeier Hansson (a.k.a. DHH), the creator of Ruby on Rails and Basecamp, who went from feeling "competence draining out of my fingers"[^4] to finding hand-typed syntax "a tedious chore"[^5], to declaring himself "optional in the part that produces the code"[^6][^7] and going "pencils down" on handwritten code altogether[^8], or even Linus Torvalds himself (although not fully AI-pilled, he vibe-coded part of a hobby project and pushed back against making the kernel docs take an explicit stance on AI)[^9].

It is also worth noting that model capabilities are not everything. The way we interact with agents is probably equally important and, in some cases, even more so. It requires a different way of working which not everyone has properly figured out yet, and I think this is why those who are not fully on board with "agentic coding" are not able to fully migrate their setup. Sometimes this is due to personal preferences, but it can also be due to team or company policies. Luckily for me, I managed to tune my programming routine many times until "it just feels right" — not everyone has the ability or patience to do so.

<aside class="post-update post-update--update">
<p class="post-update-label">// update · 27 September 2026, just before publishing</p>

While this post was waiting to go out, Antirez posted something that explains the puzzle I described above, why so many developers say these models don't work for them, better than I could[^10]:
> "Good programmers state they use models like GPT 6 Astra without obtaining good results: it makes me feel I live in a parallel universe. But the explanation is not that hard: good programming in the past and now requires a different skill set, even if there is some overlap."

</aside>

With today's models, is it possible to one-shot a project or feature and get something that works perfectly on the first run? Most of the time, it is not. This is why the role of the editor is to steer the agent, so that after a few iterations the feature is implemented with the same quality (or better) as if a human had written it from scratch. But models get better with every new release, and the need to steer and iterate on a feature keeps shrinking. For smaller features or bug fixes, I often find myself accepting the first solution the LLM suggests, provided it doesn't affect the rest of the code base. Some people have already gone a step further: instead of editing the output of one agent, they orchestrate a whole swarm of them on a complex problem or feature, and that is where those subscription limits start to matter. Either way, the human is still the one deciding what makes the final cut. And whoever makes the final cut also owns it: if something breaks in production, nobody is going to blame Anthropic. As Pete put it on the podcast, we should delegate, not abdicate.

This is not the end for us developers. It is rather just the beginning of an exciting new way of working.
And for most of us, this is also an incredible learning opportunity: in the past months alone, I have built many complex projects and ideas that I don't think I would have been able to build without the brilliant assistance of Claude Fable. When working with agents, you don't have to just sit back and watch. You can take the opportunity to ask questions, for example: "Why did you decide to implement it this way? What if we did it that way instead?" The same goes for getting to know someone else's code: instead of a two-hour session with a colleague, I can spend 30 minutes with an agent that has the whole repository in context, while my colleague keeps working on something else. I have also finally had the time to go down various rabbit holes, some of which never led to a final merge. But I still enjoy exploring these multiple "what if" paths and learning new things along the way. I am less sure about one kind of learning, though: I learned a lot of Rust by fighting the compiler, and if the agent is the one compiling, I'm not sure I would learn it the same way today. Much of the code my agents write will never get merged at all. Some people might think this is inefficient, but code is now the cheap part, and I actually think it's very important: for every line that goes into production, there are hundreds of lines of tests and discussions between multiple AI experts with different points of view, considering and reconsidering the possible implementations. And behind every discarded line, there are valuable lessons that we often fail to recognize.

Just like in a film, the scenes that end up on the cutting-room floor are part of what makes the final cut good. Programming has climbed yet another step on the abstraction ladder: we went from managing memory by hand to letting Python do it, and now from writing every line to deciding which lines deserve to stay. It has changed again, and it will change again. Change is rarely comfortable, but I am sure we will look back at this era as one of the most exciting transitions our profession has ever gone through.

[^1]: [antirez — Control the ideas, not the code](https://antirez.com/news/169)
[^2]: See [CloudZero's Claude pricing breakdown](https://www.cloudzero.com/blog/claude-pricing/) and [this Max vs API cost comparison](https://help.apiyi.com/en/claude-max-vs-api-pay-per-use-pricing-comparison-claude-code-savings-guide-en.html) — one reported case: 10B tokens over 8 months, ~15,000 USD API-equivalent, on a 100 USD/month plan.
[^3]: [antirez — Don't fall into the anti-AI hype](https://antirez.com/news/158)
[^4]: [Lex Fridman Podcast #474 — DHH: Future of Programming, AI, Ruby on Rails, Productivity & Parenting](https://lexfridman.com/dhh-david-heinemeier-hansson/) (July 2025)
[^5]: [Gergely Orosz — DHH's new way of writing code](https://newsletter.pragmaticengineer.com/p/dhhs-new-way-of-writing-code)
[^6]: [Lex Fridman Podcast #501 — DHH: Future of Programming, AI, Agentic Engineering, Vibe Coding & Linux](https://lexfridman.com/dhh-2/) (August 2026)
[^7]: [DHH on X: "now it's time for you to revisit your priors"](https://x.com/dhh/status/2093269782527144223)
[^8]: [DHH's Rails World 2026 keynote](https://youtu.be/vDjW_dRyKXY), via [@rails on X](https://x.com/rails/status/2102934006094508482)
[^9]: [The Register — Linus: Stop making issue of AI slop in kernel docs](https://www.theregister.com/software/2026/01/08/linus-stop-making-issue-of-ai-slop-in-kernel-docs/4519589)
[^10]: [antirez on X, 27 September 2026](https://x.com/antirez/status/2104130171305680972)
