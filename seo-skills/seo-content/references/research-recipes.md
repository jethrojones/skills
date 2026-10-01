# Research Recipes — finding the next piece

The exact data calls behind Step 1 selection. Two modes: **Ahrefs MCP available** (precise) and **Ahrefs-free fallback** (good-enough). Both produce the same thing: a scored shortlist of candidate pieces. Use whichever the environment supports — don't refuse if Ahrefs is missing.

DataForSEO MCP (`mcp__dfs-mcp__*`) is an equivalent substitute for most Ahrefs calls below; if you have it instead, the parallel tool is named in each recipe.

---

## Ahrefs mode

`project_id` lives in `.seo/config.json` as `ahrefs_project_id` — needed for `gsc-*`, `rank-tracker-*`, `site-audit-*` (not for `site-explorer-*`, which take a `target` domain). The Ahrefs API drifts; before first use of a tool in a session, call `mcp__ahrefs__doc` with the tool name for current params.

**Read DR first.** Pull or read your domain rating from `.seo/keyword-research.json` (`baseline.domain_rating`). DR caps everything: target **KD ≤ DR + 10** while DR is still climbing. If you don't have it cached:

```
mcp__ahrefs__site-explorer-domain-rating   target: <your-domain>
```

### Recipe 1 — Content gap (the main candidate source)
Keywords competitors rank for that you don't.

```
mcp__ahrefs__site-explorer-organic-keywords
  target: <competitor-domain>        # repeat per competitor from .seo/brand.md
  limit: 100
  order_by: traffic:desc
  where: kd <= <DR+10> AND volume >= 30
  country: us
```
Subtract your own ranked set (your domain's organic-keywords) to leave true gaps.
*DFS equivalent:* `mcp__dfs-mcp__dataforseo_labs_google_domain_intersection` (competitors vs you).

### Recipe 2 — Question & matching-terms sweep
Maps cleanly to how-to / definition / listicle types.

```
mcp__ahrefs__keywords-explorer-matching-terms
  keywords: ["<cluster seed 1>", "<cluster seed 2>", ...]
  limit: 200
  where: kd <= <DR+10> AND volume >= 30
  order_by: traffic_potential:desc
  country: us
```
Filter for question modifiers (how, what, why, best, vs, for). **Traffic potential (TP) beats raw volume** — a KD-22/TP-2,500 keyword is a better target than a KD-8/TP-200 one.
*DFS equivalent:* `mcp__dfs-mcp__dataforseo_labs_google_keyword_suggestions`.

### Recipe 3 — Related terms (cluster expansion)
Find adjacent clusters off your best-ranking existing page.

```
mcp__ahrefs__keywords-explorer-related-terms
  keywords: ["<your best-ranking term>"]
  limit: 100
  country: us
```

### Recipe 4 — Striking distance (existing sites)
Queries you already rank 5-20 for with no dedicated page — a focused new piece often captures these fast.

```
mcp__ahrefs__gsc-keywords
  project_id: <project_id>
  date_from: <90-days-ago>   date_to: <today>
  where: position >= 5 AND position <= 20 AND impressions >= 50
  order_by: impressions:desc
  limit: 100
```
Cross-check `gsc-pages` to see which page owns the query. If a *dedicated* page already exists, it's a boost, not a new piece — skip it here.

### Recipe 5 — AI-citation gaps
Questions in your space LLMs answer without citing you. Filling these is high-leverage AI surface area.

```
mcp__ahrefs__brand-radar-ai-responses   (and brand-radar-cited-pages)
```
*DFS equivalent:* `mcp__dfs-mcp__ai_opt_llm_ment_search` / `ai_optimization_llm_response`.

### Recipe 6 — SERP overview (run on the chosen keyword, drives TYPE)
Before committing, look at who ranks and what format Google rewards.

```
mcp__ahrefs__serp-overview   keyword: "<target>"   country: us
```
Read the top 10:
- 5+ results DR > 60 and substantive → likely can't displace; downgrade winnability.
- 3+ results DR < 30, or top 3 are Reddit/Quora → strong signal you can rank.
- The **format** of the top 10 dictates the type (listicles → write a listicle, etc.) — see `content-types.md` Step D.
*DFS equivalent:* `mcp__dfs-mcp__serp_organic_live_advanced`.

### Rendering & cost notes
- Many Ahrefs results carry `render_with` metadata — **call the named render tool** (`render-data-table`, `render-time-series-chart`, `render-scorecard`); show the rendered data, don't summarize raw JSON.
- Monetary fields (`value`, `traffic_value`, `cpc`) are in **USD cents** — divide by 100.
- Cache results to `.seo/keyword-research.json`; treat as stale only after ~30-90 days or on an explicit "re-research." `site-explorer-organic-keywords` is the priciest call — batch all competitors in one pass.
- If calls start failing, check `mcp__ahrefs__subscription-info-limits-and-usage`.

---

## Ahrefs-free fallback

No `mcp__ahrefs__*` (and no `mcp__dfs-mcp__*`)? The skill still works — precision drops, not capability. Be honest up front: *"No keyword tool is connected, so volume/KD will be estimates. We can still pick and ship a strong piece; refine the numbers later with a tool."*

### 1. User pastes data
If the user has Ahrefs/Semrush/Mangools/Ubersuggest/GSC, ask them to paste: domain DR/DA, competitor organic-keyword export (CSV), GSC positions 5-20, and volumes for any specific terms you're weighing. Parse into the `.seo/keyword-research.json` shape; mark missing columns.

### 2. Web-search + SERP scrape
1. Identify competitors (ask, or read their pricing/about pages).
2. For each, web-search `"<competitor> alternatives"` / `"<topic> guide"` and read Google autocomplete, the **People-Also-Ask** box, and "related searches" (scrape `google.com/search?q=...` with `firecrawl-scrape`, or use the `firecrawl-search` skill / built-in `WebSearch`).
3. Scrape the **top 3-5 ranking pages** for the target topic — capture their H1/H2 structure and depth. This is your table-stakes + gap read (the core of the SERP teardown in `writing.md`).
4. Estimate volume crudely from Google Trends relative interest; record as a **range** and mark `"source": "estimated"`.

### 3. Structured interview (last resort)
Use `AskUserQuestion`: top competitors? problems customers describe at signup? tools they tried before yours? ideal-customer title/industry? Turn answers into hypothesis topics, mark them unvalidated, and suggest validating volumes with a free tool (Google Keyword Planner, Mangools free tier) before deep work.

### What's degraded
| Capability | Ahrefs/DFS mode | Fallback mode |
|---|---|---|
| Volume | precise monthly | range estimate |
| KD | 0-100 score | heuristic ("competitive" if top-3 are DR > 60) |
| Traffic potential | per-keyword TP | volume × CTR estimate |
| Striking distance | GSC pos 5-20 via MCP | user pastes GSC data |
| SERP overview | top 10 with per-result DR | `firecrawl-scrape` the SERP page |

When a tool becomes available later, do a refresh pass to upgrade `estimated` rows to real numbers.
