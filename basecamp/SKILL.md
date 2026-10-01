---
name: basecamp
description: Interact with Basecamp via the Basecamp CLI. Full API coverage projects, todos, cards, messages, files, schedule, check-ins, timeline, recordings, templates, webhooks, subscriptions, lineup, chat, gauges, assignments, notifications, and accounts. Use for ANY Basecamp question or action.
---

# Basecamp CLI

Official CLI (`basecamp`) installed at `/usr/local/bin/basecamp`. Use it for all Basecamp operations — do NOT use raw curl API calls anymore.

## Installation / Auth

```bash
basecamp auth login          # Opens browser for OAuth
basecamp auth login --scope full  # Full read+write (BC3 OAuth only)
basecamp auth status         # Check auth
basecamp doctor              # Health check
```

Config lives at `~/.config/basecamp/`. Tokens auto-refresh.

## Agent Invariants

**MUST follow these rules:**

1. **Choose the right output mode** — `--jq` when you need to filter/extract data; `--json` for full JSON; `--md` when presenting results to a human. **Never pipe to external `jq` — use `--jq` instead.**
2. **Parse URLs first** with `basecamp url parse "<url>"` to extract IDs
3. **Comments are flat** - reply to parent recording, not to comments
4. **Check context** via `.basecamp/config.json` before assuming project
5. **Formatting for messages** — Content fields accept basic HTML but MARKDOWN IS NOT SUPPORTED. Tables, code blocks, and complex markdown render poorly. For messages: use plain text with line breaks, or use bullet lists. For formatted content (tables, markdown): create a Vault document instead of a message.
6. **Project scope is mandatory for most commands** — via `--in <project>` or `.basecamp/config.json`

### Output Modes

| Goal | Flag | Format |
|------|------|--------|
| Filter/extract JSON | `--jq '<expr>'` | Built-in jq (no external jq needed) |
| Full JSON output | `--json` | JSON envelope: `{ok, data, summary, breadcrumbs, meta}` |
| Human-readable | `--md` / `-m` | GFM tables, task lists, Markdown |
| Automation | `--agent` | Raw JSON data (no envelope) |

### CLI Introspection

```bash
basecamp --agent --help          # Top-level commands as JSON
basecamp todos --agent --help    # Subcommand details as JSON
basecamp commands --json         # Full command catalog
```

## Quick Reference

| Task | Command |
|------|---------|
| List projects | `basecamp projects list --json` |
| My todos (in project) | `basecamp todos list --assignee me --in <project> --json` |
| My todos (cross-project) | `basecamp reports assigned --json` |
| Overdue todos | `basecamp reports overdue --json` |
| Upcoming schedule | `basecamp reports schedule --json` |
| Create todo | `basecamp todo "Task" --in <project> --list <list> --json` |
| Complete todo | `basecamp done <id>` |
| Create card | `basecamp card "Title" --in <project> --json` |
| Move card | `basecamp cards move <id> --to <column> --in <project>` |
| Post message | `basecamp message "Title" "Body" --in <project> --json` |
| Post to chat | `basecamp chat post "Message" --in <project> --json` |
| Add comment | `basecamp comment <recording_id> "Text" --in <project>` |
| Search | `basecamp search "query" --json` |
| Parse URL | `basecamp url parse "<url>" --json` |
| My assignments | `basecamp assignments --json` |
| Notifications | `basecamp notifications --json` |
| Account-wide gauges | `basecamp gauges list --json` |
| Watch timeline | `basecamp timeline --watch` |

## Todos

```bash
basecamp todos list --in <project> --json
basecamp todos list --assignee me --in <project>
basecamp todos list --overdue --in <project>
basecamp todos list --status completed --in <project>
basecamp todos list --list <todolist_id> --in <project>
basecamp todo "Task" --in <project> --list <list> --assignee me --due tomorrow
basecamp done <id> [id...]           # Complete (multiple OK)
basecamp reopen <id>                 # Uncomplete
basecamp assign <id> --to <person> --in <project>
basecamp todos sweep --overdue --complete --comment "Done" --in <project>
```

## Todolists

```bash
basecamp todolists list --in <project> --json
basecamp todolists create "Name" --in <project> --json
basecamp todolists update <id> --name "New" --in <project>
```

