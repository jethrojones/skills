---
name: seo-content
description: "When the user wants to produce the next piece of search-optimized content for a site — a content engine that bootstraps its own brand + keyword foundation on first run (no other skill required) and then, each run, researches what to write next, picks the content TYPE (guide, how-to, listicle, comparison, definition, data study, resource/template library, opinion, case study), and ships one deeply-researched, on-brand, in-voice, SEO-optimized piece. Use when the user says 'write the next piece,' 'what should I publish next,' 'content engine,' 'feed the blog,' 'make a new SEO article,' 'next content,' 'write a guide/how-to/listicle/comparison,' 'create new content,' or re-runs after /seo-sprint laid the groundwork. Distinguish from seo-sprint (executes a fixed programmatic-page roadmap phase by phase), content-strategy (plans topics but doesn't write), and blog-article (writes one arbitrary post with no opportunity research or dedup ledger). This skill OWNS the loop: decide-what-and-which-type → deep research → write → verify → register, one publishable piece per invocation."
---

# SEO Content

A content engine. Each invocation produces **one** publishable, deeply-researched, on-brand, in-voice, SEO-optimized piece — and, critically, **decides for itself what that piece should be and what type it should take.** Run it again and it picks the next-best piece. The research that answers "what do I write next?" is the skill's core job, not a step the user does first.

It runs on a small foundation in `.seo/` (brand voice, stack config, link targets, keyword data). **This skill sets that foundation up itself on first run** — drop it into a bare repo and it bootstraps everything it needs (see Step 0). If you've already run `seo-sprint`, that same foundation is already there and this skill just reuses it. Either way, no external skill is required.

The user never specifies a topic or type unless they want to. The default contract is: **"go figure out the best next thing to publish and publish it."**

---

## Relationship to its siblings

| Skill | Owns |
|---|---|
| **seo-sprint** | A *fixed roadmap* of programmatic pages (alternatives/compare/for/playbooks) + technical audit + off-page checklist, executed phase by phase. Optional sibling, **not a prerequisite** — if it's run, the two share the same `.seo/` foundation; if not, this skill builds its own. |
| **seo-content** (this) | The *open-ended editorial loop*. Re-decides the single best next piece every run, chooses its type dynamically, writes it deep. No fixed roadmap — the backlog is regenerated from live data each run. |
| **content-strategy** | Planning only — clusters and calendars. Hands the "what" to this skill; this skill also does its own selection if no plan exists. |
| **blog-article** | Writes one arbitrary post you hand it. No opportunity research, no type selection, no dedup ledger. This skill *can* hand off the actual prose to it but owns everything around it. |

This skill is **fully self-contained**: it bundles its own verification scripts (`scripts/`), its own research + output + setup references (`references/`), and its own foundation templates (`assets/`). It depends on **no other skill.** The `.seo/` foundation it reads is one it creates itself (Step 0) when absent, or reuses untouched when `seo-sprint` already made it — the two coexist on a shared foundation with zero conflict. The augmenting skills below are pure upside when present, never required.

---

## Operating model — one run, one session, one PR

Run this **fresh each time: new chat session, new branch, one PR per piece.** Do **not** loop it repeatedly inside one long session.

The skill is deliberately **stateless across runs**. Everything that must persist between pieces — what's shipped, the scored backlog, the link inventory — lives in the `.seo/` files, not in the conversation (the same reason seo-sprint keeps its roadmap as a doc). So a fresh session loses nothing: it reads those small files and starts warm.

A single run pulls heavy research — full SERP scrapes of 5-10 competitor pages, primary sources, the draft itself. The Step 2 fan-out keeps most of that in *subagents*, so the main thread carries the distilled brief, not the raw piles — but the draft, the brief, and the critique loop still add up. By the third piece in one session you're diluting attention and re-reading stale context. Fresh session = each piece gets clean attention against `.seo/brand.md`, and each PR is an independently reviewable, revertable unit. The only cost is re-reading the small `.seo/` foundation files at the start — cheap, and the point.

