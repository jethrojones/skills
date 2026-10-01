# Opportunity Research — deciding what to write next

This is the skill's core job. By the end of this step you have **one chosen topic, one chosen type, and the data to justify both** — ready for the Step 1 checkpoint.

Don't skip to writing. A mediocre topic written brilliantly loses to a great topic written adequately. Selection is where the leverage is.

---

## Step A — Build the exclusion set (what NOT to write)

Before generating ideas, know what's off the table:

1. **Shipped pieces** — read the `## Shipped` table in `.seo/content-ledger.md`.
2. **Programmatic pages** — `git ls-files | grep -iE 'alternatives|compare|/for/|playbooks'` (and read `docs/seo-sprint.md` tracker *if it exists*). Editorial content must not duplicate a templated page targeting the same keyword. (No sprint tracker? The git scan alone is enough.)
3. **Existing content** — for file-based sites, `git ls-files | grep -iE 'blog|guides|content|articles|docs'`. For **DB/CMS sites, there are no files to scan** — list existing content from the sitemap (`/sitemap.xml`) or the CMS API instead (see `content-stores.md` Operation 1). Read titles/slugs either way.

Anything matching the exclusion set is dead. If the strongest opportunity is already covered but *thin*, that's a striking-distance **boost**, not a new piece — this skill ships new pieces. Note the boost in the hand-off (and hand it to `seo-sprint` if that skill is installed), unless the user wants a fresh companion piece instead.

---

## Step B — Regenerate the opportunity pool

Pull from four signal sources. All the exact tool calls — Ahrefs/DFS mode and the Ahrefs-free fallback — are in `research-recipes.md`. Use whichever mode the environment supports.

Read **DR** from `.seo/keyword-research.json` first — it caps everything (KD ≤ DR + 10 while DR is climbing).

### B1. Keyword / topic gaps (the main source)
- **Content gap** — keywords your competitors rank for and you don't:
  `mcp__dfs-mcp__dataforseo_labs_google_domain_intersection` (competitors vs you) or `mcp__ahrefs__site-explorer-organic-keywords` per competitor minus your own ranked set. Filter KD ≤ DR+10, volume ≥ 30.
- **Question sweep** — `keywords-explorer-matching-terms` / `mcp__dfs-mcp__dataforseo_labs_google_keyword_suggestions` seeded with your clusters, filtered to question modifiers (how, what, why, best, vs, for). Questions map cleanly to how-to / definition / listicle types.
- **Related terms** — `keywords-explorer-related-terms` around your best-ranking existing page to find adjacent clusters you can extend into.

### B2. Striking distance (existing sites)
- `gsc-keywords` positions 5-20, impressions ≥ 50, where **no dedicated page exists**. A focused new piece can capture a query your homepage is accidentally ranking for. (If a dedicated page exists, it's a boost, not a new piece — see Step A.)

### B3. AI-citation gaps
- Where do LLMs answer questions in your space without citing you? `mcp__ahrefs__brand-radar-ai-responses` / `brand-radar-cited-pages`, or `mcp__dfs-mcp__ai_opt_llm_ment_search` / `ai_optimization_llm_response`. A piece that becomes the canonical answer to an uncited question is disproportionately valuable — LLMs cite structured, sourced, definitive content.

### B4. Freshness / timely
- Seasonal demand (`kw_data_google_trends_explore`), a just-launched feature worth a piece, or a recent shift in the space (a competitor pricing change, a platform API change). Timely pieces age slower and earn shares.

Merge into one candidate list. Dedup against Step A.

---

## Step C — Score the candidates

Score each on five axes. Keep it lightweight — a 1-5 per axis, summed, is enough to rank. Don't build a spreadsheet; build a ranked shortlist.

| Axis | What it measures | High score when |
|---|---|---|
| **Winnability** | Can this rank at our DR? | KD ≤ DR; top-10 SERP has weak/thin pages or forums |
| **Traffic potential** | Size of the cluster, not just the head term | TP ≥ 500; one keyword gates many long-tail variants |
| **Conversion intent** | How close to buying | Commercial/transactional > informational; "best X tool" > "what is X" |
| **Strategic value** | Authority / links / AI-citation draw | Original data, contrarian POV, or fills an AI-citation gap |
| **Effort** | Inverse — cheaper is better at equal value | Reusable structure, data already in hand (penalize 3-day data studies unless value is high) |

**Tie-breakers, in order:** conversion intent → winnability → traffic potential. A KD-12 commercial keyword beats a KD-8 informational one almost every time.

Write the **full scored shortlist** to the `## Candidate backlog` section of `.seo/content-ledger.md`. Next run reads this first and only re-scores if it's >30 days old or the user says "re-research." This is what makes each run start warm instead of cold.

---

## Step D — Choose the TYPE

The type is **not** a free choice. It's dictated by intent × SERP shape × goal. Run a SERP overview on the chosen keyword (`serp-overview`, or scrape the top 10 with firecrawl) and read what's actually ranking.

Quick selection logic (full catalog + structure in `content-types.md`):

| Signal in the SERP / query | Type to write |
|---|---|
| Query is "how to X"; top results are step-by-step | **How-to / tutorial** |
| Query is "best X" / "X tools" / "N ways"; top results are listicles | **Listicle / roundup** |
| Query is "what is X" / "X meaning"; snippet box present, short pages rank | **Definition / answer page** |
| Broad commercial-investigation head term; top results are long pillar pages | **Pillar guide** |
| "X vs Y" or multi-tool decision; top results compare options | **Comparison** |
| Nobody in the top 10 has original numbers; topic is data-shaped | **Data study / original research** |
| "X template" / "X examples" / "X checklist"; people want a usable asset | **Resource / template library** |
| Theme-led, low keyword volume, high authority/AI-citation value | **Opinion / POV** |
| "How [company] does X" / teardown intent | **Case study / teardown** |

**The override rule:** when the SERP format and the query phrasing disagree, follow the SERP. Google has already decided what it rewards for that query. Writing a tutorial into a listicle SERP is a losing bet no matter how good the tutorial is.

If two types both fit (e.g. a guide *with* an embedded data study), pick the primary type for structure/schema and fold the secondary in as a section.

---

## Output of this step

Hand the Step 1 checkpoint:
- **Top 3 candidates**, each with: title, target keyword, vol, KD, your DR, intent, SERP-format read, proposed type + one-line why.
- Your recommended pick (#1) clearly marked.

Then let the user confirm or redirect. Their positioning instinct is a legitimate tie-breaker the data can't see.
