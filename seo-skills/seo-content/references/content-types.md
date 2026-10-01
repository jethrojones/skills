# Content-Type Catalog

Nine types. Each entry: **when to pick it**, the **structure**, the **quality bar** (word floor + must-haves), and the **schema**. The type is chosen in `opportunity-research.md` Step D from intent × SERP shape — this file tells you how to build it once chosen.

Internal-link minimums apply to every type: **≥3 in-body links** (mix of features, tools, sibling content, and ≥1 conversion page like `/pricing` or a relevant `/for/`), and **≥2 inbound** links from existing pages. No orphans.

---

## 1. Pillar guide

**Pick when:** broad commercial-investigation head term; top 10 are long, comprehensive pages; you want one authoritative hub that gates a cluster.

**Structure:** problem framing → mental model/framework → 4-6 "do this" sections → 2-3 "don't do this" / anti-patterns → an operational plan (week-by-week or step-by-step, measurable outcomes per step) → what success looks like. TOC with anchored sections.

**Quality bar:** ≥2,000 words (≥2,500 if the SERP leaders are that long). 8+ sections, none under ~250 words. Concrete numbers throughout. Counter-arguments addressed inline. Names what NOT to use, not just what to use. (If the repo already has a `/playbooks/` or similar long-form surface, ship it there and match that surface's existing structure — if `seo-sprint` is installed, its `references/patterns/playbooks.md` is the template.)

**Schema:** `Article` + `BreadcrumbList`. Add `FAQPage` if a Q&A section exists.

---

## 2. How-to / tutorial

**Pick when:** "how to X" query; top results are step-by-step; clear procedural intent. Often wins a featured snippet.

**Structure:** one-paragraph "what you'll accomplish + prerequisites" → numbered steps, each with what-to-do + what-done-looks-like → common-mistakes section → a worked example end-to-end → short FAQ. Lead with the snippet-able summary (a tight ordered list near the top) so Google can lift it.

**Quality bar:** ≥1,200 words. Every step independently actionable — no "configure it appropriately." Real commands/values/screenshots where the stack allows. If the task has branches (OS, plan tier), handle the top 2, not all of them.

**Schema:** `HowTo` (with `step` items) + `BreadcrumbList`. `FAQPage` for the FAQ.

---

## 3. Listicle / roundup

**Pick when:** "best X" / "X tools" / "top N" / "N ways to" query; top 10 are listicles. Highest-frequency commercial SERP shape.

**Structure:** intro stating the selection criteria (builds trust + differentiates) → the list, each item with a consistent mini-template (name, who it's for, standout strength, one honest limitation, price) → a short "how we picked" / methodology note → a decision-helper closing ("pick X if…, pick Y if…").

**Quality bar:** ≥1,500 words. **Include your own product honestly and in a defensible position** — not artificially #1; readers and Google both punish that. Each entry needs a real limitation (the honesty signal). Consistent fields across all entries. If you can't say something specific about an item, you haven't researched it.

**Schema:** `ItemList` + `BreadcrumbList`. `FAQPage` if present.

---

## 4. Definition / answer page

**Pick when:** "what is X" / "X meaning" / "X definition" query; snippet box present; short authoritative pages rank. Pure informational, top-of-funnel, AI-citation-friendly.

**Structure:** a 40-60 word direct definition in the **first paragraph** (snippet target) → expanded explanation → why it matters / when it applies → a concrete example → related terms (internal links) → short FAQ. Inverted-pyramid: answer first, depth after.

**Quality bar:** ≥600 words (depth signals authority even on short-answer queries, but don't pad). The opening definition must stand alone as a quotable answer. One clear example. This type is your best AI-citation surface — make the core claim quotable and sourced.

**Schema:** `Article` or `DefinedTerm` + `BreadcrumbList` + `FAQPage`.

---

## 5. Comparison

**Pick when:** "X vs Y" or multi-tool decision query; top results weigh options. High commercial intent.

**Structure:** TL;DR verdict up top (who should pick what) → comparison table (consistent dimensions) → dimension-by-dimension prose (don't just dump the table) → "pick X if / pick Y if" → honest note on where each genuinely wins. If it's *your product vs a single competitor*, prefer a programmatic `/compare/` page if the repo has that surface (and `seo-sprint`'s `references/patterns/compare.md` if installed). Use this editorial type for **neutral multi-tool** comparisons that don't fit a fixed template.

**Quality bar:** ≥1,200 words. Every compared option gets a fair, specific treatment. **The honesty rule:** name where each option genuinely wins. No straw-man competitors.

**Schema:** `BreadcrumbList` + `FAQPage`. `ItemList` if structured as a ranked set.

---

## 6. Data study / original research

**Pick when:** nobody in the SERP has original numbers; the topic is quantifiable; you want links + citations + AI mentions. The highest link-draw type — other writers cite data they can't get elsewhere.

**Structure:** headline finding up top (the quotable stat) → methodology (how you got the data — credibility gate) → findings, each a chart/table + interpretation → "what this means for you" → methodology footnote + a "cite this" block.

**Quality bar:** ≥1,500 words. **Real data with a real method** — your product's anonymized metrics, a survey you ran, or a defensible aggregation. If you can't source or generate genuine data, do not write this type (fabricated stats are a trust and ranking disaster). Each finding visualized + interpreted. Make it easy to cite (clear stat callouts, a citation line). If the `deep-research` skill is installed, hand the gathering to it; otherwise fan out the searches inline and verify each figure against a second source.

**Schema:** `Article` + `Dataset` + `BreadcrumbList`.

---

## 7. Resource / template library

**Pick when:** "X template" / "X examples" / "X checklist" / "X swipe file" query; users want a *usable asset*, not prose. ("Library" = a curated, browsable collection — templates, examples, prompts, snippets.)

**Structure:** brief intro on how to use the resource → the asset itself (templates/examples/checklist, copy-pasteable or downloadable) → short usage guidance per item → a CTA tying the resource to the product. The asset is the hero; prose is supporting.

**Quality bar:** ≥800 words of supporting copy *plus* a genuinely useful asset (≥5 examples/templates, or one substantial downloadable). The asset must be real and good — a thin template list loses to the one site that made a proper collection. If an interactive free tool would beat a static library here, flag that to the user (and use the `free-tool-strategy` skill if it's installed) — but still ship the library this run unless they redirect.

**Schema:** `ItemList` (or `HowTo` if step-templated) + `BreadcrumbList`.

---

## 8. Opinion / POV

**Pick when:** theme-led not keyword-led; low search volume but high authority + AI-citation + shareability value; you have a genuine contrarian or experience-backed thesis.

**Structure:** the thesis stated sharply up front → the conventional wisdom you're countering → your argument in 3-4 beats, each grounded in real experience/data → the strongest counter-argument, addressed honestly → what to do differently. Personal, first-person, opinionated.

**Quality bar:** ≥1,000 words. A real, defensible, non-obvious thesis — "you should do marketing well" is not a POV. Grounded in lived experience or data, not vibes. Addresses the best counter-argument (this is what separates a POV from a rant). This type lives or dies on the strength of the take; if the take is weak, pick a different piece.

**Schema:** `Article` + `BreadcrumbList`.

---

## 9. Case study / teardown

**Pick when:** "how [company] does X" / "[brand] strategy" / teardown intent; readers want a real example dissected.

**Structure:** what the subject does + why it's worth studying → the teardown in beats (what they did, what's clever, what's a mistake) → the extractable principles (the reusable lessons) → "how to apply this to your own [thing]" → tie to product. Use real, verifiable specifics — screenshots, real numbers, quotes.

**Quality bar:** ≥1,200 words. Concrete and verifiable — a teardown of a real thing with real details, not a hypothetical. Each observation yields a transferable lesson (otherwise it's gossip, not content). Fair to the subject. If teardown of a named competitor, keep the honesty rule: credit what they do well.

**Schema:** `Article` + `BreadcrumbList`.

---

## Cross-cutting requirements (all types)

- **Information gain (non-negotiable, every type):** the piece must contain ≥1 original element absent from the top 10 — proprietary data, first-hand testing, expert commentary, or a genuinely novel framework. This isn't only the data-study's job; it's the bar for *all* types under the 2026 core updates. The element comes from the research brief (`research-brief.md`) and is a hard ship gate (`quality-loop.md`).
- **Answer-engine optimization (every type):** lead with the answer, write self-contained quotable core claims, attribute + date every stat, cover the entity map, match the answer-intent bucket. Full layer in `aeo.md`.
- **Meta title** ≤60 chars, primary keyword near the front. **Meta description** ≤155 chars, keyword + hook. **Canonical** set. **One `<h1>`.**
- **Keyword placement:** in H1, title, first 100 words, and ≥2 H2s — naturally, never stuffed.
- **FAQ section** wherever the SERP shows a People-Also-Ask box; pull the actual PAA questions.
- **Internal links:** ≥3 in-body, ≥2 inbound, varied anchor text (`.seo/link-inventory.md`).
- **Voice:** governed by `.seo/brand.md` — voice tags, perspective, forbidden words.
- **E-E-A-T:** named author + credentials (`.seo/brand.md` Author section), first-hand framing where true, visible date stamp.
- **Schema** per type above; validate with `python scripts/tech_audit.py --schema <url>`.

**Verification note:** enforce the word floor with `python scripts/word_count.py <path> --min <floor>`. `scripts/link_audit.py` only knows the programmatic A-E page types, so use it with `--orphan-check` (to catch orphans) and count the ≥3 in-body / ≥2 inbound links by hand against the minimums above.
