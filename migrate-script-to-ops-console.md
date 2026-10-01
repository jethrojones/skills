# Skill: Migrate Script to Ops Console

Migrate an existing Python/shell script from the old cron-based runner to the [YOUR_COMPANY] Ops Console at `https://YOUR_OPS_CONSOLE_URL`.

## What the Ops Console is

A Cloudflare Workers app (`ops-console` repo, `YOUR_GITHUB_ORG/ops-console`) that replaces the old folder of Python scripts with a persistent, web-accessible control plane. It has:

- **D1** — relational state (scripts, schedules, runs, secrets, audit_log tables)
- **R2** — verbose run logs stored as JSON
- **KV** — short-lived cache
- **Queue** — `ops-dispatch` (triggers runs)
- **Durable Objects** — WorkflowLock (prevents concurrent runs), UsageCounter, WebhookDedup
- **Cloudflare Access** — email domain SSO protecting the dashboard

Scripts live in `ops-console/scripts/{script-id}/` and are one of three runtimes:
- `worker` — pure TypeScript, runs directly inside the Worker. **Default choice.**
- `external` — thin TypeScript shim that POSTs to GitHub Actions; actual work happens externally
- `workflow` — TypeScript with Cloudflare Workflows (long-running, durable)

**Always prefer `worker` (TypeScript) runtime.** The `external` runtime introduces two major problems: (1) secrets must be stored in TWO places — ops console D1 and GitHub Actions repo secrets — which is fragile and confusing; (2) Jeff (and others) won't have GitHub access to troubleshoot failures. Only use `external` if the job genuinely cannot be done in TypeScript (e.g., it relies on a large Python library with no JS equivalent).

## Directory layout for each script

```
scripts/{script-id}/
  script.ts          # Required — run() entry point
  script.test.ts     # Optional — unit tests
  metadata.json      # Script registration metadata
  SKILL.md           # Human-readable description for Claude debug context
  fixtures/          # Optional — test fixtures
```

## Step 1 — Choose a script ID

Lowercase, hyphenated, unique. Examples: `crm-sync`, `docuseal-webhook`, `kit-hubspot-sync`.

## Step 2 — Determine the runtime

| Situation | Runtime |
|-----------|---------|
| Script calls APIs, processes data, can be written in TypeScript | `worker` ← **start here** |
| Python script that uses libraries with no JS equivalent (e.g., pandas, numpy, scipy) | `external` |
| Job runs longer than ~30 seconds or needs crash-recovery | `workflow` |

**Do not default to `external` just because the original was Python.** Most HubSpot/ArcGIS/Airtable/Vimeo scripts are just HTTP calls — they rewrite trivially in TypeScript. The complexity of managing dual secrets and debugging GitHub Actions failures far outweighs the cost of rewriting.

## Step 3 — Create `metadata.json`

```json
{
  "id": "script-id",
  "name": "Human-Readable Name",
  "description": "One sentence describing what it does.",
  "runtime": "external",
  "github_workflow_id": "script-id.yml",
  "default_schedule": "0 14 * * 1-5",
  "business_hours_only": true,
  "required_secrets": ["hubspot", "other_service"],
  "triggers": [
    { "type": "cron", "enabled": true },
    { "type": "manual", "enabled": true }
  ]
}
```

Fields:
- `runtime` — `external`, `worker`, or `workflow`
- `github_workflow_id` — only for `external`; the `.yml` filename in `.github/workflows/`
- `default_schedule` — cron expression (America/New_York timezone). Leave out if webhook-only.
- `business_hours_only` — if true, cron only fires Mon–Fri 10am–11pm ET
- `required_secrets` — service names whose secrets are stored in D1 and decrypted at runtime
- `triggers` — which trigger types are enabled

## Step 4 — Create `script.ts`

### CRITICAL: Register every `worker` script in the static registry

Wrangler **cannot** bundle dynamic template-literal imports like `` import(`../scripts/${id}/script.js`) ``. This produces a `[empty-glob]` warning at build time and a "Module not found in bundle" error at runtime.

