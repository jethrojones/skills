# {{PRODUCT_NAME}} — Content Ledger

> The memory of the content engine. Read first on every `seo-content` run: the **Shipped** table is the dedup record (never re-write a covered topic); the **Candidate backlog** is the scored shortlist so each run starts warm. Updated in the same edit batch as every piece shipped.

---

## Shipped

| Date | Title | Type | Slug / URL | Target keyword | Vol | KD | Primary internal links | Commit / PR |
|---|---|---|---|---|---|---|---|---|
{{SHIPPED_ROWS}}

<!-- Append one row per piece at Step 5. Type ∈ guide | how-to | listicle | definition | comparison | data-study | resource | opinion | case-study -->

---

## Candidate backlog

> Scored shortlist from the last selection run. Re-score when this is >30 days old or the user says "re-research." The next run reads this before regenerating the pool — it starts from here, validates the top pick is still open and winnable, and only does fresh research if needed.

| Rank | Candidate | Proposed type | Target keyword | Vol | KD | Intent | Score | Notes / angle |
|---|---|---|---|---|---|---|---|---|
{{BACKLOG_ROWS}}

<!-- Score = sum of winnability + traffic-potential + conversion-intent + strategic-value + (6 - effort), each 1-5. See references/opportunity-research.md Step C. -->

---

## Coverage map (optional)

> A running view of which clusters/themes have content and which are thin or empty. Helps spot topical-depth gaps the keyword tools miss. Fill in as the library grows.

| Cluster / theme | Pieces shipped | Gaps still open |
|---|---|---|
{{COVERAGE_ROWS}}

---

## Notes

- **DR cap:** read current DR from `.seo/keyword-research.json`. Targets must be KD ≤ DR + 10 while DR is climbing.
- **No duplication:** before adding a candidate, check it isn't already a programmatic page in `docs/seo-sprint.md` or a shipped row above.
- **One piece per run.** This ledger grows by one `Shipped` row per invocation.
