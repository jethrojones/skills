---
name: kit
description: Interact with Kit (email marketing) API for subscribers, tags, and broadcasts. Use when user asks about Kit, email lists, or subscriber management.
---

# Kit API Skill

API access to Kit (formerly ConvertKit) for managing subscribers, tags, sequences, and email campaigns.

## Authentication

API key stored at `~/.config/kit/api_key.txt`

```bash
KIT_KEY=$(cat ~/.config/kit/api_key.txt)
```

All requests use header: `X-Kit-Api-Key: $KIT_KEY`

Base URL: `https://api.kit.com/v4`

## Rate Limits

- API Key: 120 requests per 60 seconds
- OAuth: 600 requests per 60 seconds

---

## Subscribers

```bash
# List subscribers (paginated, 500 per page)
curl -s "https://api.kit.com/v4/subscribers" \
  -H "X-Kit-Api-Key: $KIT_KEY"

# Get subscriber by email
curl -s "https://api.kit.com/v4/subscribers?email_address=user@example.com" \
  -H "X-Kit-Api-Key: $KIT_KEY"

# Get subscriber by ID
curl -s "https://api.kit.com/v4/subscribers/{subscriber_id}" \
  -H "X-Kit-Api-Key: $KIT_KEY"

# Create subscriber
curl -s -X POST "https://api.kit.com/v4/subscribers" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email_address": "user@example.com",
    "first_name": "Jane",
    "fields": {
      "last_name": "Smith",
      "school": "Lincoln High"
    }
  }'

# Update subscriber
curl -s -X PUT "https://api.kit.com/v4/subscribers/{subscriber_id}" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "fields": {
      "is_implementer": "true"
    }
  }'
```

---

## Tags

```bash
# List all tags
curl -s "https://api.kit.com/v4/tags" \
  -H "X-Kit-Api-Key: $KIT_KEY"

# Create tag
curl -s -X POST "https://api.kit.com/v4/tags" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Tag Name"}'

# Add tag to subscriber (by email)
curl -s -X POST "https://api.kit.com/v4/tags/{tag_id}/subscribers" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email_address": "user@example.com"}'

# List subscribers with tag
curl -s "https://api.kit.com/v4/tags/{tag_id}/subscribers" \
  -H "X-Kit-Api-Key: $KIT_KEY"

# Remove tag from subscriber
curl -s -X DELETE "https://api.kit.com/v4/tags/{tag_id}/subscribers/{subscriber_id}" \
  -H "X-Kit-Api-Key: $KIT_KEY"
```

### Key Tags

| Tag | ID | Purpose |
|-----|-----|---------|
| is implementer | <TAG_ID> | Pilot implementers |
| enrolled in pilot | <TAG_ID> | Enrolled in pilot |
| ready for pilot to start | <TAG_ID> | Ready to begin |
| pilot 2026 accepted | <TAG_ID> | Accepted for 2026 pilot |
| applied for pilot 2026 | <TAG_ID> | Applied for 2026 pilot |

---

## Sequences

```bash
# List all sequences
curl -s "https://api.kit.com/v4/sequences" \
  -H "X-Kit-Api-Key: $KIT_KEY"

# Add subscriber to sequence (by email)
curl -s -X POST "https://api.kit.com/v4/sequences/{sequence_id}/subscribers" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email_address": "user@example.com"}'

# Add subscriber to sequence (by ID)
curl -s -X POST "https://api.kit.com/v4/sequences/{sequence_id}/subscribers/{subscriber_id}" \
  -H "X-Kit-Api-Key: $KIT_KEY"

# List subscribers in sequence
curl -s "https://api.kit.com/v4/sequences/{sequence_id}/subscribers" \
  -H "X-Kit-Api-Key: $KIT_KEY"
```

---

## Custom Fields

```bash
# List all custom fields
curl -s "https://api.kit.com/v4/custom_fields" \
  -H "X-Kit-Api-Key: $KIT_KEY"

# Create custom field
curl -s -X POST "https://api.kit.com/v4/custom_fields" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"label": "Field Name"}'
```

---

## Forms

```bash
# List forms
curl -s "https://api.kit.com/v4/forms" \
  -H "X-Kit-Api-Key: $KIT_KEY"

# Add subscriber to form
curl -s -X POST "https://api.kit.com/v4/forms/{form_id}/subscribers" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email_address": "user@example.com"}'
```

---

## Segments

```bash
# List segments (read-only)
curl -s "https://api.kit.com/v4/segments" \
  -H "X-Kit-Api-Key: $KIT_KEY"
```

---

## Broadcasts

```bash
# List broadcasts
curl -s "https://api.kit.com/v4/broadcasts" \
  -H "X-Kit-Api-Key: $KIT_KEY"

# Create broadcast (draft)
curl -s -X POST "https://api.kit.com/v4/broadcasts" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email_address": "from@example.com",
    "subject": "Email Subject",
    "content": "<p>HTML content here</p>"
  }'
```

---

## Pagination

All list endpoints return paginated results:

```json
{
  "pagination": {
    "has_previous_page": false,
    "has_next_page": true,
    "start_cursor": "xxx",
    "end_cursor": "yyy",
    "per_page": 500
  }
}
```

Use `?after={end_cursor}` to get next page:
```bash
curl -s "https://api.kit.com/v4/subscribers?after=WzEyMzQ1Njc4OTBd" \
  -H "X-Kit-Api-Key: $KIT_KEY"
```

---

## Bulk Operations

⚠️ Bulk endpoints require OAuth authentication (not API key).

For bulk uploads via API key, loop through one at a time with rate limit awareness:

```bash
# Example: Add multiple subscribers to a tag
for email in "a@example.com" "b@example.com" "c@example.com"; do
  curl -s -X POST "https://api.kit.com/v4/tags/<TAG_ID>/subscribers" \
    -H "X-Kit-Api-Key: $KIT_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"email_address\": \"$email\"}"
  sleep 0.5  # Rate limit safety
done
```

Or use Kit's CSV import UI for large batches.

---

## Common Workflows

### Add implementer to Kit
```bash
KIT_KEY=$(cat ~/.config/kit/api_key.txt)
EMAIL="teacher@school.edu"

# 1. Create/update subscriber
curl -s -X POST "https://api.kit.com/v4/subscribers" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"email_address\": \"$EMAIL\", \"first_name\": \"Jane\", \"fields\": {\"is_implementer\": \"true\"}}"

# 2. Add "is implementer" tag
curl -s -X POST "https://api.kit.com/v4/tags/<TAG_ID>/subscribers" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"email_address\": \"$EMAIL\"}"

# 3. Add to implementer sequence
curl -s -X POST "https://api.kit.com/v4/sequences/2622866/subscribers" \
  -H "X-Kit-Api-Key: $KIT_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"email_address\": \"$EMAIL\"}"
```

### Check if subscriber exists
```bash
curl -s "https://api.kit.com/v4/subscribers?email_address=user@example.com" \
  -H "X-Kit-Api-Key: $KIT_KEY" | jq '.subscribers[0].id // "not found"'
```
