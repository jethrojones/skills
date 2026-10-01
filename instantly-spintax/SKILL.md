# Instantly Spintax & Deliverability

Use spintax to randomize email content and improve deliverability. Prevents ESP detection as spam.

## Why Spintax Matters

Email service providers flag accounts sending identical emails to thousands of recipients. Spintax creates unique variations automatically.

## Spintax Format

```
{random|word one|word two|word three}
```

- Curly brackets with `random` keyword
- Pipe `|` separates options
- Can be words, phrases, or entire sentences
- No limit on number of options

## Examples

**Single words:**
```
Would you like to {random|learn|find out|discover} more?
```

**Phrases:**
```
Can I {random|give you a quick call anytime next week|schedule a brief chat|find 15 minutes on your calendar}?
```

**Full copy with multiple spintax:**
```
Hi {{firstName}},

I wanted to {random|reach out|connect|touch base} about {random|helping|assisting|supporting} {{companyName}} {random|handle|manage|deal with} {random|increasing|boosting|raising} your pipeline.

{random|Can I give you a quick call anytime next week?|Do you have any time this week or next for a quick chat?|Mind if I send over some info?}
```

## Using ChatGPT to Generate Spintax

**Prompt for synonyms:**
```
Bring two synonyms for "handle" and put the results in this format:
{random|handle|SYNONYM1|SYNONYM2}
```

**Prompt for phrase variations:**
```
Say the following sentence in two different ways:
"Would you like to hear more?"
Put the results in this format: {random|OPTION1|OPTION2|OPTION3}
```

## Best Practices

1. **You don't need many** — A few spintax variations + first name + company name = thousands of unique emails
2. **More valuable at scale** — If sending 10/day, less critical. At 500+/day, very important.
3. **Combine with variables** — `{{firstName}}`, `{{companyName}}` already provide uniqueness
4. **Test preview** — In Instantly, click "Preview Email" to see randomized output

## When to Use

- Sending 100+ emails/day with same copy
- Running campaigns across multiple accounts
- Notice deliverability declining
- Getting flagged as spam despite good targeting

## Source

Based on Instantly Strategy Sessions: "Spintax, Quality Over Quantity & Q&A"
https://www.youtube.com/watch?v=KKBILF7OVC4
