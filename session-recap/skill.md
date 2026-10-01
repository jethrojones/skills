---
name: session-recap
description: Write the end-of-session recap the user always wants — what changed, what's next — or a handoff recap for a non-technical teammate or client. Use at the end of any work session, or when asked to "summarize what we did" or "write this up for [person]."
---

# Session Recap

The user ends most working sessions asking for a recap. Produce it in one of two modes.

## Mode 1 — Recap for the user (default)
Direct and short. Format:

```
## What changed
- <one line per real change, most important first — verified facts only>

## Decisions made
- <only if any>

## What's next
- <open items, who owns them>
```

Rules: no fluff, no restating the conversation, no hedging. If something was attempted and failed, say so plainly. If a change is deployed, confirm you verified it live.

## Mode 2 — Handoff recap (non-technical teammate or client)
Written for a non-technical reader who wasn't in the session and will act on this alone.

- **Explain like the reader is 5** for anything technical (DNS, DMARC, API keys): what it is, why it matters to them, what they need to do — in plain words.
- **No markdown tables** — they paste badly into email. Use short labeled paragraphs or simple lists.
- **Leave out internal plumbing** that doesn't change what the reader does (which account something lives in, refactors, tooling detours).
- Include **expiry/ownership notes** ("this key expires on X; here's how you make a new one").
- End with a short "If something breaks" line: the first thing to check and who/what to ask.

## Both modes
- Pull only from what actually happened this session; verify claims against files/state before asserting them.
- Log the session in today's daily note at `<vault>/Daily Notes/` (append, never overwrite).

---
Created by Claude Fable 5 on 2026-07-04 09:03 PT. Generalized 2026-07-04 09:15 PT.
