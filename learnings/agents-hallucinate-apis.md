---
title: Agents Hallucinate APIs
date: 2026-04-09
source: great-minds-plugin, shipyard-ai
tags: [ai, hallucination, api, documentation, critical]
---

# Agents Hallucinate APIs

## The Lesson
AI agents will write plausible-looking code against APIs that don't exist. They generate from training data, not from the actual source.

## Context
The Emdash EventDash plugin was 3,600 lines of code written against a completely hallucinated API. 121 `throw new Response()` calls, 14 `rc.user` references, `process.env` usage — none of which exist in Emdash's sandbox plugin system. Three other plugins had the same problem.

## The Fix
1. Write verified documentation (`docs/EMDASH-GUIDE.md`) by reading actual source code
2. Make doc-reading mandatory in pipeline prompts ("Read docs/ before writing code")
3. Create `BANNED-PATTERNS.md` with known-bad patterns that auto-fail QA
4. QA greps for banned patterns before code review

## How to Apply
Any time agents are building against a framework, CMS, or external API — verify the docs exist and are mandatory reading. Never trust model memory for API surfaces.

## Related
- [[autonomous-claude-code-patterns]]
- [[pipeline-is-the-product]]
- [[code-review-is-not-qa]]
- [[start-minimal-verify-expand]]
