# Output Formats — shipping file-based content into any stack

> **Is the site's content actually in files?** This file covers the **file-based** store — markdown/MDX/content-collection pieces committed to the repo. If content lives in a **database or headless CMS** (WordPress, Sanity, Contentful, Strapi, Payload, Ghost, a Rails/Django/Prisma model, Webflow, Notion-as-CMS…), start from `content-stores.md` instead — it owns the read/write/inbound-link flow for those, and points back here only if the store turns out to be files.

Editorial pieces (guides, how-tos, listicles, etc.) live wherever the site already publishes its blog/content. Your job is to **detect that surface, match its existing shape, and reuse its layout** — never to invent a new content system.

The golden rule: **find one existing published article, copy its file location + frontmatter shape + layout component exactly, and slot the new piece in beside it.** If the repo already publishes content, that existing piece is a more reliable spec than anything below.

---

## Step 1 — Detect the content surface

Run from the repo root. First match wins.

| Signal in the repo | Where editorial content usually lives |
|---|---|
| `astro.config.*` | `src/content/<collection>/*.md(x)` (Content Collections) — schema in `src/content/config.ts` |
| `package.json` has `next` + `app/` | MDX in `content/` or `src/content/`, or a `app/blog/[slug]/page.tsx` route reading from a data dir / CMS |
| `package.json` has `next` + `pages/` | `pages/blog/*.mdx` or a `posts/` markdown dir read at build time |
| `Gemfile` has `rails` (+ maybe `inertia_rails`) | a `Post`/`Article` model + DB, or markdown in `app/views`/`content`, or an Inertia page fed by a controller |
| `_config.yml` (Jekyll) | `_posts/YYYY-MM-DD-slug.md` with Jekyll frontmatter |
| `config.toml`/`hugo.*` (Hugo) | `content/blog/<slug>.md` with Hugo frontmatter |
| `gatsby-config.*` | markdown in `content/` sourced via `gatsby-source-filesystem` |
| `nuxt.config.*` | `content/` (Nuxt Content) markdown |
| `svelte.config.*` (SvelteKit) | `src/routes/blog/<slug>/+page.md(svx)` or a posts dir |
| None / unknown | **Markdown fallback** (below) — emit portable markdown and tell the user where to wire it |

Confirm the guess by actually finding an existing post: `git ls-files | grep -iE 'blog|posts|articles|content|guides'`. If you find one, **its real path and frontmatter win over this table.** Persist the resolved location to `.seo/config.json` (e.g. `"content_dir"`, `"content_layout"`) so the next run starts warm.

If two surfaces are plausible (e.g. both `app/` and `pages/`, or a separate marketing repo), ask once with `AskUserQuestion` rather than guessing.

---

## Step 2 — Match the frontmatter

Read an existing post's frontmatter and reproduce its exact keys. Don't add fields the site's schema doesn't have (it'll fail the build), and don't drop ones it requires. Typical editorial fields:

```yaml
---
title: "..."                 # the H1 / display title
slug: "..."                  # lowercase, hyphenated, 2-5 words
description: "..."           # meta description, ≤155 chars
date: 2026-01-15             # published date (match the site's key: date / pubDate / publishedAt)
updated: 2026-01-15          # if the site tracks it
author: "..."                # if the site has authors
tags: ["..."]                # if the site uses them
canonical: "https://..."     # canonical URL
image: "..."                 # OG/hero image (see images note below)
---
```

Whatever the site's existing schema is, **match it.** If it uses `pubDate`, use `pubDate`. If posts carry a `category` enum, pick a valid value. The build is the test — a frontmatter mismatch is a hard failure, not a style nit.

---

## Step 3 — Reuse the layout, emit the SEO surface

- **Layout:** render through the **existing** blog/article layout component. Do not create a new template. If the layout already emits `<title>`, meta description, canonical, and OG tags from frontmatter, just populate those fields. If it doesn't, add the meta/canonical/OG and JSON-LD `<script type="application/ld+json">` block inline in the content or via the layout's head slot — match how other pages do it.
- **Schema (JSON-LD):** emit the type the piece requires (`Article`, `HowTo`, `FAQPage`, `ItemList`, `Dataset`, `BreadcrumbList` — per `content-types.md`). Validate with `scripts/tech_audit.py --schema <url>` once rendered.
- **TOC / anchors:** if the layout auto-generates a TOC from headings, just write clean `##`/`###` structure. If not and the piece is ≥1,500 words, add an anchored TOC the way existing long posts do.
- **Images:** specify what's needed (hero/OG at 1200×630, any inline diagrams) but don't fabricate them. If the `og-image` or `feature-image` skills are installed, hand off image generation to them; otherwise leave a clearly-marked placeholder path and note it in the handoff so the user supplies the asset.

---

## Markdown fallback (no detectable content surface)

If the stack has no content system yet, emit a single portable markdown file with complete frontmatter and **tell the user where to wire it in.** Don't try to build a CMS.

```
content/blog/<slug>.md
```

```yaml
---
title: "..."
slug: "..."
description: "..."
date: 2026-01-15
canonical: "https://example.com/blog/<slug>"
schema: [Article, FAQPage]      # which JSON-LD the renderer should emit
---

# <H1 with primary keyword>

...body...
```

Hand-off note to include:

> I wrote the piece as portable markdown at `content/blog/<slug>.md`. Your site doesn't have a content pipeline I could detect, so you'll need to render it once — most frameworks read a markdown dir with a few lines of config (Hugo/Jekyll/Eleventy: drop it in their posts dir; Next/Astro/Nuxt: point a content loader at the folder). After that first wiring, every future piece is just another file here.

---

## Verify the output rendered

After writing, confirm the page actually builds and emits one H1:

- Rebuild the site (or run the dev server) and load the new URL.
- `grep -c '<h1' <build-output path>` → must be exactly 1.
- Run the schema check: `python scripts/tech_audit.py --schema <url>`.

A piece that doesn't render is not shipped. Don't report success on an unbuilt draft.
