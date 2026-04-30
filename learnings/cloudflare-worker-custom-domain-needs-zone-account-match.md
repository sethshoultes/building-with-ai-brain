---
title: Cloudflare Worker custom domain requires the zone and the worker on the same account
date: 2026-04-30
source: sethshoultes-mcp custom-domain attach
tags: [cloudflare, wrangler, dns, custom-domain, gotcha]
---

# Cloudflare Worker custom domain requires the zone and the worker on the same account

## The Lesson

To attach a custom domain (e.g. `mcp.sethshoultes.com`) to a Cloudflare Worker, the **zone** for the parent domain must live on the **same Cloudflare account** that the worker is being deployed under. If wrangler is logged into account A and the zone is on account B, the deploy fails with `Could not find zone for "<domain>". Make sure the domain is set up to be proxied by Cloudflare.` The error message implies a DNS misconfiguration; the actual problem is the account mismatch.

## Context

Building the `sethshoultes-mcp` worker. Wanted to attach `mcp.sethshoultes.com` as a custom domain via wrangler.toml:

```toml
routes = [
  { pattern = "mcp.sethshoultes.com", custom_domain = true, zone_name = "sethshoultes.com" }
]
```

Deploy failed with the zone-not-found error even though `dig NS sethshoultes.com` returned Cloudflare nameservers (proving the zone exists somewhere on Cloudflare).

The diagnostic was checking which accounts the wrangler OAuth token could see (`curl -H "Authorization: Bearer <token>" https://api.cloudflare.com/client/v4/accounts`) and then querying for the zone (`/zones?name=sethshoultes.com`). The first query returned two accounts; the second returned zero. The zone was on a third account the OAuth token didn't have membership in.

## The Fix

`npx wrangler logout` then `npx wrangler login`, this time with the email that owns the account holding the zone. Check via the Cloudflare dashboard top-right account selector to confirm which account is current. Then re-deploy.

Once the right account was logged in:
- `curl -H "Authorization: Bearer <new-token>" https://api.cloudflare.com/client/v4/zones?name=sethshoultes.com` returned the zone with its account_id.
- `npx wrangler deploy` succeeded; Cloudflare auto-created the DNS record (`mcp.sethshoultes.com → worker`) and provisioned the SSL cert in ~30 seconds.
- `curl -X POST https://mcp.sethshoultes.com/ -d '...'` worked immediately.

## How to Apply

- **Before configuring a custom domain on a worker**: confirm wrangler is logged into the account that holds the parent zone. `cat ~/Library/Preferences/.wrangler/config/default.toml` (macOS) shows the active OAuth token; query `/client/v4/accounts` and `/client/v4/zones?name=<domain>` to confirm the account matches.
- **When the zone-not-found error fires despite DNS pointing to Cloudflare**: don't debug DNS. Check the account.
- **When working across multiple Cloudflare accounts in one project**: write down which account holds which zone in the project's notes (or in a runbook). The accounts visible to wrangler change based on which OAuth token is active; the zones don't move when the login changes.
- **When deploying without custom domain**: the workers.dev URL works regardless of which account wrangler is logged into. The custom-domain attach is what introduces the account-zone-match requirement.

## Related

- [[cloudflare-525-zone-mismatch]] — different mismatch, same shape (Cloudflare's account-and-zone separation surfacing as a deploy error)
- [[mcp-discovery-loop-three-file-pattern]] — what this custom domain is for
- Runbook: [[Attach a Cloudflare Worker to a custom subdomain]]
