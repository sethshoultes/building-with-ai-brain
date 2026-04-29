---
title: Orchestrator and Writer Are Different AI Roles
date: 2026-04-25
source: great-authors plugin novel-writing session (Murder on the Arizona Strip)
tags: [ai-agents, sub-agents, orchestration, writing, claude-code, plugin-design, great-authors]
---

# Orchestrator and Writer Are Different AI Roles

## The Lesson

When an AI is running a project that uses persona sub-agents (writers, designers, reviewers), the AI's role is *orchestrator* — coordinating the work of the sub-agents — not *writer* itself. Confusing the two roles produces mechanical output, because the orchestrator's brain is in coordination mode (routing, briefing, integrating), not in creation mode (inhabiting voice, finding scene). The fix is *always* to dispatch the sub-agent rather than do the work yourself.

## Context

In a session writing a 17,500-word novel (`Murder on the Arizona Strip`) using the `great-authors` plugin, I (Claude as main agent) wrote chapters 5–8 in-context, pattern-matching King's voice from his earlier work in the project. The result read mechanical. The user named it: *"those chapters you wrote are terrible and sound overly robotic. you should be using the authors to write and review not you. you need to orchestrate the sub agent authors."*

The corrective dispatch — King persona as a sub-agent (`subagent_type: great-authors:king-persona`) with a self-contained brief — produced demonstrably better prose for the same chapters. Same persona file, same architecture, same bible. The difference was *who was holding the context.* When King's persona is the foreground of a fresh sub-agent context, the voice emerges. When I (the orchestrator) try to filter the persona through my coordination context, the voice is hollow.

## The Fix

Codify the role distinction at multiple levels:

1. **Project-level CLAUDE.md** — a project bible file (auto-loaded at session start) that explicitly tells Claude *for this project, you are the orchestrator, not the writer.* Prevents the failure mode at the start of every session.

2. **A formal orchestrator persona** (Gottlieb, in this case — modeled on Robert Gottlieb the editor) that can be channeled when the user wants the orchestrator role formalized in conversation.

3. **A formal `/authors-rewrite` skill** that handles the dispatch automatically, so the orchestrator's only decision is *which author?* — not *how do I construct the brief?*

4. **Auto-save by default** for any skill whose deliverable is the artifact (prose, code, doc). Orchestrators forget to save; defaults shouldn't depend on memory.

5. **An `ORCHESTRATING.md`** at the plugin root explaining the role, the seven skills by use case, and what NOT to do (the most important section).

## How to Apply

### When you find yourself reaching for the Write tool to produce prose…

Stop. Ask: have I dispatched the writer for this? If not, that's the next move.

The narrow exceptions where the orchestrator may produce prose:

- **Mechanical edits** — surgical fixes (typo, name continuity, count adjustment). These are integration, not creation.
- **Explicit user request** — *"just write me a paragraph here."* Honor that.

### When briefing a sub-agent…

A self-contained brief is the orchestrator's leverage. Include:

- Which files to read in what order (with absolute paths, since sub-agents inherit cwd but may not be in the project root)
- Architecture beats that must land
- Voice rules to hold (and any to relax)
- Length expectations
- One concrete craft challenge specific to this work
- What to leave alone
- Where to save the output
- Reporting format

Thin briefs ("rewrite this") produce thin work. Spend the time on the brief.

### When deciding between critique and rewrite…

These are not interchangeable:

- **Critique** is for prose that mostly works. Surface specific problems, recommend specific cuts. The writer's prose stays; the orchestrator integrates the cuts.
- **Rewrite** is for prose that doesn't work. Cutting bad prose tighter does not make it good. Discard and dispatch.

If you cannot tell which the work needs, run a critique pass first. The verdict will tell you.

## Why This Matters Beyond Novel-Writing

This pattern generalizes to any AI agent system using personas as sub-agents:

- Code generation (general agent orchestrating language-specific or framework-specific specialists)
- Design review (orchestrator dispatching brand voice, accessibility, technical critics)
- Documentation (orchestrator dispatching style, accuracy, audience-fit reviewers)

The mistake — orchestrator drifting into doing the work themselves — produces homogenized output that pattern-matches the surface of the specialist's domain without the substance. The fix is always the same: dispatch.

## Related
- [[dispatching-subagents-from-claude-cli]]
- [[persona-plugin-vs-infrastructure]]
- [[autonomous-novel-orchestration]]
- [[orchestrator-not-channel]]

- [[generative-skills-must-persist-by-default]] — adjacent learning from the same session about defaults for output persistence
- [[orchestrating-author-sub-agents]] — runbook companion to this learning
- [[draft-a-novel-with-great-authors]] — earlier runbook from the same project
