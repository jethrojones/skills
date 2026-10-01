---
name: instantly
description: Manage Instantly.ai cold email campaigns, leads, and email accounts via API. Use when creating campaigns, adding leads, checking analytics, managing sending accounts, or syncing cold outreach data.
---

# Instantly.ai Cold Email Platform

API for cold email outreach — separate from HubSpot to protect domain reputation.

## Authentication

```bash
INSTANTLY_KEY=$(cat ~/.config/instantly/api_key.txt)
curl -s "https://api.instantly.ai/api/v2/endpoint" \
  -H "Authorization: Bearer $INSTANTLY_KEY"
```

## Core Endpoints

### Campaigns

```bash
# List campaigns
curl -s "https://api.instantly.ai/api/v2/campaigns" \
  -H "Authorization: Bearer $INSTANTLY_KEY" | jq '.items'

# Get campaign by ID
curl -s "https://api.instantly.ai/api/v2/campaigns/{id}" \
  -H "Authorization: Bearer $INSTANTLY_KEY"

# Create campaign
curl -s -X POST "https://api.instantly.ai/api/v2/campaigns" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Campaign Name",
    "email_list": ["sender@domain.com"]
  }'

# Activate campaign
curl -s -X POST "https://api.instantly.ai/api/v2/campaigns/{id}/activate" \
  -H "Authorization: Bearer $INSTANTLY_KEY"

# Pause campaign
curl -s -X POST "https://api.instantly.ai/api/v2/campaigns/{id}/pause" \
  -H "Authorization: Bearer $INSTANTLY_KEY"
```

### Leads

```bash
# List leads (POST with filters)
curl -s -X POST "https://api.instantly.ai/api/v2/leads/list" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{"campaign_id": "xxx", "limit": 100}'

# Add lead to campaign
curl -s -X POST "https://api.instantly.ai/api/v2/leads" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "xxx",
    "email": "lead@company.com",
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "Acme Inc",
    "custom_variables": {
      "school_name": "Lincoln High",
      "title": "Principal"
    }
  }'

# Add multiple leads
curl -s -X POST "https://api.instantly.ai/api/v2/leads/batch" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "xxx",
    "leads": [
      {"email": "a@example.com", "first_name": "Alice"},
      {"email": "b@example.com", "first_name": "Bob"}
    ]
  }'

# Update lead status
curl -s -X PATCH "https://api.instantly.ai/api/v2/leads/{id}" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{"interest_status": "interested"}'

# Delete lead
curl -s -X DELETE "https://api.instantly.ai/api/v2/leads/{id}" \
  -H "Authorization: Bearer $INSTANTLY_KEY"
```

### Lead Lists (for organization)

```bash
# List lead lists
curl -s "https://api.instantly.ai/api/v2/lead-lists" \
  -H "Authorization: Bearer $INSTANTLY_KEY"

# Create lead list
curl -s -X POST "https://api.instantly.ai/api/v2/lead-lists" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Virginia Middle Schools"}'
```

### Email Accounts

```bash
# List connected accounts
curl -s "https://api.instantly.ai/api/v2/accounts" \
  -H "Authorization: Bearer $INSTANTLY_KEY"

# Get account status
curl -s "https://api.instantly.ai/api/v2/accounts/{email}" \
  -H "Authorization: Bearer $INSTANTLY_KEY"

# Test account vitals
curl -s -X POST "https://api.instantly.ai/api/v2/accounts/test/vitals" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{"emails": ["sender@domain.com"]}'

# Enable warmup
curl -s -X POST "https://api.instantly.ai/api/v2/accounts/warmup/enable" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{"emails": ["sender@domain.com"]}'

# Disable warmup
curl -s -X POST "https://api.instantly.ai/api/v2/accounts/warmup/disable" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{"emails": ["sender@domain.com"]}'
```

### Analytics

```bash
# Campaign analytics
curl -s "https://api.instantly.ai/api/v2/campaigns/analytics?id={campaign_id}" \
  -H "Authorization: Bearer $INSTANTLY_KEY"

# Analytics overview
curl -s "https://api.instantly.ai/api/v2/campaigns/analytics/overview" \
  -H "Authorization: Bearer $INSTANTLY_KEY"
```

### Emails (Unibox)

```bash
# List emails/replies
curl -s "https://api.instantly.ai/api/v2/emails" \
  -H "Authorization: Bearer $INSTANTLY_KEY"

# Get unread count
curl -s "https://api.instantly.ai/api/v2/emails/unread/count" \
  -H "Authorization: Bearer $INSTANTLY_KEY"

# Reply to email
curl -s -X POST "https://api.instantly.ai/api/v2/emails/reply" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "reply_to_uuid": "xxx",
    "body": "Thanks for your response..."
  }'
```

### Block List

```bash
# Add to block list
curl -s -X POST "https://api.instantly.ai/api/v2/block-list-entries" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{"entries": ["blocked@domain.com", "baddomain.com"]}'
```

### Webhooks

```bash
# Create webhook
curl -s -X POST "https://api.instantly.ai/api/v2/webhooks" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-endpoint.com/webhook",
    "event_types": ["reply", "bounce", "unsubscribe"]
  }'
```

## Lead Interest Statuses

- `interested` — Positive reply
- `not_interested` — Negative reply
- `meeting_booked` — Meeting scheduled
- `meeting_completed` — Meeting done
- `closed` — Deal closed
- `out_of_office` — Auto-reply
- `wrong_person` — Not the right contact

## Workflow: HubSpot + Instantly

1. **Export cold contacts from HubSpot** (or external list)
2. **Import to Instantly** via API
3. **Run cold campaign** in Instantly
4. **Sync positive replies back to HubSpot** (interested, meeting_booked)
5. **Nurture warm leads in HubSpot** sequences

This protects your main domain reputation while still using HubSpot as CRM.

## Email Sequences (Campaign Steps)

Add email steps via PATCH to update a campaign with sequences:

```bash
curl -s -X PATCH "https://api.instantly.ai/api/v2/campaigns/{id}" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sequences": [{
      "steps": [
        {
          "type": "email",
          "delay": 0,
          "variants": [
            {"subject": "Subject A", "body": "<p>Email body A</p>"},
            {"subject": "Subject B", "body": "<p>Email body B</p>"}
          ]
        },
        {
          "type": "email",
          "delay": 3,
          "variants": [
            {"subject": "Follow-up", "body": "<p>Follow-up body</p>"}
          ]
        }
      ]
    }]
  }'
```

**Important:**
- `delay` is in days (0 = immediate, 3 = 3 days after previous step)
- `variants` are A/B test versions — Instantly rotates through them
- Each step requires `type`, `delay`, and at least one variant

### Email Body Formatting (Critical!)

**Always use HTML `<p>` tags for paragraphs.** Plain text with `\n` newlines renders as a wall of text.

❌ Wrong:
```json
{"body": "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."}
```

✅ Correct:
```json
{"body": "<p>First paragraph.</p><p>Second paragraph.</p><p>Third paragraph.</p>"}
```

For bullet-style lists, use `<br>` within a paragraph:
```json
{"body": "<p>What changed:</p><p>→ Item one<br>→ Item two<br>→ Item three</p>"}
```

## Python Helper Script

See `scripts/instantly.py` for a CLI wrapper.
