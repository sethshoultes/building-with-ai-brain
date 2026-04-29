---
title: "ElevenLabs client_tool_call event shape — the data.client_tool_call nesting"
date: 2026-04-29
source: sethshoultes.github.io /build/ card-rendering fix
tags: [elevenlabs, client-tools, liveavatar, event-handlers, defensive-programming]
---

# ElevenLabs client_tool_call event shape — the data.client_tool_call nesting

## The Lesson

When ElevenLabs's `client_tool_call` event flows through the HeyGen LiveAvatar SDK's `ELEVENLABS_AGENT_EVENT` passthrough, the tool name and parameters are nested **one level deeper** than the obvious shape:

- Naive (wrong): `event.data.tool_name`, `event.data.parameters.slug`
- Actual: `event.data.client_tool_call.tool_name`, `event.data.client_tool_call.parameters.slug`

The handler should be defensive against both shapes — ElevenLabs may also flatten in some SDK paths. Read the tool name and parameters from `data.client_tool_call || data`.

## Context

The /talk/ and /build/ pages on sethshoultes.com surfaced post cards via two paths:
- **Path A** (passive): scan `AVATAR_TRANSCRIPTION` text for known post titles
- **Path B** (explicit): listen for the agent's `show_blog_post` client tool call

Path A worked when the agent cited a post by exact title. Path B was registered (the tool was attached to the agent, the system prompt instructed it to call) but never seemed to render a card.

Pulled the agent's conversation history via the ElevenLabs admin API:

```
[agent] Great idea! I built a voice avatar at /talk/ ... I wrote about this in *The Avatar Reads First*...
[agent]
    TOOL_CALL  show_blog_post({"slug": "the-avatar-reads-first"})
```

The agent WAS calling the tool. With a valid slug. So the page handler should have rendered a card and didn't.

The handler:
```js
session.on(AgentEventsEnum.ELEVENLABS_AGENT_EVENT, (event) => {
  const evType = event?.elevenlabs_event_type;
  const data = event?.data || {};
  if (evType === "client_tool_call" && data.tool_name === "show_blog_post") {
    const slug = data.parameters?.slug;
    ...
  }
});
```

The check `data.tool_name === "show_blog_post"` was reading from the wrong path. Actual event shape (per ElevenLabs Conversational AI WebSocket protocol) wraps the tool call under a `client_tool_call` key:

```json
{
  "type": "client_tool_call",
  "client_tool_call": {
    "tool_name": "show_blog_post",
    "tool_call_id": "...",
    "parameters": {"slug": "the-avatar-reads-first"}
  }
}
```

The HeyGen passthrough preserves this — `data` is the full message minus the outer `type`, so `tool_name` lives at `data.client_tool_call.tool_name`, not `data.tool_name`.

## The Fix

Make the handler defensive against both shapes:

```js
session.on(AgentEventsEnum.ELEVENLABS_AGENT_EVENT, (event) => {
  const evType = event?.elevenlabs_event_type;
  const data = event?.data || {};
  // ElevenLabs wraps tool calls one level deeper than the obvious shape;
  // some SDK paths may flatten — check both.
  const tool = data.client_tool_call || data;
  const toolName = tool.tool_name || data.tool_name;
  const params = tool.parameters || data.parameters || {};
  if (evType === "client_tool_call" && toolName === "show_blog_post") {
    const slug = params.slug;
    ...
  }
});
```

Also added a `console.debug` for slug lookups that don't match `posts.json` so future failures are diagnosable from the browser console without re-grepping the SDK.

## How to Apply

- **When wiring an ElevenLabs client tool handler for the first time**: do NOT rely on the obvious `data.tool_name` path. Check both `data.client_tool_call?.tool_name` and `data.tool_name`. Failing fast in dev costs nothing; a silent miss in production costs a feature.
- **When a registered tool fires per the conversation log but the page UI doesn't react**: the most likely cause is event-shape mismatch, NOT a tool-registration problem. Verify the tool was called via the admin API (`/v1/convai/conversations/<id>`); if it was, the bug is in the handler, not the agent.
- **Always log the unhandled-shape case in dev**: `console.debug("unmatched tool call", evType, data)` saves ~30 minutes the next time this happens with a different tool.
- **The same defensive pattern applies to other ElevenLabs WS event types**: when the SDK is a passthrough (no schema validation, no normalization), assume the event shape can change between versions. Read defensively.

## Related

- [`liteavatar-sdk-no-client-user-message`](liteavatar-sdk-no-client-user-message.md) — co-discovered from the same /build/ debug session (different bug, same root: thin SDK passthrough means client code has to know the upstream shape).
- [`ElevenLabs Custom LLM Tool Passthrough`](ElevenLabs%20Custom%20LLM%20Tool%20Passthrough.md) — longer treatment of how ElevenLabs routes tool calls through the LiveKit data channel.
- [`agent-tool-response-trim-keep-ids`](agent-tool-response-trim-keep-ids.md) — when a tool's response shape has IDs the agent shouldn't speak but later turns need.
- Related skill: [`register-elevenlabs-client-tool`](https://github.com/sethshoultes/building-with-ai-skills/blob/main/skills/register-elevenlabs-client-tool/SKILL.md). Update this skill's `handler-templates.js` reference to reflect the defensive shape.
