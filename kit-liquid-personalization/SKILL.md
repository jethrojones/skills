# Kit Liquid Personalization Guide

Use this guide when writing emails for Kit (formerly ConvertKit) that need personalization, conditional content, or dynamic values using Liquid template language.

## Basic Personalization

### Adding Names and Email Addresses

```liquid
{{ subscriber.first_name }}
{{ subscriber.email_address }}
```

### Adding Custom Fields

Custom fields use the same format but with the field name (spaces become underscores, must be lowercase):

```liquid
{{ subscriber.last_name }}
{{ subscriber.photography_experience }}
{{ subscriber.subscription_active }}
```

**Rules for custom field names:**
- Must contain only Latin letters, underscores, hyphens, and/or numbers
- Must start with a Latin letter or underscore
- Must be lowercase

### Fallback/Default Values

Always use fallbacks to handle missing values:

```liquid
{{ subscriber.first_name | strip | default: "there" }}
{{ subscriber.last_name | strip | default: "friend" }}
```

**Important:** Filters (anything after `|`) are NOT supported in subject lines.

## Conditional Content

### Basic If/Else with Tags

```liquid
{% if subscriber.tags contains "Purchased course" %}
Content for subscribers with the tag.
{% else %}
Content for subscribers without the tag.
{% endif %}
```

### If/Elsif/Else Statements

```liquid
{% if subscriber.tags contains "Purchased course" %}
Content for course purchasers.
{% elsif subscriber.tags contains "Purchased ebook" %}
Content for ebook purchasers.
{% else %}
Content for non-purchasers.
{% endif %}
```

**Note:** The first positive match wins. Order conditions by priority from top to bottom.

### Checking Custom Field Values

Use `contains` for comparing custom field values:

```liquid
{% if subscriber.subscription_active contains "true" %}
Subscription is active!
{% endif %}

{% if subscriber.audience_segment_level contains "high" %}
High school content here.
{% elsif subscriber.audience_segment_level contains "middle" %}
Middle school content here.
{% endif %}
```

### Unless Statements

Show content only if a condition is NOT met:

```liquid
{% unless subscriber.tags contains "Purchased course" %}
Content for non-purchasers only.
{% endunless %}

{% unless subscriber.subscription_active contains "true" %}
Account setup is not yet complete.
{% endunless %}
```

### Nested Conditions

```liquid
{% if subscriber.tags contains "Past purchaser" %}
  {% if subscriber.tags contains "Purchased course" %}
    Has both "Past purchaser" and "Purchased course" tags.
  {% elsif subscriber.tags contains "Purchased ebook" %}
    Has "Past purchaser" and "Purchased ebook" tags.
  {% else %}
    Has "Past purchaser" but neither course nor ebook.
  {% endif %}
{% else %}
Does not have the "Past purchaser" tag.
{% endif %}
```

## Useful Filters

### Capitalization

```liquid
{{ subscriber.first_name | capitalize }}
```
Converts 'jughead' to 'Jughead'.

### Truncation (First Word Only)

```liquid
{{ subscriber.first_name | truncatewords: 1, "" }}
```
Converts 'Jughead Jones' to 'Jughead'.

### Stripping Whitespace

```liquid
{{ subscriber.first_name | strip }}
```
Removes leading and trailing spaces.

### Combining Filters

```liquid
{{ subscriber.first_name | truncatewords: 1, "" | capitalize }}
{{ subscriber.first_name | default: "friend" | truncatewords: 1, "" | capitalize }}
```

**Note:** Filters apply to fallback values too. `default: "friend" | capitalize` becomes "Friend".

### URL Encoding

```liquid
{{ subscriber.email_address | url_encode }}
```
Converts `jughead@example.com` to `jughead%40example.com`.

## Date & Time Filters

### Current Timestamp

```liquid
{{ "now" | timestamp }}
```

### Time Zone Conversion

```liquid
{{ "now" | in_time_zone: "America/Denver" }}
{{ "now" | in_time_zone: "America/Denver" | date: "%Y-%m-%d %H-%M-%S %z" }}
```

### Advance to Next Weekday

```liquid
{{ "now" | advance_date_to_next: "monday" }}
```

### Days/Weeks Since or Until

```liquid
{{ "2000-01-01" | days_since }}
{{ "2025-12-31" | days_until }}
{{ "2025-12-31" | weeks_until }}
```

## Common Patterns

### Personalized Greeting with Fallback

```liquid
Hi {{ subscriber.first_name | strip | default: "there" }},
```

### Conditional Content Based on Custom Field Boolean

```liquid
{% if subscriber.is_implementer contains "true" %}
You're an implementer!
{% else %}
You're not an implementer.
{% endif %}
```

### Show Content Only If Field is False/Empty

```liquid
{% unless subscriber.subscription_active contains "true" %}
Please complete your account setup.
{% endunless %}
```

### Multiple Conditions with AND

```liquid
{% if subscriber.subscription_active contains "true" and subscriber.onboarding_complete contains "true" %}
You're all set!
{% endif %}
```

### Multiple Conditions with OR

```liquid
{% if subscriber.audience_segment_level contains "high" or subscriber.audience_segment_level contains "district" %}
High school or district content.
{% endif %}
```

## Where Liquid Works in Kit

- Broadcast subject lines and email body
- Sequence subject lines and email body
- Incentive email subject lines and email body
- Content snippets
- Email templates
- Custom field values in automations

**Exception:** Filters (`default`, `truncatewords`, `capitalize`, `strip`) do NOT work in subject lines.

## Testing Personalized Content

1. Click "Preview" in the email editor
2. Click "Preview as subscriber"
3. Type a subscriber's email address
4. The preview will update to show exactly how it'll look for that subscriber

**Note:** In preview emails, shortcodes show as `[FIRST NAME GOES HERE]` etc. This is normal—they'll render correctly when actually sent.

## Common Syntax Errors

### Missing Brackets

```liquid
# Wrong
{% if subscriber.tags contains "Tag" %
Content
{% endif %}

# Correct
{% if subscriber.tags contains "Tag" %}
Content
{% endif %}
```

### Missing endif/endunless

```liquid
# Wrong
{% if subscriber.tags contains "Tag" %}
Content

# Correct
{% if subscriber.tags contains "Tag" %}
Content
{% endif %}
```

### Wrong Quote Marks

If your tag or value contains a quotation mark, use single quotes:

```liquid
{% if subscriber.tags contains 'He said "hello"' %}
```

### Troubleshooting Steps

1. Remove the code entirely
2. Re-add it from the personalization menu
3. If custom content, paste it back carefully
4. Check for missing brackets, quotes, or endif/endunless statements
