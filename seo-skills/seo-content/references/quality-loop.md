# Quality Loop (Step 4)

A one-shot draft is a first draft. As of 2026, content that ranks and gets cited goes through **critique → revise → re-check**, with the critique done by a perspective separate from the one that wrote the prose. This step replaces "write it, run the word-count script, ship" with a short adversarial loop: a critic panel scores the draft, you revise the weakest dimensions, and hard gates decide whether it ships.

Keep it bounded: **at most two revise rounds.** The goal is a piece that clears every gate, not infinite polishing.

---

## 4a. The critic panel

Run these five critics against the draft + the research brief. Where the host supports subagents, run them in parallel and as *separate* agents from the writer (a critic invested in the prose will rate it too kindly). Each returns a 1-5 score + the specific, actionable misses.

| Critic | Asks | Fails when |
|---|---|---|
| **Skeptic / fact-check** | Is every factual claim in the verified ledger? Any assertion without a source? Cross-check the draft's numbers against the ledger; try to refute the load-bearing claims. | An unsourced or unverified claim is stated as fact; a number doesn't match the ledger. |
| **Information-gain** | What's here that's in *none* of the top 10? Is the original element (data / first-hand / expert / framework) real and substantive, or is the piece dressed-up synthesis? | The information-gain statement isn't actually delivered in the body. |
| **AEO / extractability** | Lead-with-the-answer? Self-contained quotable claims? Stats attributed + dated? Entity map fully covered? Schema + freshness present? (`aeo.md`) | The answer is buried; claims need context to parse; entity gaps; no schema/date. |
| **Voice** | Matches `.seo/brand.md` — voice tags, perspective, forbidden words? Reads like the site's existing content? | Forbidden word present; register is off; sounds like generic SaaS. |
| **Completeness / structure** | All table-stakes sections covered? Logical flow? Any thin (<~150-word) section that promises more than it delivers? | A SERP table-stakes section is missing; a heading over-promises. |

Score the draft on each axis. **Any axis ≤3 is a revise target.**

---

## 4b. Revise

Fix the weakest dimensions first — the panel hands you specific misses, not vibes. Bias toward **adding substance** (a missing source, the under-delivered original-data point, an uncovered entity) over reshuffling words. For the voice axis, the bundled polish pass (`polish-pass.md`) is the tool; run it here.

After revising, re-run only the critics that failed. Stop when all five are ≥4 **or** you've done two rounds — then go to the gates. If after two rounds a *gate* still fails, that's signal the piece was mis-selected; say so in the hand-off rather than shipping under-spec.

---

## 4c. The hard gates (pass/fail — must all pass to ship)

The critic panel improves the piece; the gates decide if it ships. These are non-negotiable:

1. **Information gain** — the brief's information-gain element is concretely present in the body (original data / first-hand / expert / novel framework). *This is the gate that matters most in 2026.* Dressed-up synthesis fails.
2. **Citation coverage** — every factual claim traces to the verified ledger; no `unverified` claim shipped as fact; high-stakes numbers carry inline attribution. No fabricated statistics.
3. **AEO-readiness** — extractable answer up top, self-contained quotable core claims, entity map covered, required schema emitted, date stamped (`aeo.md`).
4. **Deterministic checks** (the bundled scripts):
   - `python scripts/word_count.py <path> --min <type-floor>` — meets the type's word floor (`content-types.md`).
   - `python scripts/link_audit.py --orphan-check --root .` — not an orphan; then hand-confirm ≥3 in-body + ≥2 inbound links. *(File stores only — `link_audit.py` is filesystem-based. For DB/CMS, confirm the link minimums against the sitemap/API by hand, per `content-stores.md`.)*
   - `python scripts/tech_audit.py --schema <url>` if rendered — schema validates.
5. **Voice** — brand match confirmed, forbidden-words grep clean.

A failing gate is information, not blame — it usually points at a thin section, a missing source, or a forgotten schema block. Fix the root cause; don't lower the bar.

---

## Degradation

- **No subagents** → run the five critics as sequential clean-slate passes (review the draft fresh against each lens, hardest on yourself). The separation is conceptual: read as a critic trying to reject the piece, not as its author.
- **`deep-research` installed** → useful for the skeptic/fact-check critic's independent cross-checks.
- The gates run identically regardless of host — they're the floor.