Every `worker` runtime script **must** be added to `src/script-registry.ts` with a static import:

```typescript
// src/script-registry.ts
import type { WorkflowContext } from './queue-consumer.js';
import { run as myScriptRun } from '../scripts/my-script/script.js';
// add more imports here for each new worker script

export const scriptRegistry: Record<string, (ctx: WorkflowContext, params?: unknown) => Promise<void>> = {
  'my-script': myScriptRun as (ctx: WorkflowContext, params?: unknown) => Promise<void>,
  // add entry here too
};
```

After editing `script-registry.ts`, always run `npm run typecheck` before deploying.

### For `external` runtime (dispatches to GitHub Actions)

```typescript
import type { WorkflowContext } from '../../src/queue-consumer.js';

export interface MyScriptParams {
  dry_run?: boolean;
  // add other inputs that map to GitHub Actions workflow_dispatch inputs
}

export async function run(ctx: WorkflowContext, params?: MyScriptParams): Promise<void> {
  ctx.log('info', 'Dispatching script-id to GitHub Actions', { params });

  const resp = await fetch(
    `https://api.github.com/repos/${ctx.env.GITHUB_REPO_OWNER}/${ctx.env.GITHUB_REPO_NAME}/actions/workflows/script-id.yml/dispatches`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${ctx.secrets.github_pat}`,
        Accept: 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'User-Agent': 'ops-console',
      },
      body: JSON.stringify({
        ref: 'main',
        inputs: {
          dry_run: String(params?.dry_run ?? false),
        },
      }),
    },
  );

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`GitHub dispatch failed: ${resp.status} ${text}`);
  }

  ctx.log('success', 'Dispatched to GitHub Actions', { status: resp.status });
}
```

Notes:
- `ctx.secrets` is a `Record<string, string>` — keys match `required_secrets` in `metadata.json`
- Always include `github_pat` in `required_secrets` for `external` scripts
- `ctx.log(type, message, detail?)` — types: `'info'`, `'api_call'`, `'api_response'`, `'error'`, `'success'`
- Throw to mark the run as failed; don't catch and swallow errors

### For `worker` runtime (runs TypeScript directly)

**Before writing any loop that calls an API per item, read the "Cloudflare Workers subrequest limits" section.** If you have N items and K calls per item, count the total. Use HubSpot batch APIs (batch upsert, batch associations) when processing more than ~10 records.

```typescript
import type { WorkflowContext } from '../../src/queue-consumer.js';

export async function run(ctx: WorkflowContext, params?: unknown): Promise<void> {
  const token = ctx.secrets.hubspot;

  ctx.log('info', 'Starting job');

  const resp = await fetch('https://api.hubapi.com/crm/v3/...', {
    headers: { Authorization: `Bearer ${token}` },
  });
  ctx.log('api_response', 'HubSpot response', { status: resp.status });

  if (!resp.ok) throw new Error(`HubSpot error: ${resp.status}`);

  const data = await resp.json();
  ctx.log('success', 'Job complete', { count: (data as { results: unknown[] }).results?.length });
}
```

## Cloudflare Workers subrequest limits

Every outgoing `fetch()` call a Worker makes counts as a **subrequest**. The limits are:

| Plan | Limit per invocation |
|------|---------------------|
| Free | **50 subrequests** |
| Workers Paid | **1000 subrequests** |

A queue consumer counts each batch of messages as one invocation. So if processing one HubSpot task makes 3 API calls per school, and that district has 22 schools, you're at 66+ calls before the task is even marked complete — easily crashing the free plan and eating the paid plan budget.

**The limit is NOT configurable in `wrangler.toml`.** The error message from Cloudflare says "to configure this limit refer to wrangler.toml" but that section only controls CPU and memory. The subrequest limit is set by your Cloudflare plan. The only way to "configure" it is to upgrade from free to paid.

### How to budget subrequests before writing a script

Count: `(calls per item) × (number of items) + overhead`

Example for 22 records:
- 7 overhead calls (fetch tasks, get parent record, fetch children, upsert parent)
- 22 items × 3 calls each (search + upsert + associate) = 66
- 1 mark task complete
- **Total: 74** — safe on paid (1000), fatal on free (50)

If your math exceeds 40 (leave headroom), use batch APIs.

### Managing subrequests with HubSpot batch APIs

HubSpot supports batch operations for CRM objects. Always use these when processing more than ~10 records:

**Batch upsert companies** (search + create + update — does NOT require the property to be unique in HubSpot):
```typescript
// 3 calls for up to 100 records instead of 2 calls per record
// Step 1: find which already exist (1 search call)
const searchData = await hs('POST', '/crm/v3/objects/companies/search', token, {
  filterGroups: [{ filters: [{ propertyName: 'external_id', operator: 'IN', values: records.map(r => r.external_id) }] }],
  properties: ['external_id'],
  limit: 100,
});
const existingMap = new Map(searchData.results.map(r => [r.properties.external_id, r.id]));

