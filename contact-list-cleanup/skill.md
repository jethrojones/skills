---
name: contact-list-cleanup
description: Clean and normalize contact lists (CSV/XLSX) for import into HubSpot, Instantly, or Kit. Use when the user has a raw export or email dump that needs cleaning, deduping, name-splitting, or internal-contact removal before import.
---

# Contact List Cleanup

Standard pipeline for turning a raw contact export into an import-ready CSV. Apply these rules without re-asking each time.

## Standing rules (apply unless told otherwise)
1. **Remove internal people**: ask once which domain(s) are internal for this list, then drop every row at those domains. Also drop the user's own addresses and any named family/test contacts.
2. **Split names**: if there's only a full-name or email-only column, derive `First Name` and `Last Name` columns. From email locals like `jane.smith@…`, split on `.`/`_`; capitalize. If you genuinely can't tell, leave Last Name blank rather than guessing.
3. **Dedupe by email** (case-insensitive). Keep the row with the most filled fields.
4. **Output**: a new CSV next to the source, named `<source>-clean.csv`. Never overwrite the raw export.
5. **Mark processed files** by appending `_done` to the filename after a successful import/append, and skip `*_done*` files when scanning folders. No extra confirmation needed for renames.

## Destination formats
- **HubSpot**: match column headers to HubSpot property names. Import via `hubspot-cli` skill or the UI template.
- **Instantly**: columns `email, first_name, last_name, company_name` minimum. See `instantly` skill for upload.
- **Kit**: `email, first_name` minimum. See `kit` skill.

## Process
1. Read the file (use `xlsx` skill for Excel; plain parsing for CSV). Show a 5-row preview and the column mapping you plan.
2. For destructive steps (row deletion), do a **dry run first**: report what will be removed and why, then execute.
3. Write the clean CSV, report counts: rows in → rows out, removed (by reason), deduped.

---
Created by Claude Fable 5 on 2026-07-04 09:03 PT. Generalized 2026-07-04 09:15 PT.
