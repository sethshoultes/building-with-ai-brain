# Add a public MCP endpoint to a static site

## When to use

Standing up the agent-discovery loop on a static site (Jekyll, Hugo, 11ty, Next.js export, anything that publishes to GitHub Pages or similar). The result: an AI agent given the domain can fetch `/.well-known/mcp.json`, discover an endpoint, and enumerate the site's catalog with no credentials.

## Architecture

Three files, each doing one thing:

1. **Endpoint** — a Cloudflare Worker (or any HTTP service) that speaks JSON-RPC 2.0
2. **Formatter** — tool implementations inside the Worker that shape what the endpoint returns; they read from public sources only (the live site's published JSON, the GitHub API, etc.)
3. **Discovery file** — a static `.well-known/mcp.json` in the site repo, served by the static-site generator

## Prerequisites

- A Cloudflare account that holds the parent domain's zone (see [[cloudflare-worker-custom-domain-needs-zone-account-match]])
- Wrangler CLI logged into that account: `npx wrangler login`
- A public catalog the agent should be able to query (e.g., a Jekyll-generated `posts.json`)

## Steps

### 1. Stand up the Worker

```bash
mkdir -p ~/Local\ Sites/<your-domain>-mcp/src
cd ~/Local\ Sites/<your-domain>-mcp
```

Create `wrangler.toml`:

```toml
name = "<your-domain>-mcp"
main = "src/index.js"
compatibility_date = "2025-04-01"

routes = [
  { pattern = "mcp.<your-domain>", custom_domain = true, zone_name = "<your-domain>" }
]
```

Create `src/index.js` (skeleton — see `~/Local Sites/sethshoultes-mcp/src/index.js` for the full reference):

```js
const PROTOCOL_VERSION = "2025-06-18";
const SERVER_INFO = { name: "<site name>", version: "1.0.0" };
const TOOLS = [/* tool definitions with inputSchema */];

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

async function callTool(name, args) {
  // implement each tool; fetch from public sources only
}

export default {
  async fetch(request) {
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
    if (request.method !== "POST") return new Response("Method Not Allowed", { status: 405, headers: CORS });
    const req = await request.json();
    if (req.method === "initialize") return /* return protocolVersion, capabilities, serverInfo */;
    if (req.method === "tools/list") return /* return TOOLS */;
    if (req.method === "tools/call") return /* return callTool result */;
    return /* error -32601 */;
  }
};
```

Deploy: `npx wrangler deploy`. Cloudflare auto-creates the DNS record and SSL cert.

### 2. Implement the formatters

Each tool is a function in the Worker that fetches from a **public** source and returns JSON. Examples:

- `list_posts` → fetch `/posts.json` (or equivalent) from the live site, return as text
- `get_post` → fetch `/blog/<slug>.html` from the live site, return the HTML body
- `list_skills` → fetch from `https://api.github.com/repos/<org>/<repo>/contents/skills`

The wall is in the source, not in the response shaping. If the formatter cannot fetch admin data, it cannot leak admin data.

### 3. Smoke-test the endpoint

```bash
curl -X POST https://mcp.<your-domain>/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Expected: a JSON-RPC response with the `tools` array.

### 4. Configure the static site to serve `.well-known/`

For Jekyll, edit `_config.yml`:

```yaml
include:
  - .well-known
```

Other generators have similar config — Hugo's `staticDir`, 11ty's `addPassthroughCopy`, etc. The default for most generators is to drop dotfiles; the include is required.

### 5. Create the discovery file

Create `.well-known/mcp.json` in the site repo:

```json
{
  "name": "<site name>",
  "description": "<one-line description of the catalog>",
  "protocol": "mcp",
  "version": "2025-06-18",
  "endpoints": {
    "public": "https://mcp.<your-domain>/"
  },
  "auth_required": false,
  "transport": "http",
  "documentation": "https://<your-domain>/<post explaining the loop>.html"
}
```

### 6. Build, commit, push

```bash
git add _config.yml .well-known/mcp.json
git commit -m "Add public MCP discovery file"
git push
```

Wait for the static-site rebuild (~30-90s for GitHub Pages).

### 7. Verify the loop end-to-end

```bash
# Step 1: fetch the discovery file
curl https://<your-domain>/.well-known/mcp.json

# Step 2: extract the endpoint URL from the response, then call tools/list
curl -X POST <discovered-endpoint> \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Step 3: call a tool
curl -X POST <discovered-endpoint> \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_posts","arguments":{}}}'
```

If all three succeed without credentials, the loop is closed.

## Gotchas

- **Account mismatch on custom domain attach**: see [[cloudflare-worker-custom-domain-needs-zone-account-match]]. The zone must be on the same Cloudflare account wrangler is logged into.
- **Jekyll dropping `.well-known/`**: confirmed by checking `_site/.well-known/mcp.json` after `bundle exec jekyll build`. If the file isn't there, the `include` line is missing or misformatted.
- **CORS preflight on POST**: include `OPTIONS` handling in the Worker. Some clients fail the preflight silently if the Worker only accepts POST.
- **Forgetting to opt out of auth**: the discovery file's `auth_required: false` is the contract. If the endpoint is actually authenticated, the file lies, and clients will fail confused.
- **Edge caching too aggressively**: `Cache-Control: public, max-age=300` is reasonable for stable reads; less for catalogs that change daily. Don't cache so long that fresh content takes hours to surface.

## Related

- [[mcp-discovery-loop-three-file-pattern]] — the structural argument behind this runbook
- [[cloudflare-worker-custom-domain-needs-zone-account-match]] — the account gotcha
- Reference implementation: `~/Local Sites/sethshoultes-mcp/src/index.js`
- Reference discovery file: `~/sethshoultes.github.io/.well-known/mcp.json`
- The blog post: [Closing the Agent Discovery Loop](https://sethshoultes.com/blog/closing-the-agent-discovery-loop.html)
