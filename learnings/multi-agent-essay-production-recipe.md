---
title: Multi-agent essay-with-image production recipe
date: 2026-04-29
source: Skills as SOPs blog post — sethshoultes.com/blog/skills-as-sops.html, commit 51049b6 → a2f21dc
tags: [orchestration, sub-agents, blog-post, production-recipe, great-authors, great-minds]
---

# Multi-agent essay-with-image production recipe

## The Lesson

The reproducible shape for a "ship a blog essay with original featured image in a single Claude Code session" is a four-layer assembly line, each layer a self-contained brief to a sub-agent in fresh context. The orchestrator never writes the prose, never designs the image, and never renders the pixels — it does briefs, integration, and commits. The pattern has now shipped six essays end-to-end (the four Agentic Economy / Avatar pieces, plus *Skills as SOPs* and the brain-vault recipe announcement context); each one followed the same recipe with different writers and different image metaphors. The shape generalizes; the content varies.

## The four layers

| Layer | Role | Who | What they receive | What they produce |
|---|---|---|---|---|
| 1 | **Briefer / orchestrator** | Claude Code (main session) | the user's seed (a sentence, a screenshot, a request) | a self-contained author brief, a self-contained image brief |
| 2 | **Author** | a `great-authors:<persona>` sub-agent in fresh context | the brief + 4–6 reference files to read first | the post body + front matter, saved to `_posts/YYYY-MM-DD-<slug>.html` |
| 3 | **Designer** | `great-minds:jony-ive-designer` (parallel with layer 2) | the post topic + the existing image register references | a single gpt-image-1 prompt, saved to a scratch file |
| 4 | **Renderer** | gpt-image-1 via OpenAI API | Ive's prompt | a 1536x1024 PNG saved to `blog/images/<slug>-featured.png` |

Layers 2 and 3 run in parallel. Layer 4 starts as soon as layer 3 returns. Layer 1 commits everything.

## The hidden prerequisite — claim, not topic

Surfaced by Vonnegut on the *Recipe That Wrote Itself* run (2026-04-29) as the unsolicited observation his REPORT BACK produced. **The recipe doesn't manufacture the argument. It manufactures the post around one.**

Six posts in the brain vault now, and in every case the briefer started with something that wanted to be argued — credential drift is dangerous, the orchestrator should not write, a skill inherits the correctness of its procedure. When the seed is a **claim**, the author can find the shape. When the seed is only a **topic** — "write about the recipe," "write about the avatar," "write about brain vaults" — the author has to invent the claim, and that's where dispatches go wrong.

**Diagnostic before dispatch:** can you state the seed in one sentence that contains a verb of argument? *"X is the next layer of Y"* (claim). *"How brain vaults work"* (topic — fail). If you only have a topic, spend 5 minutes turning it into a claim before writing the brief. The user's exact phrasing is usually the claim, sitting in their original message.

The recipe works because the user has done the hardest thinking before the brief gets written. The assembly line does not produce arguments. It produces posts around them.

## Briefing rules (what makes this work)

The orchestrator-and-writer learning was the foundation: the orchestrator must dispatch, not write. But dispatch quality is everything. Specifically what the *Skills as SOPs* run validated:

1. **Self-contained briefs.** Every author brief includes: the persona statement, the post material, READ FIRST list with absolute paths, output target path, length window, structural anchors as discretion-level beats (not hard outline), craft requirements, what NOT to do, and a REPORT BACK format. ~1,500 words of brief produces 1,300–1,800 words of post. Thin briefs produce thin work.

2. **READ FIRST is load-bearing.** Authors that read 4–6 prior posts before drafting produce voice continuity and avoid retreading. Skipping this step (or compressing it to "match the blog's voice") produces hollow imitation. The Bible Reads First — at the persona level.

3. **Structural anchors, not outlines.** "Open on a specific moment, not an abstraction" beats "Section 1: Introduction. Section 2: ..." Anchors leave room for the author to discover; outlines lock them into the briefer's mental shape.

4. **WHAT NOT TO DO is more important than what to do.** Each brief explicitly forbids: corporate plural ("we" unless you mean a team), exclamation marks, "I'm excited to announce," padding, summary closings. The negative space defines the voice as much as the positive guidance.

5. **REPORT BACK extracts the author's craft observation.** Asking the author to name "one observation about the topic you noticed during the writing that the briefer did not name" produces the best lines in every post. *Skills as SOPs* gained the line "a wrong skill executes the wrong thing in every session that calls it, without complaint, at full speed" because Orwell extended the analogy further than the briefer's caveat. Always include the report-back ask.

6. **Voice variation matters.** Each post in this run used a different author. The blog's range comes from the variety; if the same author writes too many pieces in a row the corpus flattens. Track which voice has been used recently; pick the freshest.

