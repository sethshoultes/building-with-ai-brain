---
title: GitHub Pages rebuild race breaks post-publish webhook workflows
date: 2026-04-28
source: sethshoultes.github.io sync-rag.yml workflow run 25084287967
tags: [github-actions, github-pages, ci-cd, race-condition, webhooks, rag, gotcha]
---

# GitHub Pages rebuild race breaks post-publish webhook workflows

## The Lesson

A GitHub Actions workflow that fires on `push` and calls a webhook to a service that **fetches the published page** (e.g. ElevenLabs Conversational AI's `POST /v1/convai/knowledge-base/url` for RAG ingestion, or any "give me this URL and I'll index it" endpoint) **will race the Pages build and fail on the first push**. The workflow runs ~5–10 seconds after `push` completes; GitHub Pages typically takes 30–90 seconds to rebuild and serve the new HTML. In that window, the URL the webhook is told to fetch returns 404 or stale content. ElevenLabs surfaces this as `ReadabilityError`. Other services may surface it as 404, 500, or "no content found."

Manual re-run from the Actions tab succeeds because by then the Pages build has finished.

## How it surfaced

Pushed four new posts to `sethshoultes.github.io` at 00:11 UTC. The `sync-rag.yml` workflow watches `_posts/**` and ran at 00:11:44, 6 seconds after `push` completed. The first URL it tried to register — `https://sethshoultes.com/blog/the-avatar-reads-first.html` — returned `HTTP 400` from ElevenLabs:

```json
{"detail":{"type":"invalid_request","code":"bad_request","message":"Error while running readability","status":"ReadabilityError"}}
```

curl-checking the same URL ~60 seconds later returned `200 OK`. Manually triggering the workflow at that point completed cleanly: 4 URL docs created, indexed, attached to the agent.

## Why it happens

GitHub Pages and GitHub Actions are separate subsystems. A `push` to a Pages-enabled repo triggers two parallel processes:

1. **Pages rebuild** — Jekyll runs, the new HTML is rendered, `_site/` is published to the CDN. Takes 30–90s for a small site.
2. **Actions workflow** — runners spin up, checkout, run jobs. Takes 10–60s for a small workflow.

The workflow doesn't wait for the rebuild. If the workflow needs the published page to exist, it has to wait or retry.

## Fix options (ranked by cost)

### 1. Trigger on `page_build` instead of `push`

GitHub fires a `page_build` event when Pages finishes rebuilding. This is the natively-correct trigger:

```yaml
on:
  page_build:
  workflow_dispatch:
```

**Tradeoff:** `page_build` fires on every Pages build, not just when `_posts/**` changed. The script needs to be defensive — it already is (idempotent: GETs the agent, diffs against the local post list, no-ops if nothing's new). So in practice this is the cleanest fix for a script that's already idempotent.

### 2. Add a polling loop to the workflow

Wait for the URL to respond 200 before calling the webhook:

```yaml
- name: Wait for Pages
  run: |
    until curl -sf -o /dev/null https://sethshoultes.com/blog/$(ls _posts/*.html | tail -1 | sed -E 's|.*[0-9]{4}-[0-9]{2}-[0-9]{2}-(.+)\.html|\1|').html; do
      sleep 5
    done
```

**Tradeoff:** Brittle — assumes you know which URL to poll, assumes the URL pattern. Works fine for a single-site setup like this one.

### 3. Retry-on-error in the script

Catch the readability error and retry with backoff. Cheapest in YAML, cleanest in Python:

```python
for attempt in range(6):
    try:
        resp = call("POST", "/v1/convai/knowledge-base/url", body)
        break
    except UpstreamError as e:
        if "ReadabilityError" in str(e) and attempt < 5:
            time.sleep(15 * (attempt + 1))  # 15, 30, 45, 60, 75s
            continue
        raise
```

**Tradeoff:** Retries cost real time. If the page legitimately can't be read (e.g. a placeholder error template), this will retry uselessly.

## Recommendation

For this project (sethshoultes.github.io), **switch to `on: page_build`**. The script is already idempotent and the trigger semantics are exactly right: "the page is now live, sync it." For other projects facing the same issue, pick (1) if the script is idempotent, (3) otherwise.

## How to apply

When wiring a workflow that calls an external service to ingest a published page:

1. Ask: does the service fetch the URL itself, or does it accept HTML in the request body? If it fetches, you have this race.
2. Prefer `on: page_build` over `on: push` for any workflow that depends on Pages output being live.
3. If you must use `on: push`, add a poll-for-200 step before the webhook call.
4. Make the script idempotent so manual re-runs are safe.

## Related

- [[autonomous-claude-code-patterns]] — same family of "the side-effect needs to wait for the deploy to land" issues
- ElevenLabs `POST /v1/convai/knowledge-base/url` returns `ReadabilityError` on 404/empty pages, not a clearer 404 — error surface is the gotcha that compounds the timing gotcha