const toCreate = records.filter(r => !existingMap.has(r.external_id));
const toUpdate = records.filter(r => existingMap.has(r.external_id));

// Step 2: batch create new ones (1 call)
const created = await hs('POST', '/crm/v3/objects/companies/batch/create', token, {
  inputs: toCreate.map(s => ({ properties: buildHsProperties(s) })),
});

// Step 3: batch update existing ones (1 call)
const updated = await hs('POST', '/crm/v3/objects/companies/batch/update', token, {
  inputs: toUpdate.map(r => ({ id: existingMap.get(r.external_id), properties: buildHsProperties(r) })),
});
const allIds = [...created.results, ...updated.results].map(r => r.id);
```

**Do NOT use `batch/upsert`** — it requires the `idProperty` to be configured as a unique property in HubSpot. If it's not unique, HubSpot returns a 400 error. The search + create + update pattern above works with any property.

**Batch associations** (link schools to a district):
```typescript
// 1 API call for up to 100 associations instead of 1 per school
await hs('POST', '/crm/v4/associations/companies/companies/batch/create', token, {
  inputs: schoolHsIds.map(id => ({
    from: { id },
    to: { id: districtHsId },
    types: [{ associationCategory: 'HUBSPOT_DEFINED', associationTypeId: 13 }],
  })),
});
```

**Chunking** — HubSpot batch endpoints cap at 100 inputs per call. Always chunk:
```typescript
const CHUNK = 100;
for (let i = 0; i < items.length; i += CHUNK) {
  await hs('POST', '/crm/v3/objects/companies/batch/upsert', token, {
    inputs: items.slice(i, i + CHUNK).map(...),
  });
}
```

With batching, the same 22-record batch uses ~9 subrequests instead of 74.

### Pattern: extract property builder for reuse in batch

When using both single-record and batch upserts, extract the properties logic once:
```typescript
function buildHsProperties(fields: Record<string, unknown>): Record<string, string> {
  const properties: Record<string, string> = {};
  for (const [k, v] of Object.entries(fields)) {
    if (v == null) continue;
    const hsKey = HS_FIELD_MAP[k] ?? k;
    properties[hsKey] = String(v);
  }
  return properties;
}
// use in single upsert: { properties: buildHsProperties(fields) }
// use in batch: inputs.map(item => ({ ..., properties: buildHsProperties(item) }))
```

## Step 5 — Create `SKILL.md`

A plain Markdown file describing the script for Claude's debug context. Include:
- What it does (step by step)
- Runtime
- Required secrets and their scopes
- Known failure modes

## Step 6 — Create the GitHub Actions workflow (for `external` scripts only)

Add `.github/workflows/script-id.yml` to `YOUR_GITHUB_ORG/ops-console`. All scripts live in this one repo — never reference `YOUR_GITHUB_ORG/YOUR_REPO` or any other repo.

```yaml
name: script-id

