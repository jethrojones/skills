# {{PRODUCT_NAME}} — Brand Context

> The voice contract. Read at the start of every `seo-content` run — **everything written is governed by this file.** Section headings match what `seo-sprint` writes too, so a brand doc from either skill is readable by both. If `seo-sprint` already created this file, reuse it as-is; don't overwrite it.

## Product

- **Name:** {{PRODUCT_NAME}}
- **One-liner (≤20 words):** {{ONE_LINER}}
- **What we do:** {{LONG_DESCRIPTION}}
- **Pricing structure:** {{PRICING_SUMMARY}}
- **Free tier?** {{FREE_TIER_YN}} — {{FREE_TIER_DETAILS}}

## Audience

- **Primary persona:** {{PERSONA_PRIMARY}}
- **Secondary personas:** {{PERSONA_SECONDARY}}
- **Industries we target:** {{INDUSTRIES}}
- **Jobs to be done (top 3):**
  1. {{JTBD_1}}
  2. {{JTBD_2}}
  3. {{JTBD_3}}

## Competitors

(Who you're compared against and who ranks for your terms — seeds the content-gap research in `references/research-recipes.md` and the honest treatment in comparison/listicle pieces.)

| Brand | URL | Tier (head / mid / niche) | Notes |
|---|---|---|---|
{{COMPETITORS_TABLE}}

## Brand voice

**This section is the heart of the file.** Get it specific.

- **Voice tags:** {{VOICE_TAGS}} — e.g. "honest, technical, no-jargon, dry-witty, founder-led"
- **Person/perspective:** {{PERSPECTIVE}} — e.g. "we" (team), "I" (founder-led), "you-focused"
- **Forbidden words/phrases:** {{FORBIDDEN}} — hard ban, grepped before every piece ships. e.g. "seamlessly," "revolutionary," "synergy"
- **Reference brands for tone:** {{TONE_REFERENCES}} — e.g. "Linear's docs, Buttondown's homepage"
- **Existing content to match:** {{EXISTING_CONTENT_NOTE}} — 1-2 published pieces whose rhythm new content should match (so a reader can't tell it was written in a different session)

## Anti-positioning (where we don't compete)

(Used for honest comparison/listicle sections — naming what you intentionally don't do is a trust + ranking signal. List ≥5.)

1. {{ANTI_POS_1}}
2. {{ANTI_POS_2}}
3. {{ANTI_POS_3}}
4. {{ANTI_POS_4}}
5. {{ANTI_POS_5}}

## Concrete differentiators

(Things you DO that competitors don't — used to weave the product into a piece where it genuinely helps the reader, not bolt it on at the end.)

1. {{DIFF_1}}
2. {{DIFF_2}}
3. {{DIFF_3}}
4. {{DIFF_4}}

## Proprietary data & first-hand experience

(The information-gain moat. As of the 2026 core updates, the pieces that win contain something the top 10 *can't* — original data, first-hand testing, lived experience. List what this product can legitimately draw on so every piece can inject ≥1 original element.)

- **Product/usage data we can anonymize & cite:** {{PROPRIETARY_DATA}} — e.g. "aggregate send volumes, deliverability rates across N accounts, feature-adoption curves"
- **First-hand experience / things we've actually done:** {{FIRST_HAND}} — e.g. "ran X for 3 years, migrated N customers off Y, tested every tool in the category"
- **Original research we can run:** {{ORIGINAL_RESEARCH}} — e.g. "survey our user base, benchmark competitors hands-on, teardown analyses"
- **Internal experts we can attribute/quote:** {{INTERNAL_EXPERTS}}

## Author / E-E-A-T

(Verifiable authorship is a 2026 ranking + AI-citation signal. Who bylines the content and why they're credible.)

- **Default author:** {{AUTHOR_NAME}} — {{AUTHOR_TITLE}}
- **Credentials / why-credible:** {{AUTHOR_CREDENTIALS}}
- **Author bio URL / profile:** {{AUTHOR_URL}}

## Links to existing surfaces

- Domain: {{DOMAIN}}
- Homepage: {{HOMEPAGE_URL}}
- Pricing: {{PRICING_URL}}
- Existing blog/content: {{BLOG_URL}}
- Existing features list: {{FEATURES_URL}}

## Visual brand (optional)

> Editorial content reuses the site's existing layout components, which already carry styling — so `seo-content` does **not** need this section. Auto-fill it from `tailwind.config.*` / design-token CSS if trivially detectable; otherwise leave it for `seo-sprint` (which uses it to render programmatic pages). Don't interview the user about colors for an editorial run.

- **Accent color:** {{ACCENT_PRIMARY}}
- **Ink / surface:** {{INK_COLOR}} / {{SURFACE_COLOR}}
- **Fonts (hero / body):** {{FONT_HERO}} / {{FONT_BODY}}
