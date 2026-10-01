---
name: cold-email
description: Write high-converting cold emails for outreach. Use when creating Instantly campaigns, cold email sequences, or outreach copy.
---

# Cold Email Skill

Write cold emails that get replies. Use for outreach via Instantly.ai.

## The Formula (100 Meetings in 6 Months)

Every email follows this structure:

1. **Relevant intro** — Research-based, shows you know them
2. **Agitate the pain** — Make it sting, don't be generic
3. **Paint future state** — Customer stories, what's possible
4. **Solve CTA** — "Is solving X worth a conversation?"

**Zero product talk.** Never mention your company name, jargon, or features in cold outreach.

## Voice & Tone

- Confident, not arrogant
- Empathetic, not preachy
- Clear, not clever
- Urgent, not pushy

## Email Structure

### Subject Lines
- Short (3-6 words)
- Pattern interrupt or curiosity
- Avoid spam triggers ("free", "limited time", ALL CAPS)

**Examples:**
- "The thing your best people stopped doing"
- "Why your best people are burning out"
- "Quick question about [Company Name]"

### Body (Short!)
- 50-100 words max
- 3-5 short sentences
- No paragraphs longer than 2 lines
- Mobile-first (people read on phones)

### CTA Patterns
- "Is solving X worth 15 minutes?"
- "Worth a quick call to see how they did it?"
- "Curious how they pulled it off?"

## CTA Strategy (High-Leverage)

*Source: @iamliamsheridan — the CTA is often the highest-leverage edit in a cold email.*

### The Decision Framework
Before writing the CTA, answer: **what do I want them to do?**
- Want a call? Ask for a call.
- Want to qualify them? Ask a question.
- Want a soft yes first? Offer more info.

Most cold emails ask for a meeting when the offer needs a conversation first. Match the ask to where the prospect is.

### Email 1 vs Email 2 — Different Jobs, Different CTAs

**Email 1 — earn the reply:**
- Low friction. You're opening a conversation, not closing a deal.
- Use: `"Worth a quick chat?"` or `"Curious if this is even relevant for you?"`

**Email 2 — create soft urgency:**
- They've seen you once and didn't reply. Different angle needed.
- Use: `"Just checking — is the timing off, or is this not a fit right now?"`
- This gives them permission to say no (closes loop) OR explain timing (opens real conversation).
- **Never use the same CTA on both emails.**

### Hard vs Soft CTAs

| Type | Example | Use When |
|------|---------|----------|
| **Soft** | "Worth a quick chat?" | Cold list, no brand awareness, complex offer |
| **Hard** | "15 minutes Thursday at 2pm?" | Warm market, high deal value, they already know you |

**For [YOUR_COMPANY]:** Almost always start soft. These are strangers. Earn the hard ask.

### Sell the Value of the Call — Not the Meeting