on:
  workflow_dispatch:
    inputs:
      ops_run_id:
        description: 'Ops console run ID (for callback)'
        required: false
        default: ''
      dry_run:
        description: 'Dry run (no writes)'
        required: false
        default: 'false'

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4   # checks out ops-console itself

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r scripts/script-id/requirements.txt

      - name: Run
        env:
          HUBSPOT_ACCESS_TOKEN: ${{ secrets.HUBSPOT_ACCESS_TOKEN }}
          DRY_RUN: ${{ inputs.dry_run }}
        run: python scripts/script-id/script.py 2>&1 | tee /tmp/script_output.txt

      - name: Report back to ops console
        if: always()
        env:
          OPS_RUN_ID: ${{ inputs.ops_run_id }}
          JOB_STATUS: ${{ job.status }}
          GITHUB_RUN_URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
        run: |
          if [ -z "$OPS_RUN_ID" ]; then exit 0; fi
          OUTPUT=$(cat /tmp/script_output.txt 2>/dev/null | tail -100 || echo "")
          STATUS="success"
          if [ "$JOB_STATUS" != "success" ]; then STATUS="failed"; fi
          jq -n \
            --arg run_id "$OPS_RUN_ID" \
            --arg status "$STATUS" \
            --arg github_run_url "$GITHUB_RUN_URL" \
            --arg log_output "$OUTPUT" \
            '{"run_id":$run_id,"status":$status,"github_run_url":$github_run_url,"log_output":$log_output}' \
          | curl -s -X POST "https://YOUR_OPS_CONSOLE_URL/api/webhook/github-callback" \
              -H "Content-Type: application/json" \
              -d @-
```

**Important:** Python scripts must live in `scripts/script-id/` inside the ops console repo. Secrets must be added as GitHub Actions repo secrets **separately** from the ops console D1 secrets — this is the dual-secret burden that makes `external` undesirable.

## Step 7 — Register the script in D1

```bash
npx wrangler d1 execute ops-console --remote --command \
  "INSERT INTO scripts (id, name, description, runtime, enabled, metadata, created_at, updated_at)
   VALUES (
     'script-id',
     'Human Name',
     'One sentence description.',
     'external',
     1,
     '{\"required_secrets\":[\"hubspot\",\"github_pat\"],\"github_workflow_id\":\"script-id.yml\",\"business_hours_only\":true}',
     datetime('now'),
     datetime('now')
   );"
```

## Step 8 — Add a schedule (if cron-triggered)

```bash
npx wrangler d1 execute ops-console --remote --command \
  "INSERT INTO schedules (script_id, cron_expression, timezone, business_hours_only, updated_at)
   VALUES ('script-id', '0 14 * * 1-5', 'America/New_York', 1, datetime('now'));"
```

## Step 9 — Add required secrets via the UI

Go to `https://YOUR_OPS_CONSOLE_URL` → Settings → Connections. Add each service secret. The key must exactly match the string in `required_secrets`.

For `github_pat`, the value is the GitHub Personal Access Token with `actions: write` scope (already set as `GITHUB_PAT` in wrangler secrets, but scripts access it via `ctx.secrets.github_pat` from D1, not from env directly — so it still needs to be stored as a D1 secret under the key `github_pat`).

## Step 10 — Deploy

```bash
cd ~/ops-console
npm run deploy
```

## Checklist

- [ ] `scripts/{id}/metadata.json` created with correct `runtime` field
- [ ] `scripts/{id}/script.ts` created with `run()` export
- [ ] `scripts/{id}/SKILL.md` created
- [ ] **`worker` only**: Script added to `src/script-registry.ts` (static import + registry entry)
- [ ] **`external` only**: GitHub Actions `.yml` created with ops console callback step
- [ ] Script registered in D1 (`INSERT INTO scripts`) with matching `runtime` value
- [ ] Schedule registered in D1 (`INSERT INTO schedules`) — if cron-triggered
- [ ] Secrets added via ops console UI
- [ ] **`external` only**: Same secrets added as GitHub Actions repo secrets
- [ ] `npm run typecheck` passes clean
- [ ] Deployed with `npm run deploy`
- [ ] Test run triggered manually from ops console dashboard and actual work verified (not just "dispatched")

