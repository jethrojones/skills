---
name: google-workspace
description: Gmail, Calendar, Drive, Docs, Sheets via the gws CLI. Use for any Google Workspace task — reading email, calendar events, Drive files, Sheets, Docs, and more.
---

# Google Workspace CLI (gws)

Installed at `gws`. Authenticated as `YOUR_GOOGLE_ACCOUNT`. Credentials in `~/.config/gws/`.

## Key Principle
**Always use `gws` first.** Fall back to `gog` only if a specific API isn't covered.

## Helper Commands (use these first)

```bash
# Email
gws gmail +triage                                          # Unread inbox summary
gws gmail +send --to alice@example.com --subject "Hi" --body "Hello"
gws gmail +reply --message-id MSG_ID --body "Thanks!"

# Calendar
gws calendar +agenda                                       # Today's upcoming events
gws calendar +agenda --today                               # Today only
gws calendar +insert --summary "Meeting" --start "2026-03-26T10:00:00" --end "2026-03-26T11:00:00"

# Sheets
gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A1:D10"
gws sheets +append --spreadsheet SPREADSHEET_ID --values "Alice,95"

# Drive
gws drive +upload ./report.pdf --name "Q1 Report"

# Docs
gws docs +write --document DOC_ID --text "Appended content"

# Workflows
gws workflow +standup-report     # Today's meetings + open tasks
gws workflow +weekly-digest      # This week's meetings + unread count
gws workflow +meeting-prep       # Prep for next meeting
```

## Discovery Commands (full API surface)

```bash
# List files
gws drive files list --params '{"pageSize": 10}'

# Get email
gws gmail users messages list --params '{"userId": "me", "maxResults": 10, "q": "is:unread"}'
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}'

# List calendar events
gws calendar events list --params '{"calendarId": "primary", "maxResults": 10, "orderBy": "startTime", "singleEvents": true, "timeMin": "2026-03-25T00:00:00Z"}'

# Sheets read/write
gws sheets spreadsheets values get --params '{"spreadsheetId": "ID", "range": "Sheet1!A1:C10"}'
gws sheets spreadsheets values append \
  --params '{"spreadsheetId": "ID", "range": "Sheet1!A1", "valueInputOption": "USER_ENTERED"}' \
  --json '{"values": [["Name", "Score"]]}'

# Introspect any method
gws schema drive.files.list
gws schema gmail.users.messages.list
```

## Output & Pagination

```bash
gws drive files list --params '{"pageSize": 100}' --page-all   # Auto-paginate (NDJSON)
gws drive files list --params '{"pageSize": 100}' --page-limit 5
```

All output is structured JSON. Pipe to `jq` freely.

## Sheets Note
Wrap ranges in **single quotes** — bash interprets `!` as history expansion:
```bash
gws sheets spreadsheets values get --params '{"spreadsheetId": "ID", "range": "Sheet1!A1:C10"}'
```

## Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | API error |
| 2 | Auth error → `gws auth login -s drive,gmail,calendar,sheets,docs` |
| 3 | Validation error |
| 4 | Discovery error |

## Auth
```bash
gws auth login -s drive,gmail,calendar,sheets,docs   # Re-authenticate
```
Config: `~/.config/gws/` | Client secret: `~/.config/gws/client_secret.json`
