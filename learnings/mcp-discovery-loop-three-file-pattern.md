---
title: MCP discovery loop — the three-file pattern (static-site adaptation)
date: 2026-04-30
source: sethshoultes.com — Closing the Agent Discovery Loop
tags: [mcp, agent-discovery, well-known, jekyll, cloudflare-workers, public-api]
---

# MCP discovery loop — the three-file pattern (static-site adaptation)

## The Lesson

Closing the agent discovery loop on a static site requires three files. Each does one thing. All three are required. The loop is the agent fetching `/.well-known/mcp.json` → discovering an endpoint URL → calling JSON-RPC `tools/list` against that endpoint with no credentials. Skip any step and the loop is open.

The original three-file pattern was implemented for a WordPress/MemberPress commerce surface. Same logical structure applies to a static Jekyll site, with different mechanics:

| Role | WordPress (MemberPress) | Static (Jekyll + Cloudflare Worker) |
|---|---|---|
| **Endpoint** | `PublicServer.php` registered with WP REST API at a public route | Cloudflare Worker on a custom subdomain (`mcp.sethshoultes.com`) |
| **Formatter** | `MembershipFormatter::public_detail()` — wall between public and admin data | Tool implementations inside the Worker (`list_posts`, `get_post`, `list_skills`) — same wall, different language |
| **Discovery file** | `Auth::handle_well_known()` — serves the JSON dynamically based on toggle | Static `.well-known/mcp.json` file in the repo, served by Jekyll |

## Context

Shipped on sethshoultes.com 2026-04-29. The site already had a public corpus (blog posts, brain learnings, installable Skills) but no agent-discoverable surface. An AI client given the domain had no path from "I know about this site" to "I have structured catalog data I can reason from." The loop was open at every step.

The fix was three pieces:

1. **Cloudflare Worker** — `sethshoultes-mcp` worker, single-purpose, JSON-RPC 2.0 at the root path. `initialize`, `tools/list`, `tools/call`. Permissive CORS. Edge-cached for 5 minutes per response.
2. **Tool implementations as formatters** — `list_posts` reads `/talk/posts.json` (the existing Jekyll-generated catalog), `get_post` fetches the live post HTML by slug, `list_skills` queries the public GitHub API for the `building-with-ai-skills` repo. None of these formatters can leak anything that isn't already public, because they don't have access to anything that isn't already public. The wall is in the data sources, not in the response shaping.
3. **Static discovery file** — `.well-known/mcp.json` in the site repo, with `_config.yml` `include: [.well-known]` so Jekyll doesn't drop the dotted directory at build time.

## What it means

The pattern is portable. Any static-site stack that can serve a JSON file at `/.well-known/` and call out to a separate endpoint can ship the same triple. The worker doesn't have to be Cloudflare; the formatter doesn't have to be JavaScript; the discovery file doesn't have to be Jekyll-served. What matters is that all three exist, each does its single job, and the default for the discovery file is "doesn't exist" until the operator explicitly creates it.

The static-site equivalent of the WordPress "default off toggle" is the file's existence itself. No file → 404 → agent moves on. No special opt-in UI required; the act of authoring the file IS the opt-in.

## How to Apply

- **When standing up an MCP layer for any public site**: identify the three roles (endpoint, formatter, discovery file) and confirm each is filled by exactly one piece. If two of them are merged, you have a bug waiting to surface; if one is missing, the loop doesn't close.
- **When the formatter and the data source are the same code**: that's a smell. The formatter should be unable to leak admin data because it can't see admin data. If the formatter is choosing what to redact at response time, the wall is in the wrong place.
- **When the discovery file is dynamically generated**: confirm the "off" state returns 404, not a JSON blob announcing "authentication required." Off should be indistinguishable from "this site doesn't speak MCP."
- **When the operator wants to test the loop end-to-end**: `curl https://<domain>/.well-known/mcp.json` for the discovery file, then `curl -X POST <discovered-endpoint> -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'` for the endpoint. Both should succeed without auth.
- **When extending the corpus an agent can see**: add a tool function in the worker. The discovery file doesn't need to change — agents call `tools/list` to enumerate.

## Related

- [[hooks-as-temporal-grammar-of-tool-systems]] — the verbs that make this kind of stack accumulate
- [[github-pages-rebuild-race-breaks-post-publish-webhooks]] — same kind of static-site/serverless seam, different surface
- [[liteavatar-sdk-no-client-user-message]] — co-thread post; the SDK has shape, the platform has shape; the discovery loop lives one layer up
- The blog post: [Closing the Agent Discovery Loop](https://sethshoultes.com/blog/closing-the-agent-discovery-loop.html)
- Runbook: [[Add a public MCP endpoint to a static site]]
