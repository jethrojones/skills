# Answer Engine Optimization (AEO / GEO)

As of 2026, a large share of search demand never reaches a blue link — it's answered inside ChatGPT, Perplexity, Google AI Overviews, Claude, and Bing Copilot. Ranking gets you eligible; **AEO gets you cited.** This is a distribution channel, not a nice-to-have, and it's mostly won on three variables you control: **structure, freshness, and credible sourcing.**

Apply this layer while writing (Step 3) and enforce it at the gate (Step 4). It composes with the on-page SEO in `writing.md` and the per-type schema in `content-types.md` — it doesn't replace them.

---

## 1. Match the answer-intent bucket

Every query an answer engine serves falls into one of four buckets. The piece's *structure* should match its bucket (this overlaps the type chosen in `content-types.md`, but AEO cares about the answer shape specifically):

| Intent | Lead the page with | Schema |
|---|---|---|
| **Definitional** ("what is X") | A concise 40-60 word plain-language answer in the first paragraph, then expand. | `Article` / `DefinedTerm` + `FAQPage` |
| **Process** ("how to X") | An ordered, liftable workflow near the top; examples, checklist, troubleshooting below. | `HowTo` |
| **Comparison** ("X vs Y", "best X") | A balanced table + explicit, scenario-based recommendation ("pick X if…"). | `ItemList` / `FAQPage` |
| **Decision** ("should I X", "is X worth it") | A direct verdict up front, then the reasoning and the conditions under which it flips. | `Article` + `FAQPage` |

---

## 2. Write for extraction

An answer engine lifts *self-contained* passages. Optimize for being quotable out of context:

- **Lead with the answer.** Inverted pyramid: the direct answer first, depth after. Don't bury it under throat-clearing.
- **One idea per paragraph**, and make the topic sentence stand alone — a model should be able to quote it without the surrounding paragraph.
- **Stats carry inline attribution + a date.** "X grew 40% in 2025 (Source, 2025)." LLMs preferentially cite numbers, and Perplexity *always* shows a source — give it a clean one to grab.
- **Headings phrased as the real question** people/engines ask, answered immediately in the first sentence beneath.
- **FAQ section built from the actual PAA set** (from the entity map in the brief), each answer self-contained in 40-80 words.
- **Define key terms explicitly** the first time they appear — entity clarity is what gets you recognized as a topical authority.

**The quotability test:** for the piece's 3-5 core claims, ask "would an LLM lift this exact sentence as its answer?" If a sentence needs its neighbors to make sense, tighten it until it doesn't.

---

## 3. Entity & topical completeness

Answer engines reward semantic coverage, not keyword density. Using the **entity/topical map** from the research brief:

- Cover every must-have concept, entity, and PAA question on the map. A gap there reads as "incomplete" to both Google and the LLMs.
- Link related concepts internally (the entity graph) — this is also where the ≥3 in-body internal links land naturally.
- Name the specifics: real tools, real numbers, real proper nouns. Vague content doesn't get cited because it can't be attributed to anything.

---

## 4. Freshness & credibility signals

- **Stamp the date.** Visible "published / last updated" + accurate `datePublished`/`dateModified` in schema. Stale-looking pages get skipped.
- **Cite credible, primary sources** (the verified ledger handles this). Tier-up: link the original study, not the blog that quoted it.
- **Be transparent about original data.** When you present your own numbers, disclose the method, sample size, and limitations ("n=400 implementations, self-reported, 2025"). Caveated, sourced data earns more citations than confident vagueness — Perplexity and human readers both trust the page that shows its work.
- **Show experience & authorship.** A named author with relevant credentials, and first-hand signals ("in our data," "when we tested this") — this is the E-E-A-T + information-gain signal that 2026 rewards most.

---

## 5. Platform notes (where they differ)

- **ChatGPT** — lifts bullet lists and FAQ blocks close to verbatim. Give it clean, scannable structure.
- **Perplexity** — always cites; prioritizes authoritative sources and *original data*. Original stats are your best Perplexity play.
- **Google AI Overviews** — favor FAQ/HowTo schema, short definitions, and supporting visuals.
- **Claude** — rewards longer, coherent passages with clear reasoning and supporting evidence; don't over-fragment for it.
- **Bing Copilot** — synthesizes from high-quality results; favors step-by-step guides and comparisons.

Write the substance once, well-structured; these are formatting nudges, not five different drafts. Community validation also matters — content that gets discussed on places like Reddit (~40% of AI citations) compounds; worth noting in the hand-off as an off-platform amplifier, not something this skill fabricates.
