# skills/ — Available Claude Code Skills

Skills organized by category. Each skill lives in its own subfolder with
a `SKILL.md` (or `skill.md`) that Claude Code loads automatically when it
detects a matching request. Invoke any skill directly with `/<skill-name>`.

## Prospecting & outreach

| Skill | What it does |
|-------|-------------|
| `cold-email` | Write high-converting cold emails and Instantly campaigns |

## Hardware & fabrication

| Skill | What it does |
|-------|-------------|
| `glowforge` | Glowforge laser jobs: Glowforge-ready SVGs (outlined text, QR codes), metal business cards, power/speed test patches, and driving app.glowforge.com via Chrome. Includes Optimization Doc card examples. |

## Content & copywriting

| Skill | What it does |
|-------|-------------|
| `copywriting` | Marketing copy for any page (homepage, landing, pricing, feature, about) |
| `copy-editing` | Multi-pass review and improvement of existing marketing copy |
| `content-strategy` | Plan content strategy, topic clusters, content ideas |
| `social-content` | Social media content for LinkedIn, Twitter/X, Instagram, TikTok |
| `email-sequence` | Email sequences, drip campaigns, lifecycle email programs |
| `ad-creative` | Generate/iterate ad creative at scale (headlines, descriptions, variations) |

## SEO

| Skill | What it does |
|-------|-------------|
| `seo-audit` | Audit technical SEO, on-page issues, meta tags |
| `ai-seo` | Optimize for AI search engines (AEO, GEO, LLMO, AI Overviews) |
| `schema-markup` | Add/fix JSON-LD structured data (FAQ, product, review, breadcrumb) |
| `programmatic-seo` | Build SEO pages at scale with templates + data |
| `site-architecture` | Plan page hierarchy, navigation, URL structure, internal linking |

## CRO (Conversion Rate Optimization)

| Skill | What it does |
|-------|-------------|
| `page-cro` | Optimize any marketing page for conversions |
| `signup-flow-cro` | Optimize signup, registration, trial activation flows |
| `onboarding-cro` | Post-signup activation, first-run experience, time-to-value |
| `form-cro` | Optimize non-signup forms (lead capture, contact, demo request) |
| `popup-cro` | Popups, modals, overlays, exit-intent, announcement banners |
| `paywall-upgrade-cro` | In-app upgrade screens, upsell modals, feature gates |
| `ab-test-setup` | Plan, design, implement A/B tests and experiments |
| `analytics-tracking` | GA4, GTM, conversion tracking, event tracking, UTM setup |

## Marketing strategy

| Skill | What it does |
|-------|-------------|
| `pricing-strategy` | Pricing tiers, packaging, monetization, willingness-to-pay research |
| `launch-strategy` | Product launches, feature announcements, go-to-market planning |
| `free-tool-strategy` | Build free tools for lead gen, SEO, brand awareness |
| `marketing-ideas` | 139 proven marketing approaches organized by category |
| `marketing-psychology` | 70+ mental models and behavioral science for marketing |
| `referral-program` | Referral/affiliate/ambassador program design and optimization |
| `churn-prevention` | Cancel flows, save offers, dunning, failed payment recovery |
| `product-marketing-context` | Create/maintain the foundational product marketing context doc |
| `competitor-alternatives` | Competitor comparison and alternative pages |
| `paid-ads` | PPC campaigns across Google, Meta, LinkedIn, Twitter/X |

## Sales

| Skill | What it does |
|-------|-------------|
| `sales-enablement` | Pitch decks, one-pagers, objection handling, demo scripts, ROI calculators |
| `instantly` | Manage Instantly.ai cold email campaigns, leads, accounts via API |
| `instantly-copywriting` | Instantly-specific copywriting and testing |
| `instantly-lead-conversion` | Instantly lead conversion optimization |
| `instantly-offer-niche` | Instantly offer and niche selection |
| `instantly-spintax` | Instantly spintax and deliverability |
| `revops` | Revenue operations, lead lifecycle, MQL/SQL, pipeline stages, CRM automation |

## Tools & integrations

| Skill | What it does |
|-------|-------------|
| `google-workspace` | Gmail, Calendar, Drive, Docs, Sheets via `gws` CLI |
| `google-workspace-mcp` | Same as above via MCP (no Google Cloud Console needed) |
| `hubspot-cli` | HubSpot dev via `hs` CLI — projects, apps, CMS, HubDB, custom objects |
| `basecamp` | Basecamp CLI — projects, todos, cards, messages, files, schedule |
| `kit` | Kit (email marketing) API — subscribers, tags, broadcasts |
| `kit-liquid-personalization` | Kit Liquid template personalization |
| `fizzy` | Fizzy boards, cards, steps, comments, reactions, pins |
| `vimeo-text-tracks` | Manage Vimeo subtitles/captions via API |
| `defuddle` | Extract clean content from URLs via defuddle CLI |
| `excalidraw-flowchart` | Create Excalidraw flowcharts from descriptions |

## File operations

| Skill | What it does |
|-------|-------------|
| `convert-word-to-markdown` | .docx → .md via pandoc |
| `convert-markdown-to-word` | .md → .docx via pandoc |
| `contact-list-cleanup` | Clean raw contact exports (CSV/XLSX) for HubSpot/Instantly/Kit import |
| `wav-split` | Split multi-channel recorder WAVs (POD000xx) into per-mic mono tracks |

## Meta

| Skill | What it does |
|-------|-------------|
| `bulk-automation-workflow` | Standard pattern for large-scale batch operations |
| `session-recap` | End-of-session recap or non-technical handoff recap |
| `homelab-ops` | Homelab troubleshooting — machine inventory + known-fix notes in the vault |
| `marketingskills` | Parent skill containing all marketing sub-skills |

## Notes

- **Global install:** the generally-useful skills here are symlinked into `~/.claude/skills/` so they work from any directory. New skill → add the folder here, then `ln -s <repo>/<name> ~/.claude/skills/<name>`.
- Skills are in the WIKI.md exclude list (they're code/tooling, not wiki content).
  This index exists for human reference, not wiki linking.
- The `marketingskills/` folder is a large parent skill that bundles many of
  the marketing sub-skills above. It has its own `skills/` subfolder with
  duplicated content.
