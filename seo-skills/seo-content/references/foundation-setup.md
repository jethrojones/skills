# Foundation Setup — bootstrap the `.seo/` foundation (Step 0)

`seo-content` writes against a small shared foundation in `.seo/`. This file is how it **creates that foundation itself** on a bare repo — no `seo-sprint` required. If `seo-sprint` has already run, the foundation exists and this whole step is a no-op: reuse what's there, don't overwrite it.

Run this once, at the very start of a run, before selection (Step 1). It's fast — most of it is auto-detected; only the brand voice needs a short interview.

---

## The decision: reuse or create

Check what exists, act per file. **Never overwrite an existing foundation file** — that's the coexistence guarantee (a user who's been running `seo-sprint` loses nothing).

| File | If it exists | If it's missing |
|---|---|---|
| `.seo/config.json` | Reuse | **Create** (§1) |
| `.seo/brand.md` | Reuse | **Create** (§2) — the only step needing user input |
| `.seo/keyword-research.json` | Reuse (re-query stale slices as needed) | **Create** a baseline (§3); the rest accretes during selection |
| `.seo/link-inventory.md` | Reuse + append | **Create** from git (§4) |
| `.seo/content-ledger.md` | Reuse | Created in Step 5 from `assets/content-ledger-template.md` (already handled) |
| `docs/seo-sprint.md` | Read as dedup input | Skip — fall back to a `git ls-files` scan for the exclusion set |

If only *some* files exist (a partial or aborted setup), fill the gaps — don't restart from scratch.

State up front which mode you're in: *"Found an existing `.seo/` foundation — reusing it."* or *"No foundation here yet — I'll set one up (takes one short brand interview, then I'll write the first piece)."*

---

## §1 — `.seo/config.json` (auto-detected)

Detect the stack **and the content store** — first decide *where published content lives* per `references/content-stores.md` (files vs. headless CMS vs. app DB vs. WordPress vs. builder), then, if it's files, the content surface per `references/output-formats.md`. Persist the `content_store` block (see `content-stores.md`) alongside the rest:

```json
{
  "domain": "https://example.com",
  "stack": "astro",
  "language": "mdx",
  "content_dir": "src/content/blog",
  "content_layout": "src/layouts/BlogPost.astro",
  "output_url_prefix": "/blog",
  "ahrefs_project_id": null,
  "keyword_tool": "ahrefs | dfs | none"
}
```

- `content_dir` / `content_layout` / `output_url_prefix` come from finding one existing published post (the real path always wins over the guess).
- `domain` — read from the deployed site, `package.json` `homepage`, a sitemap, or ask once.
- `ahrefs_project_id` — if a keyword tool is connected and a project ID is needed (`gsc-*`), prompt once and store it. Leave `null` otherwise.
- If a value can't be auto-detected and isn't essential yet, leave it `null`; fill on first need.

---

## §2 — `.seo/brand.md` (the one interactive step)

This is the quality-critical file. Do it the way `seo-sprint` does: **read every signal first, draft the file, then ask only about the gaps.** Don't open with a blank questionnaire.

### Read these signals first
- `CLAUDE.md`, `README.md` — product name, one-liner, audience hints
- `package.json` / `Gemfile` — framework (already in config)
- the pricing page (any path) — plan structure, price points, free tier
- homepage / marketing hero (`git ls-files | grep -iE 'index|home|hero|marketing|landing'`) — existing positioning + voice
- **1-2 existing published posts** (`git ls-files | grep -iE 'blog|guides|content|articles'`) — read them closely; this is where the *real* voice lives. Note rhythm, perspective, formality, how they open.
- `tailwind.config.*` / token CSS — accent color/fonts (auto-fill Visual brand only if trivial; otherwise skip it)

### Then ask the gaps — one `AskUserQuestion` batch (3-4 questions)
Only ask what you couldn't infer. The essentials to end up with:
- **Product one-liner** (≤20 words) — usually inferable; confirm it
- **Primary persona** — who you're writing for
- **3-7 competitors** — by name (seeds content-gap research + comparison/listicle pieces)
- **Brand voice tags** + **forbidden words** — the non-negotiable core. If existing content gives you the voice, propose tags and ask "does this sound right?" rather than asking cold.
- **Free tier?** and **anti-positioning** (what you intentionally don't do) — for honest comparison/listicle sections
- **Concrete differentiators** — what you do that competitors don't (for weaving the product in naturally)
- **Proprietary data & first-hand experience** — what original data / testing / lived experience the product can draw on. **This is the information-gain moat** that the 2026 core updates reward; without it, pieces default to synthesis. Worth asking explicitly.
- **Default author + credentials** — who bylines the content and why they're credible (E-E-A-T + AI-citation signal)

Write the result to `.seo/brand.md` from `assets/brand-template.md`. Skip the Visual brand section unless it auto-filled — editorial content reuses existing layout components and doesn't need it.

**Quality bar:** the voice section must be specific enough that a piece written from it is indistinguishable from the site's existing content. Vague tags ("professional, friendly") fail this — push for the specific, e.g. "blunt, technical, allergic to hype, writes like a founder DMing a peer."

---

## §3 — `.seo/keyword-research.json` (baseline now, rest later)

You don't need full keyword research up front — selection (Step 1) does live research every run and persists it here. Establish just the **baseline** so the winnability cap works:

- Pull domain rating (DR) per `references/research-recipes.md` (Ahrefs/DFS mode), or estimate it in the Ahrefs-free fallback. Store it: this caps targets at **KD ≤ DR + 10**.
- If no keyword tool is connected at all, write `{"baseline": {"domain_rating": null, "source": "none"}}` and proceed — selection will run in fallback mode and the user can refine later.

Seed shape:

```json
{
  "baseline": { "domain_rating": 18, "source": "ahrefs", "as_of": "<date>" },
  "clusters": {},
  "candidates": []
}
```

The `clusters`/`candidates` fill in as selection runs accumulate research. No reduction in quality — the depth lands exactly where it's used.

---

## §4 — `.seo/link-inventory.md` (generated from git **or sitemap**)

Build the inventory of existing link targets — same as `seo-sprint` Step 6, just sourced by you:

- **File-based content** →
  ```
  git ls-files | grep -iE 'features?|tools?|pricing|about|blog|guides|content|articles|index|home'
  ```
  Capture each page's URL + a title/anchor candidate (read the file's H1 or frontmatter title).
- **DB / CMS content** → source from the **sitemap** (`/sitemap.xml`) or the CMS API instead (see `content-stores.md` Operation 1). Same template, different source.

Sort the results into the sections of `assets/link-inventory-template.md`: homepage/core marketing, features, tools, existing content. This gives the first piece real internal-link targets; every run appends to it.

---

## After setup: proceed, don't stop

`seo-sprint`'s Initialize stops for human review because it's about to execute a whole roadmap. This is lighter — you've created a foundation, not a plan. **Flow straight into Step 1 (selection)** in the same run so the user gets their piece. Note in the hand-off that the foundation was bootstrapped and the user can edit `.seo/brand.md` anytime to tune the voice.

Tell them once, in the hand-off, what the upgrade path is:

> Set up a fresh `.seo/` foundation (brand, config, link inventory) and wrote your first piece against it. Edit `.seo/brand.md` anytime to refine the voice. If you later want the full programmatic-SEO machine (alternatives/comparison/use-case pages, technical audit, off-page checklist), `seo-sprint` builds on this same foundation — no rework.
