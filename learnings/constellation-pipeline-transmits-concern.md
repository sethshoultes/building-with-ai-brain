---
title: The Constellation Pipeline Transmits Concern, Not Just Artifacts
date: 2026-04-28
source: regex-explainer recipe #1, end-to-end run (cookbook recipe shipped)
tags: [great-minds, constellation, agency, multi-agent, qa, discovery, validation]
---

# The Constellation Pipeline Transmits Concern, Not Just Artifacts

## The Lesson

When discovery surfaces a load-bearing concern and that concern is wired explicitly into downstream phase briefs, the pipeline transmits the concern across phases — and the concern catches real bugs at QA that a smell-test pass would never find. The agency works as a system not because it produces artifacts, but because its phases pass *worry* to each other.

This is the load-bearing claim of the multi-phase agency pattern. Without it, the constellation is just a sequence of personas. With it, the constellation is a pipeline that compounds discovery insight into shipped quality.

## Context

Recipe #1 (regex-explainer) ran the full Great Minds pipeline end-to-end on a real customer brief. Sara Blakely's discovery surfaced one specific concern, repeatedly, in different framings:

> *"Wrong explanations, confidently delivered, are worse than no explanation. His junior devs will trust them. That trust is the whole product, and it is also the whole risk."*

That concern got carried into the operator's QA brief for Margaret Hamilton — explicitly. Margaret's QA brief said:

> *"The sharpest failure mode Sara named in discovery — wrong-but-confident explanations. If you find any pattern where the prose is technically wrong, that's a P0."*

Margaret then found two P0 bugs that match the failure mode exactly:

- **P0-1**: Named-group lookup in the test panel produced wrong group names when two groups captured identical strings (`foo-foo` → second group inherited first group's name). Confidently wrong output.
- **P0-2**: Quantified lookarounds like `(?=foo)+` produced prose claiming "repeated one or more times" — but lookarounds are zero-width; the quantifier is meaningless. Confidently wrong output.

Neither bug would have been caught by the smoke test (Sam's email pattern + Phil's smell-test pattern both pass cleanly without exercising these failure modes). Margaret found them because she was looking for the failure mode Sara named.

## Why This Matters

A common failure mode of multi-agent pipelines is that each phase produces an artifact and hands it to the next phase, but the *reasoning* — the worry, the open question, the load-bearing concern — gets dropped at the boundary. Each phase starts from the artifact and re-derives whatever it cares about.

The constellation works *better* than that when the operator carries discovery's concern into downstream briefs explicitly. The QA persona doesn't have to re-derive Sara's failure-mode worry; it inherits it as a search lens.

The agency claim is real: the pipeline doesn't just sequence personas, it compounds insight.

## How to Apply

### Carry concerns forward in briefs, not just artifacts

When dispatching a downstream persona (Phil, Margaret, Steve), include a direct quote or paraphrase of the load-bearing concern from earlier phases. Example QA brief stanza:

```
Sara's discovery surfaced this load-bearing concern: "[exact quote]"
This is the failure mode you're testing for. Anything matching this pattern is a P0.
```

The persona then reads through that lens — they're not re-deriving the concern, they're searching for instances of it.

### Pick concerns that are crisp and named

Sara's concern landed because it was crisp ("wrong-but-confident explanations are the worst failure mode") and named (the failure mode has a name). Vague worries don't transmit. "This might have edge cases" doesn't help Margaret. "Confidently wrong output is a P0" does.

If discovery returns vague worries, push back at the operator-decision point: name the worry crisply before dispatching debate.

### Use convergence as confirmation

If Margaret finds bugs that match Sara's stated worry, the pipeline worked. If Margaret finds bugs that *don't* match — different failure mode — the pipeline missed something. That's signal: discovery may have had blind spots, or QA may have a stronger lens than discovery did.

For recipe runs, log both kinds in the retro:
- **Concerns that transmitted and caught bugs**: confirms pipeline integrity
- **Bugs caught that no upstream concern predicted**: signals upstream gap

### Don't expect bug-free smoke tests

The smell test catches the *easy* case. The hard cases — the ones that match Sara's worry but live outside the smell-test's path — only show up under Margaret's QA. If the smoke test is green, that's not "ready to ship." That's "ready to give to QA."

## The Pattern

```
Discovery: "X is the worst failure mode"
   ↓ [carry the concern forward in brief text, not just artifacts]
QA brief: "Test for X. Anything matching X is P0."
   ↓
QA finds bugs that match X
   ↓
Confirms pipeline worked AND ships better quality than the smoke test alone
```

```
[Failure case]
Discovery: "X is the worst failure mode"
   ↓ [concern dropped at brief boundary]
QA brief: generic test list, no failure-mode lens
   ↓
QA finds typos, misses X-class bugs
   ↓
Bugs matching X ship to customer
```

## Related

- [[code-review-is-not-qa]] — QA needs runtime testing, not just source review (precondition for this lesson — the QA persona has to actually use the tool to find concern-matching bugs)
- [[distinct-editor-personas-converge-on-real-craft-problems]] — multi-persona convergence as validation (sibling pattern: convergence across personas vs. concern-transmission across phases)
- [[agency-operator-must-redirect-not-pinch-hit]] — the operator's role in the pipeline is structural, not pinch-hit