**Parallel throughput:** because state is file-based, you can run several pieces at once in separate git worktrees. The only write-contention is the append-only `.seo/content-ledger.md` and `.seo/link-inventory.md` — resolve any merge conflict by keeping both rows. Sequential is simpler; reach for worktrees only when you specifically want volume.

---

## Prerequisites

Only two, and the second one this skill can satisfy itself:

1. **Working directory is a git repo** — `git rev-parse --is-inside-work-tree`. If not, stop: "Run me from inside the repo where your site lives."
2. **A `.seo/` foundation exists — or gets bootstrapped.** Check for `.seo/config.json` and `.seo/brand.md`. If present (you ran `seo-sprint`, or a prior `seo-content` run set them up), reuse them. If missing, **Step 0 creates them** — don't stop, don't tell the user to go run another skill.

At the start of a run, check what's connected — ping `mcp__ahrefs__subscription-info-limits-and-usage` (or look for `mcp__dfs-mcp__*`) and note the **Tools & environment** table below. Adapt to what's present; never refuse for a missing tool.

Read once, up front, every run (after Step 0 has ensured they exist):
- `.seo/brand.md` — voice tags, persona, anti-positioning, differentiators, forbidden words. **Everything you write is governed by this file.**
- `.seo/config.json` — stack, content surface, keyword-tool `project_id`, output paths.
- `.seo/link-inventory.md` — internal link targets.
- `.seo/keyword-research.json` — DR baseline + cached keyword data (treat as stale if >90 days; re-query the slice you need).
- `.seo/content-ledger.md` — **what you've already shipped + the scored backlog.** If it doesn't exist, create it from `assets/content-ledger-template.md` on this run. This is how "run me again for the next piece" works without repeating yourself.
- `docs/seo-sprint.md` if present — so you don't write editorial content that duplicates a programmatic page.

---

## Tools & environment (none required — better with, fine without)

The skill detects what's available and adapts; nothing here is a hard dependency. Connect what you can for higher-quality output.

| Tool / capability | What it unlocks | Without it |
|---|---|---|
| **Ahrefs MCP** *(or **DataForSEO MCP**)* | Real keyword volume/KD, DR baseline, SERP overviews, content-gap, GSC striking-distance, AI-citation gaps — the selection + winnability math | Ahrefs-free fallback: web search + SERP scraping + estimated ranges (`research-recipes.md`) |
| **firecrawl** *(skill or MCP)* | Robust SERP teardown, JS-rendered page extraction, sitemap reads for DB/CMS sites | `WebSearch` + `WebFetch` — works, weaker on SPA-rendered pages |
| **`WebSearch` / `WebFetch`** | Baseline research, fact verification, primary-source hunting — the floor for Step 2 | (usually always present) |
| **Subagent fan-out** *(Agent/Task tool)* | Parallel research in Step 2 + parallel critics in Step 4; keeps the main context clean | Run the angles/critics sequentially — same coverage, slower |
| **Content-store write access** *(CMS API/CLI/MCP — WordPress REST, Sanity CLI, Notion MCP…)* | Create the piece as a **draft** directly in the CMS/DB | Hand off a ready-to-paste artifact + field map (`content-stores.md`) |

For *skill*-level add-ons (`deep-research`, `blog-article`, `og-image`…) see **Optional augmenting skills** below.

---

## The run (one piece per invocation)

### Step 0 — Foundation: reuse or bootstrap

Full method in `references/foundation-setup.md`. If `.seo/config.json` + `.seo/brand.md` already exist, this is a no-op — reuse the foundation untouched (the coexistence guarantee: a `seo-sprint` user loses nothing). If they're missing, set them up from the repo: auto-detect config (§1), draft brand context from repo signals + one short `AskUserQuestion` interview (§2), establish the DR baseline (§3), and generate the link inventory from `git ls-files` (§4). Then flow straight into Step 1 in the same run — bootstrapping a foundation is light enough that it doesn't need its own review stop. **Never overwrite an existing foundation file.**

Then five steps. Step 1 is the one interactive checkpoint (the selection); the rest run through, with Step 4 looping internally until the gates pass.

### Step 1 — Select: decide WHAT and WHICH TYPE

