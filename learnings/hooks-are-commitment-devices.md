---
title: Lifecycle hooks are commitment devices, not automations
date: 2026-04-29
source: McPhee dispatch on nouns-and-verbs
tags: [hooks, behavioral-design, decision-architecture, claude-code, brain-vault]
---

# Lifecycle hooks are commitment devices, not automations

## The Lesson

A lifecycle hook (SessionStart, Stop, PostToolUse, cron) is not primarily an automation. It is a **commitment device**: it relocates the decision point from "later, when I remember" to "right now, while the context is warm." The compounding effect of hooks does not come from them automating an action — most of them don't. It comes from them moving the moment-of-decision to when the cost of deciding is lowest and the value of what was just learned is highest.

## Context

McPhee surfaced this observation while writing *Nouns and Verbs* (2026-05-02 post on sethshoultes.com). The brief had described hooks as "the verbs that conjugate the nouns into a sentence" — the temporal-grammar argument. McPhee picked up the thread but landed somewhere different in the REPORT BACK:

> The Stop hook does not force the operator to save anything — the operator can ignore the prompt. But it changes the decision environment at the exact moment when the cost of saving is lowest and the value of what was just learned is highest. The compounding doesn't come from the hook automating the save. It comes from the hook restructuring *when the decision gets made*.

This generalizes beyond Claude Code hooks. Any system that fires a prompt at a specific moment in a workflow is doing the same thing: moving the decision point. Daily standup at 9am asks "what are you working on" before the day disperses your attention. A retrospective scheduled at the end of a sprint asks "what did we learn" before the lessons go cold. A commit-message hook asks "describe what you changed" before you've forgotten.

## What it means

The behavioral-economics frame names this as a **commitment point** or **choice architecture intervention**: the decision environment shapes the decision more than the decision-maker's intent does. A stack without hooks doesn't lack automation; it asks the operator to make the save-or-discard decision at the worst possible moment — after the lid is closed, the context is cold, and the work feels vague and past.

The hook does not save the note. It does not write the documentation. It does not commit the file. The operator does all of that. The hook just asks the question at the moment when the answer is freshest, and the operator's discipline-rate jumps from ~10% to ~70% as a structural consequence of the prompt's timing.

## How to Apply

- **When designing a tool system that compounds**: identify the temporal seams (start, end, cron, post-action) and ask "what decision could be made cheaply right now that would otherwise be made expensively later?" Hook the prompt to the seam.
- **When a stack of good tools isn't compounding**: the missing piece is usually not a tool. It's a hook that asks the operator to do something at the right moment. The save-to-vault prompt at session-end is the canonical example.
- **When evaluating a hook's value**: don't count what it automates. Count the % of the time the operator does the right thing WITH the hook firing vs. WITHOUT. The delta is the hook's value.
- **When tempted to automate the action instead of the decision**: pause. Forcing a save without operator consent is a different feature with different costs (storage bloat, signal/noise, false positives). The commitment-device version asks; the automation version assumes. Ask first.
- **When transferring this pattern outside of Claude Code**: the same logic applies to git commit hooks, CI/CD post-deploy notifications, weekly review prompts, end-of-month financial check-ins, the doctor's appointment-reminder text. They look like automation; they're really decision-point relocation.

## Related

- [[hooks-as-temporal-grammar-of-tool-systems]] — the structural argument; this learning is the behavioral-economics counterpart
- [[autonomous-claude-code-patterns]] — when you DO want automation rather than commitment-prompts
- [[generative-skills-must-persist-by-default]] — adjacent insight on default behavior shaping outcome
- The blog post that surfaced this: [Nouns and Verbs](https://sethshoultes.com/blog/nouns-and-verbs.html)
