---
title: Register ElevenLabs Client Tool via API
date: 2026-04-28
tags: [elevenlabs, voice-agents, runbook]
---

# Register ElevenLabs Client Tool via API

## When to use

You've defined a clientTool in the React component (e.g. `components/technician-call.tsx`) and the agent's system prompt references it, but the agent can't actually invoke it. ClientTools live in the browser; the ElevenLabs agent only knows about tools registered in its dashboard's tool registry. Two pieces of state that have to be aligned manually.

This runbook applies when adding a new browser-side tool that has no MCP handler. (For tools defined in `MCP_TOOLS`, use the existing `scripts/elevenlabs/sync-agent-config.ts --apply` instead.)

## Prerequisites

- [ ] `ELEVENLABS_API_KEY` in `~/.config/dev-secrets/secrets.env`
- [ ] Persona's agent ID known (`ELEVENLABS_AGENT_ID_<PERSONA>` in `.env.local` or pulled from `vercel env pull`)
- [ ] ClientTool implementation already lives in the React component
- [ ] System prompt has been updated to teach the agent when to call it

## Steps

### 1. Confirm the tool isn't already registered

```bash
set -a && source ~/.config/dev-secrets/secrets.env && set +a
AGENT_ID="agent_..." # from .env.local

curl -s -H "xi-api-key: $ELEVENLABS_API_KEY" \
  "https://api.elevenlabs.io/v1/convai/agents/$AGENT_ID" \
  | python3 -c "
import json, sys, urllib.request, os
d = json.load(sys.stdin)
ids = d['conversation_config']['agent']['prompt'].get('tool_ids', [])
key = os.environ['ELEVENLABS_API_KEY']
for tid in ids:
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/convai/tools/{tid}', headers={'xi-api-key': key})
    t = json.loads(urllib.request.urlopen(req).read())
    print(t['tool_config']['name'])
"
```

### 2. Write a one-shot registration script

Pattern: `scripts/elevenlabs/register-<name>-tool.ts`. Mirror `register-end-call-tool.ts` or `register-navigation-tools.ts` (in the GDS repo).

The tool_config shape ElevenLabs expects:

```ts
{
  type: 'client',
  name: 'myToolName',
  description: '... (when to call, what it does, what NOT to do)',
  response_timeout_secs: 5, // 10 for slow tools, 15 for retrieval
  disable_interruptions: false,
  force_pre_tool_speech: false,
  pre_tool_speech: 'auto',
  assignments: [],
  tool_call_sound: null,
  tool_call_sound_behavior: 'auto',
  tool_error_handling_mode: 'auto',
  parameters: {
    type: 'object',
    required: ['param1'],
    description: '',
    properties: {
      param1: {
        type: 'string',
        description: 'What this is for',
        enum: null,
        is_system_provided: false,
        dynamic_variable: '',
        constant_value: '',
      },
    },
  },
  expects_response: true,
  dynamic_variables: { dynamic_variable_placeholders: {} },
  execution_mode: 'immediate',
}
```

Two API calls in sequence:

- `POST /v1/convai/tools` with `{ tool_config: ... }` body → returns `{ id: 'tool_...' }`
- `PATCH /v1/convai/agents/<AGENT_ID>` with `{ conversation_config: { agent: { prompt: { tool_ids: [...existing, newId] } } } }`

**Critical**: PATCH must include the existing tool_ids unchanged. PATCH replaces the field; it doesn't merge. Read first, append, write.

### 3. Make the script idempotent

Re-running the script should not duplicate the tool. Check for an existing tool with the same name on the agent and exit early if found.

### 4. Run it

```bash
set -a && source ~/.config/dev-secrets/secrets.env && source .env.local && set +a
export ELEVENLABS_AGENT_ID_TECHNICIAN="agent_..."
npx tsx scripts/elevenlabs/register-<name>-tool.ts
```

### 5. Update the canonical list

Add the tool name to `lib/voice/agent-tools.ts` (the persona's tool list) so the verifier in `sync-agent-config.ts` knows it's expected. Otherwise it'll surface as "UNEXPECTED ON AGENT" on the next run.

### 6. Run the verifier

```bash
npx tsx scripts/elevenlabs/sync-agent-config.ts --persona <persona>
```

Expect: `[verify] <persona>: ✓ all tools accounted for`.

## Verify

- [ ] Curl the agent endpoint, confirm tool count went up by exactly 1
- [ ] Verifier reports clean
- [ ] Start a real voice call, ask the agent something that should trigger the tool, confirm the clientTool fires (browser DevTools network tab or React state changes)

## Notes

- Agent config changes are live immediately. No deploy needed (it's server-side ElevenLabs config, not your codebase).
- The 1.4-second pre-end delay used in `endCall` is empirical — gives a one-sentence farewell time to stream out before the WebRTC channel closes. Adjust if your tool needs longer.
- For tools the agent shouldn't actually call (mentioned in prompt for context only — like `visualDiagnose` triggered by a UI button), add the name to `PROMPT_ONLY_REFERENCES` in `lib/voice/agent-tools.ts` instead of registering it.

## Related

- [[ElevenLabs Custom LLM Tool Passthrough]] — server-side BYO-LLM proxy mechanics
- [[ElevenLabs dynamicVariables smuggling pattern]] — for threading session context to the agent