This is the part the user is paying for. Full method in `references/opportunity-research.md`. The shape:

1. **Read what's already covered** — the content ledger + existing pages (file sites: `git ls-files | grep -iE 'blog|guides|content|articles'`; DB/CMS sites: the sitemap or CMS API, per `references/content-stores.md`), plus the `docs/seo-sprint.md` roadmap if it exists. Build an exclusion set. Never propose something already shipped or already a programmatic page.
2. **Regenerate the opportunity pool** from live signals (don't trust a stale backlog blindly):
   - **Keyword/topic gaps** — content-gap (keywords competitors rank for and you don't), question + matching-terms sweeps around your clusters, related-terms. Recipes in `references/research-recipes.md`. Filter to **KD ≤ DR + 10** — the winnability rule: while your domain rating is still climbing, anything harder than DR+10 is a doomed target (read current DR from `.seo/keyword-research.json`).
   - **Striking distance** (existing sites) — `gsc-keywords` positions 5-20 with no dedicated page. A new focused piece often captures these faster than boosting.
   - **AI-citation gaps** — questions in your space that LLMs answer *without* citing you. Use `mcp__ahrefs__brand-radar-*` or `mcp__dfs-mcp__ai_optimization_*` if available. Content that fills these is high-leverage AI surface area.
   - **Freshness / timely** — anything seasonal, newly-launched, or recently-shifted in the space.
3. **Score** each candidate (rubric in `references/opportunity-research.md`): winnability (KD vs DR), traffic potential, conversion intent, strategic value (authority / links / AI-citation), and effort. Produce a ranked shortlist.
4. **Pick the TYPE for the top candidate.** Type is dictated by **search intent × SERP shape × strategic goal**, not by preference. Run a SERP overview (`serp-overview` or scrape the top 10) and read what format Google already rewards. Full type catalog + selection logic in `references/content-types.md`. Types: pillar guide, how-to/tutorial, listicle/roundup, definition/answer page, comparison, data study/original research, resource/template library, opinion/POV, case study/teardown.
5. **Checkpoint (`AskUserQuestion`).** Present the **top 3 candidates** with their numbers and the proposed type for each:
   > "Next piece — my pick: **[title]** as a **[type]**. Keyword '[kw]' — vol X, KD Y (you're DR Z, winnable), intent [commercial/info], top-10 SERP is [N listicles / M how-tos]. Why this type: [one line]. Runners-up: [#2], [#3]."
   Options: "Write my pick" / "Write #2" / "Write #3" / "Different angle (tell me)". The user's gut on positioning beats the data — let them redirect.

Persist the full scored shortlist to the **Candidate backlog** section of `.seo/content-ledger.md` so the next run starts warm.

### Step 2 — Research → verified brief: the substance

Quality is decided here. As of the **March 2026 core update**, the dominant signal is *information gain* — what this piece knows that the top 10 don't — and every claim must be grounded in a verified source. Full method in `references/research-brief.md`. The shape:

1. **Fan out six research angles** — SERP teardown (table-stakes + the gap), primary sources/studies, statistics, contrarian/counter-evidence, product/first-hand data, and the entity/topical map. **Spawn these as parallel subagents where the host supports it** (Agent/Task tool, or `deep-research` if installed); otherwise run them sequentially. Same coverage either way.
2. **Synthesize a research brief** — a **claim ledger** (every claim + source + tier + date), an **entity-coverage map**, the **information-gain statement** (the specific original-data / first-hand / expert / novel-framework element absent from the top 10), and the angle. *If you can't state the information gain concretely, stop and loop back to Step 1 — the piece won't rank.*
3. **Verify in a separate pass** — independently cross-check every claim against a 2nd source (don't let the gatherer be the only verifier). `unverified` claims get re-researched, bracketed, or cut. Never ship a fabricated or single-sourced statistic as fact.

The output is a verified brief; Step 3 writes *from* it. Pull internal-link targets from `.seo/link-inventory.md` here too. Save the brief to `.seo/briefs/<slug>.md` for auditability.

### Step 3 — Write: on-brand, in-voice, SEO + answer-engine optimized

Write *from the brief*, not from memory. Full craft spec in `references/writing.md`; answer-engine layer in `references/aeo.md`. Non-negotiables:

- **Deliver the information gain.** The original-data / first-hand / expert / framework element from the brief must land *in the body*, concretely. This is what makes the piece worth ranking in 2026.
- **Voice from `.seo/brand.md`** — voice tags, perspective (I/we/you), and the **forbidden words list**. Match the project's existing content, don't impose a generic blog voice.
- **Type-specific structure** — follow the outline + quality bar for the chosen type in `references/content-types.md`.
- **Answer-engine optimization** (`references/aeo.md`) — lead with the answer; write self-contained, quotable core claims; attribute + date every stat; cover the entity map; match the answer-intent bucket. This is how you get cited by ChatGPT/Perplexity/AI Overviews/Claude, now a primary distribution channel.
- **On-page SEO** — keyword in H1 + title, variants in H2s, slug rules, meta title (≤60) + description (≤155), TOC for long pieces, FAQ from the real PAA set, and the schema the type requires (`Article`, `HowTo`, `FAQPage`, `Dataset`, `ItemList`, `BreadcrumbList`).
- **E-E-A-T signals** — named author + credentials (from `.seo/brand.md`), first-hand framing ("in our data," "when we tested"), and a visible date stamp.
- **Internal links** — per-type minimums *in the body*, varied anchor text per `.seo/link-inventory.md`.
- **Output target** — match the site's **content store** (`references/content-stores.md`): files in the repo, a headless CMS, an app DB, WordPress, or hand-off. For file stores, reuse the existing layout per `references/output-formats.md` (markdown fallback included) and don't invent a new one; for DB/CMS, render the body in the store's format (HTML / markdown / portable text). Either way, never auto-publish.

### Step 4 — Quality loop + gates

Not one-shot. Full method in `references/quality-loop.md`: a critic panel scores the draft, you revise the weakest dimensions (bounded to **two rounds**), then hard gates decide whether it ships.

1. **Critic panel** (run as *separate* passes/subagents from the writer): skeptic/fact-check, information-gain, AEO/extractability, voice, completeness. Each scores 1-5 + specific misses; any axis ≤3 is a revise target. For the voice axis, run the bundled polish pass (`references/polish-pass.md`).
2. **Revise** the weakest dimensions — bias toward adding substance (a missing source, the under-delivered data point, an uncovered entity) over reshuffling words. Re-run the critics that failed.
3. **Hard gates — all must pass to ship:**
   - **Information gain** present in the body (the 2026 gate that matters most — dressed-up synthesis fails).
   - **Citation coverage** — every claim traces to the verified ledger; no unverified claim as fact; no fabricated stats.
   - **AEO-readiness** — extractable answer, quotable claims, entity map covered, schema emitted, date stamped.
   - **Deterministic** — `word_count.py --min <floor>`, `link_audit.py --orphan-check` (+ hand-confirm ≥3 in-body/≥2 inbound), `tech_audit.py --schema <url>` if rendered.
   - **Voice** — brand match + forbidden-words grep clean.

A failing gate is information, not blame — it points at a thin section, a missing source, or a forgotten schema block. If a gate still fails after two rounds, the piece was likely mis-selected; say so rather than shipping under-spec.

### Step 5 — Register + hand off

**Publish the piece into the content store** (`references/content-stores.md`): write the file (file stores), create a **draft** entry via CLI/API/MCP (CMS/DB, if a write path is configured), or hand off the rendered body + field map (the safe default). **Never auto-publish.** Then, in the same batch:

- **Append to `.seo/content-ledger.md`** — a `shipped` row (date, type, title, slug, target keyword, primary internal links). This is the dedup record the *next* run reads.
- **Update `.seo/link-inventory.md`** — register the new page as a future link target + 4-5 anchor-text variants.
- **Add the inbound links (no orphans)** — file stores: edit ≥2 existing pages. DB/CMS: emit an inbound-link **punch-list** (2 existing posts + anchors) for the user, or update them via API as drafts if a write path is configured.
- **Keep the verified brief** at `.seo/briefs/<slug>.md` — the citation record behind the piece (auditable, and reusable if you ever update the piece).
- If `docs/seo-sprint.md` has a content section, note the new piece there.

Then hand off (do **not** auto-commit):

```
✓ Shipped: [title]  ([type])

  Target:   "[keyword]"  (vol X, KD Y, you're DR Z)
  Piece:    <content file>  — OR — CMS draft at <preview URL>  — OR — ready-to-paste artifact + field map
  Inbound:  <2 existing pages edited>  — OR — punch-list: link from [post-1], [post-2]
  State:    .seo/content-ledger.md (shipped row) · .seo/link-inventory.md (registered + anchors) · .seo/briefs/<slug>.md (claim ledger)

Quality gates:
  ✓ Information gain: [the original element — e.g. "our anonymized data on X, n=1,200"]
  ✓ Citations: 14 claims, all verified (9 primary sources)
  ✓ AEO: lead-answer + 5 quotable claims, entity map covered, FAQPage + Article schema, dated
  ✓ Words: 1,840 / 1,500 min ([type] floor)
  ✓ Internal links: 4 in-body, 2 inbound
  ✓ Voice: matches brand.md, forbidden-words clean

Suggested commit: "content: [title]"

Next up (from backlog): [#2 title] ([type]) · [#3 title] ([type])
Run me again for the next piece.
```

---

## Interactive principles

Same ethos as seo-sprint — you're a collaborator across many runs, not a content mill.

- **Ask before you guess** at the *selection* checkpoint, then run through. Surface the top 3 with numbers; let the user's positioning instinct override the data.
- **Show the data.** "Targeting '[kw]' — vol 400, KD 12, you're DR 20, top-10 is 6 thin listicles we can beat. Writing it as a data study because nobody in the SERP has original numbers." Concrete > assertion.
- **Be honest about what won't rank.** If the best candidate is still KD 60 at DR 10, say so and offer the closest winnable angle. Don't write doomed pieces to look busy.
- **One piece per run.** Resist scope creep into "and I'll also write three more." Ship one, register it, hand off. The loop is the feature.

---

## Anti-patterns (do NOT do these)

- **Don't write without information gain.** A piece that only restates the top 10 — however well — is invisible under the 2026 core updates. If the brief can't name a concrete original element (data / first-hand / expert / novel framework), loop back to Step 1. This is the hardest, most important rule.
- **Don't let the writer be its own verifier.** Claims are gathered in one pass and confirmed in a *separate* one. A model grading its own facts rubber-stamps them.
- **Don't skip the AEO layer.** If the core claims aren't extractable and attributed, you forfeit AI-citation traffic — now a primary channel, not a bonus.
- **Don't repeat the ledger.** Always read `.seo/content-ledger.md` first. Re-shipping a covered topic (or duplicating a programmatic page) wastes the run and cannibalizes rankings.
- **Don't ignore the SERP when picking type.** "How to X" where the top 10 are all listicles means Google wants a listicle, not a tutorial. Type follows the SERP, not your preference.
- **Don't impose a generic blog voice.** Read existing content and `.seo/brand.md`; match it. Forbidden words are forbidden.
- **Don't ship orphans.** Every piece needs ≥2 inbound links from existing pages, added the same run.
- **Don't target KD > DR + 10** while DR is still climbing. Harder keywords won't rank yet no matter how good the piece is.
- **Don't auto-commit.** Show the diff summary; let the user drive git.
- **Don't fabricate data.** Real numbers with sources, or clearly-bracketed ranges the user can verify. Inventing statistics is the fastest way to lose trust and get the page penalized. (This includes faking first-hand experience — an invented failure or client to *sound* authentic is the same sin.)
- **Don't optimize for AI detectors.** The goal is genuine E-E-A-T quality, not a passing "AI-detector" score. Google rewards helpful content regardless of how it's produced and doesn't rank on detection; chasing detector scores — or injecting cosmetic imperfections to "seem human" — is wasted effort and often counterproductive. Build citation-worthy content and detection is irrelevant.

---

## Optional augmenting skills

This skill does the whole job on its own. If any of these are also installed, it produces a *better* result by handing the relevant slice off — but if they're absent, do the work inline and just mention the skill once in the hand-off so the user knows the upgrade exists. Never block on a missing skill.

| Skill | If present | If absent (do this inline) |
|---|---|---|
| `deep-research` | Hand it Step 2's research fan-out + the separate verification pass — multi-source gathering and independent fact-checking are exactly its job | Run the six research angles yourself (parallel subagents if the host supports them, else sequential); verify each claim against a second source |
| `blog-article` | Optional second drafting pass for a long pillar guide's prose | Write the prose inline (the default) |
| `og-image` / `feature-image` | Generate the hero/OG image | Specify the image (1200×630) and leave a marked placeholder for the user |
| `free-tool-strategy` | When a resource piece would work better as an interactive tool, plan it there | Ship the static resource/template library |
| `content-strategy` | If the user already has a topic plan from it, read it as input to selection | Do your own selection from live signals (the default) |
| `seo-sprint` | Shares the same `.seo/` foundation (no setup needed); hand it striking-distance *boosts* and programmatic `/alternatives`,`/compare`,`/for` pages | Bootstrap the foundation yourself (Step 0); note any boost/programmatic opportunity in the hand-off as an optional upgrade. This skill ships standalone editorial pieces regardless. |

---

## File map

| File | Purpose |
|---|---|
| `references/opportunity-research.md` | How to decide WHAT next + WHICH TYPE — gap recipes, scoring rubric, type-selection logic |
| `references/content-types.md` | The content-type catalog: when to pick each, structure + quality bar + schema per type |
| `references/research-brief.md` | **Step 2** — multi-agent research fan-out → verified brief (claim ledger, entity map, information-gain statement) + separate fact-check pass |
| `references/writing.md` | **Step 3** — write from the brief: on-brand/in-voice craft + on-page SEO + AEO/E-E-A-T hooks |
| `references/aeo.md` | Answer-engine optimization — intent buckets, extractable formatting, entity/topical coverage, freshness, platform notes |
| `references/quality-loop.md` | **Step 4** — recursive critic panel + revise loop + the hard ship gates (information gain, citations, AEO, deterministic, voice) |
| `references/polish-pass.md` | Bundled final-edit pass — AI-tell list, em-dash decision tree, voice pass, skeptical pass (adapted from the `polish` skill) |
| `references/research-recipes.md` | Selection-research calls — Ahrefs/DFS mode + Ahrefs-free fallback (content-gap, SERP, GSC, AI-citation) |
| `references/content-stores.md` | Where content lives + how to publish to it across **files, headless CMS, app DB, WordPress, builder/manual** — the read / write / inbound-link flow for non-file stores |
| `references/output-formats.md` | The **file-based** store in detail: detect the content surface, match frontmatter, reuse layout, emit schema — incl. markdown fallback |
| `references/foundation-setup.md` | **Step 0** — bootstrap (or reuse) the `.seo/` foundation: config detection, brand interview, DR baseline, link inventory |
| `scripts/word_count.py` | Word-count gate |
| `scripts/link_audit.py` | Internal-link + orphan gate |
| `scripts/tech_audit.py` | Schema validation |
| `assets/content-ledger-template.md` | `.seo/content-ledger.md` skeleton (shipped log + scored backlog) |
| `assets/brand-template.md` | `.seo/brand.md` skeleton (voice contract) — coexistence-compatible with `seo-sprint` |
| `assets/link-inventory-template.md` | `.seo/link-inventory.md` skeleton (internal link targets) |
| **The `.seo/` foundation (data — bootstrapped by Step 0, or reused from `seo-sprint`)** | |
| `.seo/brand.md`, `.seo/link-inventory.md`, `.seo/keyword-research.json`, `.seo/config.json` | Brand voice, link targets, keyword data + DR baseline, stack config — read at the start of every run |
| `.seo/content-ledger.md`, `.seo/briefs/<slug>.md` | Dedup ledger + scored backlog; per-piece verified claim ledger (written each run) |
