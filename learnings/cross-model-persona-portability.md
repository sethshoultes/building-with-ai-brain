---
title: Cross-Model Persona Portability — the Agent Dispatch Protocol Is the Contract
date: 2026-04-28
source: kimi-k2.6:cloud orchestration of the book-proposal recipe in ~/Local Sites/murder-on-the-arizona-strip-2
tags: [great-minds-constellation, claude-code, cross-model, kimi-k2.6, agent-protocol, recipe-portability]
---

# Cross-Model Persona Portability — the Agent Dispatch Protocol Is the Contract

## The Lesson

The Great Minds Constellation is not Claude-locked at the persona level. The contract that makes the persona pipeline work is the **Agent dispatch protocol** — the discipline of dispatching a `<plugin>:<persona>` sub-agent with a self-contained brief, having it read the project bible in fresh context, and writing its output to a deterministic path. The underlying model running the orchestrator is portable.

Empirical proof: a Kimi K2.6:cloud session in `~/Local Sites/murder-on-the-arizona-strip-2` ran the book-proposal recipe end-to-end. It dispatched `great-authors:mccarthy-persona` (sample chapter), `great-authors:gottlieb-persona` (chapter outline), and `great-minds:maya-angelou-writer` (pitch copy) in parallel. Cross-plugin routing worked. The personas read the bible and wrote where expected. The Plan → Build → QA → Review pipeline shape held — same as recipe #1 — with a publisher-readiness layer added.

## Why this matters

The constellation looks Claude-Code-coupled because it ships *as* a Claude Code plugin marketplace. But the marketplace is the distribution; the runtime is the model + harness running the dispatch. A non-Anthropic model running through Claude Code's Agent tool can drive the same persona pipeline that an Opus session would.

This means recipes (book-proposal, video-pipeline, etc.) are portable across model choices. Use Opus when the orchestrator's reasoning bandwidth is load-bearing; use Kimi K2.6 or another cheaper model when the orchestrator is mostly routing and the heavy lifting happens inside the persona sub-agents.

## What's still Claude-Code-coupled (caveat)

Some pieces of the experience depend on Claude Code specifically:

- The Agent tool itself (other CLIs may not expose `subagent_type` cleanly).
- The plugin marketplace + per-project enablement in `.claude/settings.json`.
- The `/team-build` and other slash skills — they live as Claude Code skills.

What's *not* coupled:

- The persona files (markdown).
- The bible at `.great-authors/`.
- The dispatch-and-read-first pattern.
- The output-to-deterministic-path discipline.
- The Plan → Build → QA → Review pipeline shape.

When porting the constellation to a different agent runtime, the persona pipeline carries; the harness-specific glue does not.

## How to apply

- **When billing matters**, pick the model based on what the orchestrator is doing. Routing-heavy work (dispatching 4 sub-agents in parallel, integrating their outputs) does not need Opus; Kimi K2.6 or Sonnet handle it.
- **When documenting recipes**, distinguish in the README between protocol-level requirements (`Agent` dispatch, persona files, bible structure) and harness-level requirements (Claude Code's marketplace, settings.json enablement). Future-you porting to a different runtime will read this distinction first.
- **When a plugin isn't loaded**, the orchestrator can pinch-hit by absorbing the persona's job directly — e.g., the `great-researchers` plugin not being loaded meant the orchestrator did Caro's research synthesis itself, with a `Researcher: Robert Caro (substituted: direct web research + synthesis)` byline. The recipe still ran; the substitution got noted for the case study.

## Related

- [[orchestrator-and-writer-are-different-ai-roles]] — the role-distinction this protocol depends on
- [[plugin-ships-prompts-project-ships-renders]] — sister architectural lesson about what the plugin owns vs. what the project owns
- [[distinct-editor-personas-converge-on-real-craft-problems]] — multi-editor convergence as validation, observed under the same protocol
- great-minds-constellation README — https://github.com/sethshoultes/great-minds-constellation