## Cards (Kanban)

**Note:** Cards do NOT support `--assignee` filtering. Fetch all and filter client-side.

```bash
basecamp cards list --in <project> --json
basecamp cards columns --in <project> --json
basecamp card "Title" "<p>Body</p>" --in <project> --column <id>
basecamp cards move <id> --to <column_id> --in <project>
basecamp cards move <id> --to <column_id> --position 1 --in <project>
basecamp cards move <id> --on-hold --in <project>
```

## Messages

```bash
basecamp messages list --in <project> --json
basecamp message "Title" "Body" --in <project>
basecamp message "Draft" "WIP" --draft --in <project>
basecamp message "Silent" "Body" --no-subscribe --in <project>
```

## Comments

```bash
basecamp comments list <recording_id> --in <project> --json
basecamp comment <recording_id> "Text" --in <project>
```

## Files & Documents

```bash
basecamp files list --in <project> --json
basecamp files download <id> --in <project>
basecamp files uploads create <file> --in <project>
basecamp files doc create "Doc" "Body" --in <project>
```

## Schedule

```bash
basecamp schedule entries --in <project> --json
basecamp schedule create "Event" --starts-at "2024-03-15T09:00:00Z" --ends-at "2024-03-15T10:00:00Z" --in <project>
basecamp reports schedule --json   # Cross-project upcoming events
```

## Check-ins

```bash
basecamp checkins --in <project> --json
basecamp checkins answers <question_id> --in <project>
basecamp checkins answer create <question-id> "My answer" --in <project>
```

## Timeline

```bash
basecamp timeline --json            # Account-wide
basecamp timeline --in <project>    # Project activity
basecamp timeline me --json         # Your activity
basecamp timeline --watch           # Live (TUI)
```

## People & Mentions

```bash
basecamp people list --json
basecamp me --json

# Deterministic mentions (preferred for agents)
basecamp people pingable --jq '.data[] | select(.name == "Jane Smith")'
# => {"id": 42000, "attachable_sgid": "BAh7...", "name": "Jane Smith"}
basecamp comment 123 "Hey [@Jane Smith](mention:BAh7...), check this" --in <project>

# Fuzzy (interactive)
basecamp comment <id> "@Jane.Smith, please review" --in <project>
```

## Assignments & Notifications

```bash
basecamp assignments --json
basecamp assignments due overdue --json
basecamp notifications --json
basecamp notifications read <id> --json
```

## Gauges

```bash
basecamp gauges list --json
basecamp gauges needles --in <project> --json
basecamp gauges create --position 75 --color green --in <project>
```

## Webhooks

```bash
basecamp webhooks list --in <project> --json
basecamp webhooks create "https://..." --types "Todo,Comment" --in <project>
basecamp webhooks update <id> --inactive
```

## URL Parsing

Always parse Basecamp URLs before acting:

```bash
basecamp url parse "https://3.basecamp.com/1234567/buckets/7654321/messages/1234567890" --json
# Returns: account_id, project_id, type, recording_id, comment_id
```

## Built-in jq Filtering

```bash
basecamp todos list --in <project> --jq '.data[] | select(.completed == false) | .title'
basecamp todos list --in <project> --jq '.data | length'
basecamp people list --jq '[.data[] | {name: .name, email: .email_address}]'
```

`--jq` implies `--json`. Never pipe to external `jq`.

## Per-repo Config

```bash
basecamp config init
basecamp config set project_id <id>
basecamp config set todolist_id <id>
# .basecamp/config.json — commit this to git for project context
```

## Exit Codes

| Exit | Meaning |
|------|---------|
| 0 | OK |
| 1 | Usage error |
| 2 | Not found |
| 3 | Auth error → `basecamp auth login` |
| 4 | Forbidden |
| 5 | Rate limit (auto-handled) |
| 6 | Network error |
| 7 | API error |
| 8 | Ambiguous (use ID instead of name) |

## Learn More

- CLI repo: https://github.com/basecamp/basecamp-cli
- Full SKILL.md (155 endpoints): https://github.com/basecamp/basecamp-cli/blob/main/skills/basecamp/SKILL.md
- BC3 API docs: https://github.com/basecamp/bc3-api