## Known secrets and their D1 keys

| D1 key | What it is |
|---|---|
| `hubspot` | HubSpot Private App token |
| `github_pat` | GitHub PAT with Actions write scope |
| `kit` | Kit (email) API key (v4, `X-Kit-Api-Key` header) |
| `instantly` | Instantly v2 Bearer token |
| `docuseal` | DocuSeal API token |
| `resend` | Resend API key |
| `drive` | Google Drive service account JSON |

## Common mistakes

### Bundling (most critical for `worker` runtime)
- **Not registering the script in `src/script-registry.ts`** — causes "Module not found in bundle" at runtime. Wrangler cannot bundle dynamic imports. Every `worker` script needs a static import entry in the registry. This error looks like: `Module not found in bundle: ../scripts/my-script/script.js`.
- **Not running `npm run typecheck` after editing the registry** — catches unused imports (`TS6133`) and other errors before deploy.

### Runtime choice
- **Defaulting to `external` for Python scripts** — prefer TypeScript rewrite. The `external` runtime requires secrets in two places (D1 + GitHub repo secrets) and means non-engineers can't troubleshoot without GitHub access.
- **Forgetting to update D1 `runtime` column** after rewriting a script from `external` to `worker` — the dashboard will still try to use the wrong dispatch path.

### External runtime specifics
- **Forgetting `github_pat` in `required_secrets`** — dispatch will fail with 401
- **Wrong repository in workflow `checkout`** — always use `YOUR_GITHUB_ORG/ops-console`, never `YOUR_GITHUB_ORG/YOUR_REPO` or other repos. Scripts live in `scripts/{id}/` in the ops console repo.
- **Dual secrets not set** — for `external`, secrets must be in BOTH ops console D1 (for the shim) AND GitHub Actions repo secrets (for the Python script). Forgetting either side causes silent failures.
- **No ops console callback** — without the "Report back to ops console" step in the workflow, run status stays `running` forever and logs never appear in the dashboard.

### Subrequest limit
- **Making one fetch() per record instead of using batch APIs** — the most common way to hit the subrequest limit. Any loop that calls an API per item (per school, per contact, per task) is a red flag. See the "Cloudflare Workers subrequest limits" section above.
- **Not counting subrequests before writing** — do the math: `(calls per item) × (max expected items)`. If it could exceed 40 on the critical path, use batch APIs.
- **Assuming the limit is configurable** — the Cloudflare error message says "refer to wrangler.toml" but the subrequest limit is not configurable there. Only upgrading to the paid plan raises it from 50 → 1000.
- **Using `batch/upsert` without a unique property** — HubSpot's batch upsert requires the `idProperty` to be configured as unique in the portal. If it's not, you get a 400 error. Use the search + `batch/create` + `batch/update` pattern instead (works with any property).

### Success definition
- **Treating "dispatch accepted" as success** — a run should only be marked `success` when actual work is confirmed: records updated, tasks completed, emails sent, etc. If the script exits without doing real work (e.g., 0 tasks processed when tasks existed), it should throw and mark the run `failed`.

### General
- **`metadata.json` changes don't auto-sync to D1** — `metadata.json` is a reference file only. The live metadata comes from the D1 `scripts.metadata` column. After changing `metadata.json` (e.g. adding `params_schema`, `triggers`, `required_secrets`), always run `UPDATE scripts SET metadata = '...' WHERE id = 'script-id'` to sync it.
- Cron not firing: check `business_hours_only` and that `next_run_at` is set in the schedules table
- Script not found: the D1 `scripts.id` must exactly match the directory name under `scripts/`
- Secret not found at runtime: key in `required_secrets` must exactly match the service name stored in D1
