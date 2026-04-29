---
title: "LiveAvatar SDK has no client-side user-message API in LITE mode"
date: 2026-04-29
source: sethshoultes.github.io /build/ starter-prompt fix
tags: [liveavatar, elevenlabs, lite-mode, sdk, api-design, dynamic-variables]
---

# LiveAvatar SDK has no client-side user-message API in LITE mode

## The Lesson

`session.message(text)` on `@heygen/liveavatar-web-sdk@0.0.17` does NOT send a user message to the agent. It sends `AVATAR_SPEAK_RESPONSE` — which makes the avatar speak the text aloud as if it's the agent's own response. There is no LITE-mode client API for "send this as the user's turn." The avatar's mouth, not the agent's ear.

The workaround for priming the agent at session start is `elevenlabs_agent_config.dynamic_variables.starter_prompt` (or any name) at token-mint time, plus a paragraph in the agent's system prompt that reacts to `{{starter_prompt}}` if it's set.

## Context

The /build/ page on sethshoultes.com had starter-prompt buttons. Click "Add an avatar to my site," it would:

1. Stage the prompt text
2. Start the LiveAvatar session
3. Call `session.message(prompt)` to "send" the prompt to the agent

The user reported: the avatar greets normally, then waits silently. The starter never reaches the agent. Conversation logs confirmed: agent received nothing, just the greeting + empty pause.

Reading the SDK source (`/tmp/lasdk/package/lib/LiveAvatarSession/LiveAvatarSession.js`):

```js
message(message) {
    ...
    const data = {
        event_id: event_id,
        event_type: CommandEventsEnum.AVATAR_SPEAK_RESPONSE,
        text: message,
    };
    this.sendCommandEvent(data);
}
```

`AVATAR_SPEAK_RESPONSE` is one of three avatar-side commands (`AVATAR_SPEAK_TEXT`, `AVATAR_SPEAK_RESPONSE`, `AVATAR_SPEAK_AUDIO`) — all three make the avatar SAY something. None are user-side. The SDK `CommandEventsEnum` has no `USER_MESSAGE` or equivalent. In LITE mode, the user can only speak (microphone goes through ElevenLabs's STT) or — at session start — pass dynamic variables.

## The Fix

Three-layer change:

1. **Page** (`/build/index.html`): instead of `session.message(prompt)` after connect, append `?starter=<prompt>` to the worker URL when fetching the session token.

2. **Worker** (`sethshoultes-avatar-worker/src/index.js`): accept `?starter`, validate length (≤800 chars to bound prompt-injection blast radius), forward as:
   ```js
   elevenlabs_agent_config: {
     ...
     dynamic_variables: { starter_prompt: starterPrompt }
   }
   ```

3. **Agent system prompt**: append a paragraph that conditions on `{{starter_prompt}}`:
   > When the dynamic variable {{starter_prompt}} is present and non-empty, the user just clicked a starter card on the /build/ page. Open the conversation by saying "Got it — let me walk you through that," then immediately begin addressing the starter topic. Cite the relevant blog post by title and call show_blog_post for it. Don't wait for the user to repeat the question — they already chose the topic.
   >
   > The starter request: {{starter_prompt}}

## How to Apply

- **When you want a LITE-mode avatar to start with content the user already selected** (starter cards, deep links, topic carousels): never reach for `session.message`. The fix lives at session-start, not after-connect. Use dynamic variables.
- **When debugging "the agent isn't responding to a programmatic message"**: check the SDK's command enum. If the API is named `message` / `say` / `repeat` / `speak`, it almost certainly puts words in the avatar's mouth, not in the user's input stream.
- **When you need the agent to SEE a user-style turn from the client** (not just be primed at session-start): you can't do it on the LiveAvatar Plugin path. Use the ElevenLabs SDK direct path (`@elevenlabs/client`'s `Conversation.startSession`) which exposes a different surface — or fall back to FULL mode where you control the LLM yourself.
- **When briefing a sub-agent on building a LITE-mode integration**: explicitly state "no client-side user-message API; user input is only via mic." Otherwise the agent will guess and ship a `session.message` call that fails silently in production.

## Related

- [`elevenlabs-tool-call-event-shape`](elevenlabs-tool-call-event-shape.md) — co-discovered bug from the same /build/ session: `data.client_tool_call.tool_name` nesting.
- [`ElevenLabs dynamicVariables smuggling pattern`](ElevenLabs%20dynamicVariables%20smuggling%20pattern.md) — same vector for passing per-session context (visitor source, starter topic, A/B variant) without editing the system prompt.
- [`heygen-credit-pools-and-which-products-use-which`](heygen-credit-pools-and-which-products-use-which.md) — context on which API key the LiveAvatar session-token mint requires.
- Related skill: [`add-avatar-to-site`](https://github.com/sethshoultes/building-with-ai-skills/blob/main/skills/add-avatar-to-site/SKILL.md) and [`register-elevenlabs-client-tool`](https://github.com/sethshoultes/building-with-ai-skills/blob/main/skills/register-elevenlabs-client-tool/SKILL.md).
