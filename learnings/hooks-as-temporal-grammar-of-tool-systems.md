---
title: Lifecycle hooks are the grammar that turns a toolset into a system
date: 2026-04-29
source: King's "What's on the Desk" post — REPORT BACK observation, 2026-05-09
tags: [agent-systems, hooks, claude-code, grammar, system-design]
---

# Lifecycle hooks are the grammar that turns a toolset into a system

## The Lesson

In an agent-tooling stack — brain vault + Claude Code + Superpowers + Great Minds Constellation + skills repo — **the nouns and the verbs are different things, and a stack only becomes a system when it has both.** The vault, the skill packs, the persona plugins, the SOP library are nouns: objects on the desk, each well-shaped, each useful in isolation. They do not, by themselves, accumulate. **Lifecycle hooks (SessionStart, Stop, anything else the harness exposes) are verbs.** They create the temporal loop that turns the desk full of tools into a working system that gets denser with use.

Without the hooks: a session starts, the tools are present, the work happens, the session ends, the work is gone. Each context window is a first day on the job.

With the hooks: a session starts, the SessionStart hook surfaces yesterday's context. The work happens. The Stop hook prompts: *"Anything worth saving to the brain vault?"* The session ends having added something. The next session starts from a more advanced state than the one before. The compounding is **structural** — it happens whether or not the operator remembers to make it happen.

## Where this came from

King wrote *What's on the Desk* (2026-05-09) describing the four pieces of the operator's setup. The brief framed the hooks as one of the four pieces — useful, alongside the vault and the constellation and the skills. King's REPORT BACK observation reframed them as **a different category entirely**:

> "The vault, the Superpowers skills, and the constellation are nouns — objects on the desk. The Stop hook and the SessionStart hook are verbs. They create the temporal loop that turns a set of tools into a system that accumulates: session ends, learning saved, session begins, learning surfaced. Without the hooks, you have good tools that don't compound. With them, the compounding is structural — it happens whether or not you remember to make it happen. That's a different thing entirely, and it's the part that makes the desk feel like a desk you've worked at for a while rather than one you just walked up to. The briefer named the hooks as one of the four pieces, but framed them as 'context surfacing.' The deeper function is temporal binding — they're what makes the system a system rather than a collection."

Three claims worth pulling apart.

## The three claims

### 1. Tools are nouns; lifecycle hooks are verbs.

A vault is a thing. A skill is a thing. A plugin is a thing. None of them, by themselves, do anything across time. They sit there. The user has to invoke them.

A hook is not a thing. It is a moment plus an action. It executes whether or not anyone remembers it should execute. It only exists at session boundaries — but at those boundaries, it does something the static tools cannot.

This is the same distinction grammar makes about language: nouns name; verbs do. A sentence with only nouns is not a sentence.

### 2. Compounding without hooks requires discipline; with hooks, compounding is structural.

A vault that depends on the operator remembering to save accumulates only when the operator remembers. The discipline-to-do-this rate in practice is somewhere between 30–60% — most operators forget some of the time, fail to recognize what was worth saving the rest. The vault gains entries, but with gaps.

A vault wired to a Stop hook that prompts "Anything worth saving?" gains entries on every session-end with a non-trivial outcome. The discipline-to-do-this rate goes from variable to ~95%, because the prompt arrives at exactly the moment the work just happened — when the answer is fresh.

The vault's growth curve changes shape. It doesn't get *faster*; it gets *more reliable*. Reliability over time produces compounding that variability cannot.

### 3. The system-vs-collection distinction is a hook problem.

If you have a vault and a skill pack and a plugin marketplace, you have three good products. You do not have a system. The system is what emerges when those three products are wired into a temporal cycle that connects them. The wiring is hooks.

Stated as a test: **if the next session starts in the same state as the last one, you don't have a system; you have a collection of tools.** The next-session state being more advanced is the proof of system-ness.

## How to apply

When evaluating an agent-tooling setup — yours or someone else's — ask:

1. **What lifecycle hooks are wired?** SessionStart, Stop, PreToolUse, PostToolUse, anything else. List them.
2. **What does each hook do?** A hook that prints a message is doing presentation, not binding. A hook that runs a command which causes state to be saved/loaded is doing binding.
3. **Is there a closed loop?** Something saved at the end of session N should be readable at the start of session N+1. If the loop is open — saved but never surfaced, or surfaced but never saved — the system is half-built.
4. **What's the discipline tax?** A system whose compounding requires the operator to remember a specific action will compound less reliably than one whose compounding happens at hook-fired moments. Lower the tax; the structure does the work.

When designing one:

- **Always wire the Stop hook first.** It's the closing parenthesis. Nothing else compounds without it.
- **The SessionStart hook is the opening parenthesis.** Choose what it surfaces carefully — the operator sees that signal first every session.
- **Hook commands should be cheap.** A 5-second timeout is the standard. If the command takes longer, move it to background work that the hook only triggers.
- **Hook commands should be observable.** Failing silently is the hook's failure mode. Log to a file the operator checks occasionally.

## Why this is worth its own learning

The original learning ([[multi-agent-essay-production-recipe]]) named the hooks but framed them as "the prompt at session-end." This learning extends the framing one level up: the hooks are not just a useful UX detail; they are the architectural feature that makes the *whole stack* work as a stack. Same insight, deeper level.

Generalizes beyond Claude Code. Any agent-tooling system that wants to compound — Cursor, Codex, custom harnesses — needs the same lifecycle binding. Tools without hooks are products; products plus hooks are systems.

## Related

- [[multi-agent-essay-production-recipe]] — names the hooks; this learning extends the framing
- [[autonomous-claude-code-patterns]] — the broader pattern of agent systems that compound
- [[generative-skills-must-persist-by-default]] — same shape at the per-skill level (auto-save = a persistence "verb")
- *What's on the Desk* (King) — sethshoultes.com/blog/whats-on-the-desk.html — the post the observation came from
- ~/.claude/settings.json — where the SessionStart and Stop hooks are configured for this stack
