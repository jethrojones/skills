# Research → Verified Brief (Step 2)

The quality of a piece is decided here, before a word of prose is written. As of the **March 2026 core update**, the dominant ranking signal is *information gain* — how much genuinely new knowledge a page adds versus what already ranks. Pure synthesis of the top 10 is invisible. This step exists to manufacture information gain and to ground every claim in a verified source.

Two principles drive the design:

1. **Generate ≠ verify.** The agent that gathers a fact must not be the only one that confirms it. Research and verification are separate passes (separate subagents where the host supports it).
2. **The writer consumes facts, not raw notes.** Step 2's output is a structured **research brief** — a claim ledger, an entity map, the information-gain statement, the angle. Step 3 writes *from* the brief.

---

## 2a. Fan out the research

Run these six angles. **If the host supports subagents (e.g. the Agent/Task tool, or `deep-research` if installed), spawn them in parallel** — each returns a structured packet and your main context stays clean. If not, run them sequentially in-context. Either way, all six get covered.

| Researcher | Goal | Tools |
|---|---|---|
| **SERP teardown** | Scrape the top 5-10 ranking pages. Capture the *union* of their sections (your table-stakes coverage) and what they **all miss** (the gap your angle lives in). Note their depth + heading shape so you out-cover them. | `firecrawl-scrape` / `firecrawl-search` / WebFetch; `serp-overview` |
| **Primary sources & studies** | Find authoritative *primary* sources — original studies, datasets, official docs, standards, filings. Not aggregator blogs. | WebSearch, firecrawl, Ahrefs/DFS |
| **Statistics & data points** | Pull real, citable numbers — each with attribution, a URL, and a date. These are what LLMs lift and what earns links. | WebSearch, firecrawl |
| **Contrarian / counter-evidence** | Actively hunt evidence *against* the obvious thesis. Surfaces the strongest counter-argument (which a great piece addresses head-on) and stops you shipping a one-sided take. | WebSearch, firecrawl |
| **Product / first-hand data** | The E-E-A-T moat: the product's own anonymized metrics, real outcomes, features, anti-positioning, and any first-hand testing you can run or cite. Read `.seo/brand.md` (Proprietary data + Author sections) and the repo. | repo, brand.md, product metrics |
| **Entity / topical map** | The concepts, entities, and questions that *must* appear for topical authority + semantic completeness. Pull the real People-Also-Ask set and related entities. | `keywords-explorer-related-terms`, PAA scrape, `serp-overview` |

Each researcher returns findings as structured items, not prose:

```
- claim/fact: "<the specific thing>"
  source: <URL or "product data: <which metric>">
  tier: primary | secondary | tertiary        # primary = original source/data; tertiary = blog citing a blog
  date: <when the data is from>                # freshness matters for AEO
  confidence: high | medium | low
```

---

## 2b. Synthesize the research brief

Merge the six packets into one brief. This is the artifact Step 3 writes from. Save it to `.seo/briefs/<slug>.md` for auditability and reuse (optional but recommended).

The brief has five parts:

1. **Claim ledger** — every factual claim the piece will make, each with its source(s), tier, date, and verification status (filled in 2c). This is the spine; if a claim isn't in the ledger, it doesn't go in the piece.
2. **Entity / topical-coverage map** — the must-cover concepts, entities, and PAA questions. The piece is "complete" only when it covers this set.
3. **Table-stakes vs. gap** — what every top-10 page covers (you must match) and what they all miss (your opening).
4. **Information-gain statement** — the explicit, specific thing this piece contains that is in **none** of the top 10. Must be ≥1 of: *original/proprietary data · first-hand testing or experience · expert commentary · a genuinely novel framework or synthesis.* **If you cannot write this sentence concretely, stop and loop back to Step 1** — the piece will not rank and is not worth writing. ("Restates the consensus more clearly" is not information gain.)
5. **The angle** — the one differentiated thesis, now backed by the gap + the information-gain element.

---

## 2c. Verify — the separate pass

Do this as a **distinct pass** (a separate subagent if the host allows; otherwise a clean-slate review that treats the ledger adversarially — pretend a fact-checker is trying to get the piece retracted).

For every claim in the ledger:

- **Cross-check against an independent second source.** A claim sourced once is "single-source," not "verified." Mark each: `verified` (≥2 independent sources or one primary), `single-source`, or `unverified`.
- **Tier-up where possible.** If a stat traces back to a primary source, cite the primary, not the blog that quoted it.
- **Refute the high-stakes claims.** For any number, named comparison, or load-bearing assertion, actively try to prove it wrong. Claims that survive a real refutation attempt are the ones worth featuring.

Then resolve every non-`verified` claim — no exceptions carried silently into the draft:

- **`unverified`** → re-research it, or **cut it**. Never ship an unverifiable factual claim as fact.
- **`single-source` but plausible** → keep with explicit inline attribution ("according to <source>"), or down-rank to a bracketed range flagged for the user.
- **Fabrication is the cardinal sin.** A wrong number gets the page penalized and destroys trust faster than anything else. Real sources or clearly-bracketed estimates — never an invented statistic.

The verified ledger (claims + final status + sources) is what Step 3 writes from and what gets persisted at Step 5 as the citation record.

---

## Degradation & escalation

- **No subagents in the host** → run the six angles sequentially. Slower, same coverage. Don't skip angles.
- **`deep-research` skill installed** → hand 2a + 2c to it for heavier multi-source fan-out and verification, then resume here to build the brief.
- **User opted into a workflow** → the six researchers + the verify pass map cleanly onto a `pipeline()` (researchers → synthesize → verify). Only do this if the user explicitly asked for a workflow.
- **No keyword/AEO tools** → the SERP teardown via `firecrawl` + WebSearch still carries this step; see the Ahrefs-free fallback in `research-recipes.md`.

The output of Step 2 is always the same: a verified brief. How you produce it flexes to the environment; the bar does not.