Instead of: *"Do you have 15 minutes to discuss?"* (what's in it for them? nothing)

Try: *"I'll put together a short breakdown of what we'd do for [District] specifically. Want me to send it over?"*

**Tested result:** Value-based CTA drove 2.3x replies vs plain `"worth a quick chat?"` on the same list.

**For [YOUR_COMPANY]:** Offer something specific — a look at how another school in their district is using it, a breakdown of what's actually landing with students, etc.

### What Fails (Everyone Does This)

❌ `"If you're interested, let me know and we can get something in the diary"`
- Puts all friction on them
- "Let me know" is vague
- "Get something in the diary" is effort

✅ `"I have Thursday at 2pm or Friday at 10am. Does either work?"`
✅ `"I put together a short breakdown for [School]. Want me to send it over?"`

### The Trust One-Liner
For high-value outreach (district-level), add after your CTA:

> *"No pressure — if it's not a fit I'll be upfront."*

Removes the biggest unstated fear: *what if this becomes a sales pitch I can't escape?*

### A/B Testing CTAs
When testing, **change only the CTA** — not the whole email:
1. Current CTA (baseline)
2. Same CTA + value they get from the call
3. Question-based: `"Is the timing off, or not a fit?"`

Run 500 sends per variant. The CTA alone can swing reply rates significantly.

## Email Sequence Timing

| Step    | Delay   | Focus                                  |
| ------- | ------- | -------------------------------------- |
| Email 1 | Day 1   | Pattern interrupt, establish relevance |
| Email 2 | +3 days | Agitate pain deeper                    |
| Email 3 | +3 days | Future state, social proof             |

## Variants (A/B Testing)

Always create 3 variants per email:
- **Variant A:** Direct pain agitation
- **Variant B:** Question-led (curiosity)
- **Variant C:** Social proof led

## Instantly.ai Integration

When uploading to Instantly:
1. Use HTML `<p>` tags for paragraph spacing (NOT `\n`)
2. Set delays in days (0, 3, 6)
3. Include all variants for A/B testing

```bash
curl -s -X PATCH "https://api.instantly.ai/api/v2/campaigns/{id}" \
  -H "Authorization: Bearer $INSTANTLY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sequences": [{
      "steps": [
        {"type": "email", "delay": 0, "variants": [...]},
        {"type": "email", "delay": 3, "variants": [...]},
        {"type": "email", "delay": 3, "variants": [...]}
      ]
    }]
  }'
```

## Lessons Learned

### What Works
- **Pain-first, not product-first** — People respond to their problems
- **Short emails** — Under 100 words outperform long ones
- **Specific > generic** — "47 things on your plate" beats "you're busy"
- **Questions > statements** — "Worth a call?" beats "Let's schedule a call"

### What Doesn't Work
- Product pitches in cold email
- Long emails (over 150 words)
- Multiple CTAs
- Generic pain ("everyone is struggling with X")
- Markdown formatting (use HTML)

---

## Hormozi Email Tactics

*Source: Alex Hormozi — $10M in 90 days from email, 35-45x ROI on email spend*

### Deliverability & Avoiding Promo Tab

1. **Plain text over images** — Emails with images look promotional. Keep it text-only to look like real business correspondence.

2. **Limit links** — One or two max. More links = spam signal.

3. **Remove money language** — Words like "profit", "revenue", "$" in the body trigger spam filters. Keep financial language minimal.

4. **Get replies** — When someone replies to your email, you get "whitelisted" by their email provider. Build in a reason to reply: *"Reply YES and I'll send you X"*

5. **17% of B2B marketing emails never reach the inbox** — Not even promo tab, just vanity. These tactics matter.

### Timing

| Audience | Best Days | Best Times |
|----------|-----------|------------|
| B2C | Monday, Tuesday | 10am-noon, 1pm-3pm |
| B2B | Wednesday | 10am-noon, 1pm-3pm |

*Why Wednesday for B2B?* Business people are drowning Mon/Tue. They catch their breath mid-week.

### Reward Every Step

Think in terms of **feedback loops** — people do things because they were rewarded for doing them before.

| Action | How to Reward |
|--------|---------------|
| Opens email | Immediate value at top (quote, hook, insight) |
| Reads email | Meat delivers on promise |
| Clicks | Landing page delivers more value |

**First line = reward for opening.** Start with something valuable in one glance — a quote, a stat, or a hook. Don't start with "Hi [Name]" + fluff.

### The PS Statement

> Beyond the headline, the PS is the most read part of the email.

**Always include a PS.** Use it for:
- A contextual CTA
- A second hook or curiosity trigger
- Something fun (meme, one-liner)

*Not having a PS is "PS stupid"*

### Preview Text Optimization

That gray text after the subject line? **24% of people check it before deciding to open.**

Don't leave it to chance (default = first 150 characters of email body, often garbage like "Hi John").

Manually set it to your best hook or curiosity line.

### Speed to Lead

> Harvard Business Review: Calling leads within 60 seconds of opt-in = **391% increase in sales**

When someone fills out a form, calls them within 60 seconds. Most businesses wait hours or days. This is a massive competitive advantage.

### Segmentation

> HubSpot study: Segmented email lists see **791% higher ROI**

Send the right emails to the right people. Segment by:
- Role (practitioner vs. manager vs. executive)
- Stage (cold vs. warm vs. customer)
- Revenue/size (small org vs. large enterprise)

An advanced email to beginners = "not for me"
A beginner email to advanced = "I already know this"

### Testimonial Hooks (for email stories)

When sharing customer stories, **pain-based hooks work best**.

Top-performing hooks from 2,500+ testimonials:
- *"We were two months away from shutting our doors"*
- *"I paid payroll, rent, and finished the month with $0 profit"*

**Don't ask:** "How was life before you started working with us?" (too vague, gets rambling answer)

**Ask:** "What was your worst moment?" — Moments create hooks. Details make them powerful.

### Unsubscribes

**Don't fear unsubscribes.** They're healthy list hygiene.

- Keeping uninterested people hurts your domain reputation
- People who unsubscribe still know who you are
- They might show up as customers through another channel

**First email after long silence = higher unsubscribes.** This is normal — you're "shaking the tree" and pulling forward churn. Expect ~1% on first email, then ~0.4% ongoing.

### Cadence

The sweet spot seems to be **3x per week** for newsletter-style emails.

For cold outreach sequences: stick to the 0-3-3 day cadence (Email 1, wait 3 days, Email 2, wait 3 days, Email 3).

### Contextual CTAs

> Don't copy-paste the same CTA across different emails.

If the email is about testimonials, the CTA should relate to testimonials.
If the email is about a specific pain point, the CTA should promise relief for that pain.

Take the extra 30 seconds to make it flow.

---

## Dimitar's Cold Outreach Principles

*Source: @dimitarangg — 1M+ angles tested, 5M+ sends, 1,000s of calls booked*

### Volume + Skill (Both Required)

Cold outreach is a numbers game first, skills game second. **Volume first, then optimize.**

- 1,000 emails at 2% reply = 20 replies
- 100 emails at 4% reply = 4 replies

The 2% campaign wins. Don't perfect messaging before you've started sending.

### Offer > Copy

**No amount of great copy saves a bad offer.** The test:

> "If I stated this offer in plain, boring language, would someone still want it?"

"Here's the exact script that booked 48 calls last month" → yes  
"Let's hop on a call to discuss synergies" → no

Fix the offer before touching the copy.

### Psychology Framework

**Loss Aversion** — Humans fear loss 2.5x more than they desire equivalent gain.
- "You're falling behind" beats "you could get ahead"
- Focus on what they're *losing* by not acting, not what they'd gain

**Pattern Interrupt** — Their inbox is full of "quick question" and "partnership opportunity." Break the pattern in the first 2 seconds. Controversial subject lines, weird angles, unexpected approaches.

**Mere Exposure Effect** — Familiarity breeds preference. Multi-touch sequences beat single emails by 3-5x. They need to see you multiple times to trust you.

**Reciprocity** — Value must feel effortful and personalized. Generic "free tips" don't trigger it. Specific insight about their situation does.

**Curiosity Gap** — "Noticed something about your outbound" forces opens. "Here's a free audit" doesn't. Open loops that only close by responding.

**Commitment Consistency** — Don't ask for the call immediately. Get a micro-commitment first: "Does this sound relevant to what you're dealing with?" They say yes → asking for the call is now consistent with what they agreed to.

### Message Architecture

**3-Paragraph Structure:**
1. Who you are (name, company)
2. Why you're relevant (the challenge you solve)
3. What you want (assumptive ask)

No fluff. No fake personalization. No "saw we both went to the same college."

**4-6 Sentence Rule** — Once it hits 7+ sentences, read rates drop. 4-6 fits on one phone screen, scannable in 3 seconds.

**Assumptive vs. Passive Language:**

| ❌ Passive | ✅ Assumptive |
|-----------|---------------|
| "Would this be worth a chat?" | "Do either of these times work?" |
| "Let me know if you have questions" | "Looking to set up 15 min this week" |
| "Is this something you'd be interested in?" | "Here's my calendar, book what works" |

Passive language invites rejection. Assumptive language assumes agreement.

### Follow-Up Framework

**24-48 Hour Rule** — Standard advice says 5-7 days. What actually works: 24-48 hours max. Slow follow-ups signal you don't care.

**Three-Touch Structure:**
1. Benefit of the doubt: "Just making sure you caught my note"
2. Direct request: "Please give me your thoughts on this"
3. Assumptive breakup: "Is next month a better time?"

Then move on.

**70-80% of meetings come from follow-ups, not initial emails.** Your first email is planting the seed. Follow-ups are where deals happen.

**Hit hard, hit fast, move on.** After 4-5 touches with no response, move to fresh contacts. Over-following-up looks desperate.

### Metrics That Matter

| Metric | Target | If Below → Problem Is |
|--------|--------|------------------------|
| Open rate | 40-60% | <30% = deliverability |
| Reply rate | 2-5% | <1% = messaging |
| Positive reply rate | 40-50% of replies | Offer or wrong pain points |
| Booking rate | 30-50% of positive | Weak CTA or objection handling |
| Show rate | 70-80% of booked | Weak confirmation sequence |
| Close rate | 20-30% of shown | Sales problem, not outreach |

**Diagnosing bottlenecks:** Fix one thing at a time. Small improvements compound — 2% → 3% reply rate = 50% more replies.

**Only scale when:** Reply rate >2%, positive reply rate >1%, booking rate >30%. Scaling broken outreach just burns leads faster.

### Objection Handling

Build a response bank. Don't craft from scratch each time:

| Objection | Response |
|-----------|----------|
| "What do you charge?" | "Depends on scope — easier to show on a quick call how it maps to your situation. Here's my calendar." |
| "We already have something" | "Most of our customers came from other solutions. Worth seeing if we do something differently." |
| "Not a priority right now" | "Got it — when does it become a priority? Happy to follow up then." |
| "Send me more info" | "Absolutely — what specifically would be most useful? Or easier to show on a quick call." |

**Objections = openings.** They responded. That's more than 95% of your list.

### Multi-Channel Strategy

- **Email:** Highest volume, good conversion, scalable → primary channel
- **LinkedIn:** Best targeting (title, company size, industry, recent job changes), moderate conversion → use to *find* ICP, then email
- **Phone:** Highest conversion, lowest volume → reserve for warm/high-value

When someone sees your LinkedIn connection + email + Twitter reply, they think you're everywhere. Trust builds faster from multiple touchpoints.

## Quality Check

Before sending, gut-check:
- Does it sound like a human wrote it? (Read it aloud)
- Would YOU reply to this if you received it?
- Does every sentence serve the reader, not the sender?
- Is the personalization connected to the problem?
- Is there one clear, low-friction ask?

---

*Update this skill as we learn what converts.*
