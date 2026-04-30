# Attach a Cloudflare Worker to a custom subdomain

## When to use

Replacing a Worker's default `*.workers.dev` URL with a clean subdomain on a domain you own (e.g. `mcp.example.com` instead of `example-mcp.you-account.workers.dev`). One-time configuration; Cloudflare handles DNS and SSL automatically.

## Prerequisites

- The parent domain's zone is on Cloudflare DNS (`dig NS <domain>` returns nameservers ending in `cloudflare.com`)
- The zone is on the **same Cloudflare account** the Worker will be deployed to (this is the load-bearing requirement — see Gotchas)
- Wrangler CLI logged into that account: `npx wrangler login`

## Steps

### 1. Confirm the zone and account match

```bash
# Get the wrangler OAuth token
TOKEN=$(grep '^oauth_token' "$HOME/Library/Preferences/.wrangler/config/default.toml" | cut -d'"' -f2)

# List accounts the token can see
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('\n'.join(f\"{a['id']}  {a['name']}\" for a in d['result']))"

# Confirm the zone is on one of those accounts
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/zones?name=<your-domain>" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); [print(f\"zone={z['id']}  account={z['account']['id']} ({z['account']['name']})\") for z in d['result']]"
```

If the zone query returns 0 results, wrangler is logged into the wrong account. `npx wrangler logout && npx wrangler login`, this time with the email that owns the right account, then re-run.

### 2. Add the route to wrangler.toml

```toml
routes = [
  { pattern = "mcp.<your-domain>", custom_domain = true, zone_name = "<your-domain>" }
]
```

The `custom_domain = true` flag tells Cloudflare to:
- Auto-create the DNS record pointing the subdomain at the Worker
- Provision an SSL certificate (~30 seconds via DNS-01)
- Route all traffic for that hostname to this Worker

The `zone_name` is required when the route's hostname doesn't match a zone you can attach to via the route pattern alone (Cloudflare needs the explicit hint).

### 3. Deploy

```bash
cd ~/Local\ Sites/<worker-dir>
npx wrangler deploy
```

Output should include:

```
  mcp.<your-domain> (custom domain - zone name: <your-domain>)
```

### 4. Wait for SSL provisioning, then test

SSL takes ~15-30 seconds. After that:

```bash
curl https://mcp.<your-domain>/
```

If you get a TLS error, wait another 30 seconds and retry. If you still get TLS errors after 2 minutes, check the Cloudflare dashboard → the worker → Settings → Domains & Routes for any provisioning error.

## Gotchas

- **`Could not find zone for "<domain>". Make sure the domain is set up to be proxied by Cloudflare.`** — this misleading error doesn't mean the DNS is wrong. It means wrangler is logged into a different account than the one holding the zone. Logout/login fix; see [[cloudflare-worker-custom-domain-needs-zone-account-match]].
- **Orphan worker on the wrong account**: if you deployed once to the wrong account (without the custom domain), the worker exists there too at the workers.dev URL. To clean up: `npx wrangler logout && npx wrangler login` to that account, then `npx wrangler delete <worker-name>` from the worker dir.
- **DNS propagation**: not an issue with Cloudflare-managed zones (changes are instant globally). It IS an issue if the zone is on a third-party DNS provider — in which case you can't use `custom_domain = true` at all; use `routes` with explicit DNS records you maintain manually.
- **Forgetting `compatibility_date`**: required in wrangler.toml for new workers. Use a recent date (e.g., `compatibility_date = "2025-04-01"`).
- **Multiple workers on one subdomain**: Cloudflare allows it via routes (different paths to different workers), but `custom_domain = true` claims the entire hostname. If you need path-based routing, drop `custom_domain` and use `pattern = "mcp.<domain>/api/*"` style.

## Related

- [[cloudflare-worker-custom-domain-needs-zone-account-match]] — the account-mismatch learning
- Cloudflare docs: https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
- Reference: `~/Local Sites/sethshoultes-mcp/wrangler.toml`