## Designer dispatch — what made Ive's briefs work

The image briefer (Jony Ive) gets a separate dispatch in parallel with the author. Three things matter:

1. **Reference images go in the brief.** The brief tells Ive to read the existing 5–7 featured images on disk so he matches the visual register (pen-and-ink, New Yorker, crosshatch, off-white). Without this step the designer drifts into generic "AI illustration."
2. **Possible directions, then "pick one."** The brief offers 3–4 candidate metaphors, then explicitly says "pick the strongest — your call." This produces stronger choices than "design something that captures X."
3. **The load-bearing visual.** Ive names, in one sentence, the single element that carries the post's idea. "The four paces of open space between the figure's outstretched hand and the back of the empty chair — that gap is the friction." That sentence is what makes the renderer's job tractable.

## The team that ships an essay

Per the *Skills as SOPs* run specifically — and per the recipe in general:

| Contributor | Role | Provides | Time |
|---|---|---|---|
| **User (the seed)** | Argument owner | The thesis, the screenshots, the seed phrasing | 30s of typing |
| **Claude orchestrator** | Briefer + integrator | Author brief, image brief, commits | 5–10 min of writing briefs |
| **Author persona** | Drafter | The post body in voice, in fresh context | 2–3 min of agent runtime |
| **Jony Ive** | Image briefer | The gpt-image-1 prompt | 1 min of agent runtime |
| **gpt-image-1** | Renderer | The PNG | 30–60s of API time |
| **HeyGen / Vercel agentskills.io** | Format reference | The structural template for cross-cutting artifacts | one-time install |

End-to-end: from "let's write a post about X" to a pushed commit with embedded image is 15–25 minutes of wall clock, ~5–10 of orchestrator-typing, the rest is parallel sub-agent runtime.

## How to apply

When the next post needs writing:

1. **Pick the freshest voice** — check `_posts/` for the last 3–4 author voices used; pick something different. Established roster: Hemingway, Wallace, McPhee, Didion, Le Guin, Orwell, Vonnegut, McCarthy, King, Morrison, Baldwin, Gottlieb (the editor — not for prose).
2. **Write the author brief** following the structure above. Spend the time. Include READ FIRST with absolute paths.
3. **Write the Ive brief** in parallel. Reference the existing featured images. Offer 3–4 candidate metaphors. Name the aspect ratio.
4. **Dispatch both in parallel** via the Agent tool with `run_in_background: true`. Don't wait sequentially.
5. **Render the image** via the gpt-image-1 helper as soon as Ive returns.
6. **Integrate**: image embed at top of post, front matter wired to related posts, build with Jekyll, verify, commit.
7. **Push** — the GitHub Action picks up the new post and syncs it to the avatar's RAG knowledge base.
8. **Save the author's REPORT BACK observation to the brain.** This is the step that closes the loop. Every author dispatch returns a "one observation about the topic you noticed during writing that the briefer did not name." That observation is *almost always* the load-bearing insight in the post. **Don't let it die in chat.** Either fold it into an existing brain learning that it extends, or create a new learning if it stands on its own. The recursion this enables: the recipe's diagnostic prompt produces the upgrades to the recipe. Without this step, the insight only lives in published prose and is hard to apply forward. Examples that produced this learning's own upgrades:
   - Vonnegut on *The Recipe That Wrote Itself* → "the seed must be a claim, not a topic" → folded into this learning's *hidden prerequisite* section.
   - King on *What's on the Desk* → "tools are nouns, hooks are verbs" → became its own learning at [[hooks-as-temporal-grammar-of-tool-systems]].

## Anti-patterns (don't do these)

- Don't have the orchestrator write the prose "to save a dispatch." The voice flattens. Per *[orchestrator-and-writer-are-different-ai-roles]*.
- Don't dispatch sequentially when you can parallelize. Author + designer run simultaneously.
- Don't skip the WHAT NOT TO DO section of the brief.
- Don't use the same author voice for three posts in a row.
- Don't let the orchestrator paraphrase the user's seed phrase. The user's exact words are usually the post's thesis; let the author find them on the READ FIRST list.

## Related

- [[orchestrator-and-writer-are-different-ai-roles]] — the foundation
- [[distinct-editor-personas-converge-on-real-craft-problems]] — multi-author dispatch as validation, same shape
- [[cross-model-persona-portability]] — same recipe portable across model orchestrators
- [[generative-skills-must-persist-by-default]] — auto-save behavior on author skills
- [[sub-agent-briefs-must-be-self-contained]] — the briefing-quality argument
- *Skills as SOPs* (Orwell) — sethshoultes.com/blog/skills-as-sops.html
- *Stars Aligned: The Writers Wrote the Engineers* (Le Guin) — recursive shape of the same recipe
- *Three Sessions Running* (McPhee) — the cross-model proof of the recipe
