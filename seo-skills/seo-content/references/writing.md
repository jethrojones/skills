# Writing — on-brand voice, on-page SEO, answer-engine optimization

Covers Step 3 of the run — turning the verified research brief into prose that's *on-brand*, *technically optimized*, and *citable*. The type's structure comes from `content-types.md`; the research + the angle come from `research-brief.md` (Step 2); the answer-engine layer is in `aeo.md`.

**Write from the brief, not from memory.** Every factual claim in the draft must trace to the brief's verified claim ledger. The brief also hands you the table-stakes coverage, the entity map to cover, and — most importantly — the **information-gain element**: the original-data / first-hand / expert / novel-framework thing that's in none of the top 10. Your first job in Step 3 is to make that element land concretely in the body. A piece that doesn't deliver its information gain is dressed-up synthesis and won't rank under the 2026 core updates.

---

## On-brand, in-voice (Step 3)

`.seo/brand.md` is the contract. Before writing, internalize:
- **Voice tags** (e.g. "honest, technical, no-jargon, founder-led") — these set diction and stance.
- **Perspective** — I / we / you. Match it consistently.
- **Forbidden words/phrases** — hard ban. Grep your draft for them before finishing.
- **Tone references** — brands whose voice the user wants to echo.

Also read 1-2 existing pieces of the site's content (`git ls-files | grep -iE 'blog|guides|content'`) and **match their rhythm** — sentence length, formality, how they open, whether they use headers as questions or statements. The goal is that a reader can't tell this piece was written in a different session from the rest of the site.

---

## On-page SEO (Step 3)

Mechanical, non-negotiable:

- **Title tag** ≤60 chars, primary keyword near the front.
- **Meta description** ≤155 chars, keyword + a conversion hook.
- **Slug** — lowercase, hyphenated, 2-5 words, matches common phrasing of the keyword.
- **One `<h1>`** containing the primary keyword. **H2s** carry variants and PAA questions — naturally.
- **Keyword in the first 100 words.** Don't bury the lede.
- **TOC with anchored sections** for anything ≥1,500 words.
- **FAQ** built from the real People-Also-Ask box when the SERP shows one.
- **Schema** per the type (`content-types.md`) — emit valid JSON-LD; validate with `python scripts/tech_audit.py --schema <url>`.
- **Internal links** — ≥3 in-body (varied anchors from `.seo/link-inventory.md`), ≥2 inbound from existing pages added the same run.
- **Images/OG** — specify what's needed (hero/OG at 1200×630). If the `og-image` / `feature-image` skills are installed, hand image generation to them; otherwise leave a clearly-marked placeholder path and flag it in the hand-off for the user to supply.

---

## Answer-engine optimization + E-E-A-T (Step 3)

Ranking gets you eligible; **AEO gets you cited** by ChatGPT/Perplexity/AI Overviews/Claude — now a primary distribution channel. Full layer in `aeo.md`. The essentials while drafting:

- **Lead with the answer**, then depth. Write the core claims as *self-contained, quotable* sentences (an LLM should be able to lift one without its neighbors).
- **Every stat carries inline attribution + a date** — LLMs preferentially cite numbers, and Perplexity always shows a source.
- **Cover the entity map** from the brief; define key terms on first use — that's what earns topical-authority recognition.
- **Match the answer-intent bucket** (definitional / process / comparison / decision) — see `aeo.md` for the structure each wants.

**E-E-A-T** (the signal 2026 rewards most): a named author with relevant credentials (from `.seo/brand.md`'s Author section), first-hand framing where it's true ("in our data," "when we tested this"), and a visible published/updated date. Demonstrated experience + original contribution beats demonstrated knowledge.

---

## Show the experience (the human layer)

The hardest signal to fake — and therefore the most valuable — is *shown* lived experience. Where it's genuinely true (drawing on the brand's Proprietary-data + First-hand sections and the product/first-hand researcher's findings), work in:

- **A real failure or mistake** + what it taught — "we tried X first; it flopped because Y."
- **The actual process, including dead ends** — "approaches A and B failed before C worked," not a clean retrospective that pretends the answer was obvious.
- **Honest uncertainty + limitations** — "early data, small sample; holds in [conditions], untested in [others]." Admitting the edges of your knowledge reads as expertise, not weakness.
- **Evolution of a view** — "my thinking on this changed since [year/event]."
- **Specific, real, *named* examples** — at least a few per piece. Real companies/numbers/timeframes, never hypotheticals.

**The specificity bar:** exact figure / timeframe / named example always beats "many," "most," "significantly." *"67% of the mid-market SaaS teams we surveyed hit this in months 4-6"* beats *"many companies struggle with this."* Vagueness is the clearest tell of thin content.

**Hard rule — these only work because they're true.** Inventing a failure, a client, or a stat to *sound* authentic is the same sin as fabricating data, and it backfires harder. If the product genuinely has no experience to draw on for a topic, that's a sign it may be the wrong piece (loop back to Step 1) — or it should lean on cited primary sources + original *analysis* instead of faked first-hand color.

---

## Output format

Match the site's **content store** (`content-stores.md`): files in the repo, a headless CMS, an app DB, WordPress, or hand-off. For file stores, `output-formats.md` covers detecting the surface, matching existing frontmatter, and **reusing the existing layout component** — don't invent one. For DB/CMS, render the body in the store's format (HTML / markdown / portable text) and create a **draft** (or hand off a ready-to-paste artifact + field map). Never auto-publish.

---

## Strip the AI tells (before you finish)

A piece that reads like AI wrote it underperforms on trust and shares. Run the **bundled polish pass** in `polish-pass.md` over the finished draft — it's the full tell list (sentence-construction tells, the model word-hoard, the em-dash decision tree), the voice pass against `.seo/brand.md`, and the skeptical pass that stops you from sanding the personality flat. This is a required sub-step, not optional; the goal is to remove the robot without removing the human.

(The standalone `polish` skill, if installed, goes wider — it sweeps user-facing strings across a whole diff and updates tests. Reach for it only if this run also touched UI/email copy beyond the article. See the note at the end of `polish-pass.md`.)

---

## Hand to blog-article? (optional augmenting skill)

**Default: write the prose inline.** Only if the `blog-article` skill is installed *and* the piece is a long pillar guide that warrants a dedicated drafting pass, you may hand it the outline + research + angle for prose, then resume here for SEO wiring, verification, and registration. If `blog-article` isn't installed, this changes nothing — inline is the standard path.
