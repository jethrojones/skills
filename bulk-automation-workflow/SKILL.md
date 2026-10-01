---
name: bulk-automation-workflow
description: Standard workflow for building and executing bulk automation tasks. Includes planning, script creation, agent definition, progressive testing, batch execution, and verification. Use this pattern for any large-scale data processing, API integrations, or batch operations.
tags: [automation, bulk-processing, workflow, scripts, agents]
---

# Bulk Automation Workflow

## Purpose

This skill defines the standard approach for building and executing bulk automation tasks for the user. Follow this workflow whenever a task involves processing multiple items (videos, files, records, API calls, etc.) at scale.

## Core Principles

1. **Plan before building** — Create a detailed implementation plan before writing code
2. **Script for repeatability** — Build standalone Python scripts that can be re-run
3. **Test progressively** — Dry-run → single item → small batch → full batch
4. **Track progress** — Implement resumability so interrupted runs can continue
5. **Verify completion** — Always confirm the job is done with a final check

---

## Phase 1: Planning

Before writing any code, create a detailed plan that includes:

### Plan Structure

```markdown
# Plan: [Task Name]

## Overview
[1-2 sentence description of what will be accomplished]

## Files to Create
- `scripts/[script_name].py` — [description]
- `.claude/agents/[agent_name].md` — [description]

## Core Functions
| Function | Purpose |
|----------|---------|
| `function_name()` | What it does |

## CLI Interface
[Document command-line arguments]

## Directory Structure
[Show where files will be created at runtime]

## Dependencies
[List required packages]

## Testing Plan
1. Test 1: [description]
2. Test 2: [description]
...

## Implementation Order
1. [First step]
2. [Second step]
...
```

### Get Plan Approval

Present the plan to the user before implementing. Wait for explicit approval or requested changes.

---

## Phase 2: Script Creation

### Script Structure

All bulk automation scripts should follow this pattern:

```python
#!/usr/bin/env python3
"""
[Script description]

Usage:
    python3 scripts/[name].py [--test] [--dry-run] [--item ITEM_ID] [--delay SECONDS]
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# --- Configuration ---
# Constants, credentials, paths

# --- Progress Tracking ---
def load_progress():
    """Load progress from JSON file."""
    pass

def save_progress(progress):
    """Save progress to JSON file."""
    pass

# --- Core Functions ---
# List items, process items, etc.

# --- Main ---
def main():
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('--test', action='store_true', help='Process only first 2 items')
    parser.add_argument('--dry-run', action='store_true', help='List items without processing')
    parser.add_argument('--item', type=str, help='Process single item by ID')
    parser.add_argument('--delay', type=float, default=2.0, help='Seconds between items')
    args = parser.parse_args()

    # Setup directories
    # Load progress
    # List all items
    # Filter eligible items
    # Process based on mode (dry-run, test, single, full)
    # Print summary

if __name__ == '__main__':
    main()
```

### Required CLI Arguments

Every bulk script must support:

| Argument | Purpose |
|----------|---------|
| `--dry-run` | List what would be processed, make no changes |
| `--test` | Process only first 2 items for verification |
| `--item ID` | Process a single specific item |
| `--delay N` | Seconds to wait between items (default: 2) |

### Required Features

1. **Progress tracking**: JSON file that tracks status of each item
2. **Resumability**: Skip already-completed items on restart
3. **Error handling**: Log errors, continue to next item
4. **Rate limit handling**: Detect and wait for API rate limits
5. **Summary output**: Print statistics at the end
6. **Log file**: Save detailed log with timestamp

### Progress File Format

```json
{
  "item_id_1": {
    "status": "completed",
    "name": "Item Name",
    "timestamp": "2026-01-27T12:00:00"
  },
  "item_id_2": {
    "status": "skipped",
    "reason": "already_exists",
    "name": "Item Name"
  },
  "item_id_3": {
    "status": "error",
    "reason": "api_failed",
    "name": "Item Name"
  }
}
```

---

## Phase 3: Agent Creation

Create an agent definition in `.claude/agents/` that can run the script autonomously.

### Agent Template

```markdown
---
name: [agent-name]
description: [What the agent does]
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
---

You are a [role description]. Your job is to run the [task] pipeline autonomously.

## Your Task

When invoked, execute this pipeline automatically:

1. **Verify Prerequisites** - Check dependencies are installed
2. **Test Mode** - Run on 2 items first to verify
3. **Verify Test Results** - Check progress file and confirm success
4. **Full Batch** - Run the complete pipeline
5. **Final Verification** - Run dry-run to confirm nothing remains
6. **Report Results** - Summarize what was processed

## CRITICAL: Execute Autonomously

Do NOT ask for confirmation between steps. Run the entire pipeline and report results only at the end.

## Step 1: Verify Prerequisites

```bash
# Check required packages
python3 -c "import package; print('OK')"
```

## Step 2: Test Mode

```bash
python3 scripts/[name].py --test
```

## Step 3: Verify Test Results

```bash
cat [progress-dir]/progress.json
```

## Step 4: Full Batch

```bash
python3 scripts/[name].py --delay 2
```

## Step 5: Final Verification

```bash
python3 scripts/[name].py --dry-run
```

## Step 6: Report Results

[Instructions for summarizing]

## Error Handling

[Document how errors are handled]

## Execution Rules

1. **No pausing** - Execute the full pipeline without stopping
2. **No confirmation prompts** - Proceed automatically
3. **Handle errors gracefully** - Log errors but continue
4. **Report at end** - Provide summary only after completion
```

---

## Phase 4: Progressive Testing

### Test Sequence

Execute tests in this exact order:

#### Test 1: Dry Run
```bash
python3 scripts/[name].py --dry-run
```
**Verify**: Lists all eligible items, no changes made, no API calls that modify data.

#### Test 2: Single Item
```bash
python3 scripts/[name].py --item [KNOWN_GOOD_ID]
```
**Verify**:
- Item processed successfully
- Output files created correctly
- Progress file updated
- External system reflects changes (if applicable)

#### Test 3: Test Mode (2 Items)
```bash
python3 scripts/[name].py --test
```
**Verify**:
- Exactly 2 items processed
- Both succeeded
- Progress file shows both items

#### Test 4: Resumability
- Run test mode to completion
- Re-run the same command
- **Verify**: Previously completed items are skipped

#### Test 5: Skip Detection
- Run on an item that should be skipped (already processed, doesn't need work)
- **Verify**: Script correctly identifies and skips it

---

## Phase 5: Batch Execution

### Running the Full Batch

```bash
PYTHONUNBUFFERED=1 python3 scripts/[name].py 2>&1
```

For long-running batches, run in background:
```bash
PYTHONUNBUFFERED=1 python3 scripts/[name].py 2>&1 &
```

### Monitoring Progress

Check progress periodically:
```bash
tail -40 [output-file]
```

Or check progress file:
```bash
cat [progress-dir]/progress.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
stats = {}
for item, info in data.items():
    s = info.get('status', 'unknown')
    stats[s] = stats.get(s, 0) + 1
for k, v in sorted(stats.items()):
    print(f'{k}: {v}')
print(f'Total: {len(data)}')
"
```

### Handling Interruptions

If the script is interrupted:
1. Check progress.json for current state
2. Re-run the same command — it will resume automatically
3. Completed items will be skipped

---

## Phase 6: Verification

### Final Verification Steps

1. **Dry-run check**: Run `--dry-run` to confirm 0 eligible items remain
2. **Progress review**: Check progress.json for any errors
3. **Spot check**: Manually verify 3-5 random items in the target system
4. **Summary report**: Document total processed, skipped, errors

### Reporting Template

```markdown
## Batch Complete

| Metric | Count |
|--------|-------|
| Total processed | X |
| Successfully completed | X |
| Skipped (reason) | X |
| Errors | X |
| Elapsed time | X hours |

### Error Details (if any)
- Item ID: reason

### Verification
- Dry-run confirms 0 remaining
- Spot-checked items: [list IDs checked]
```

---

## Example Applications

This workflow applies to:

- **Video processing**: Subtitle translation, thumbnail generation, metadata updates
- **File operations**: Batch conversion, migration, cleanup
- **API integrations**: Syncing data between systems, bulk uploads
- **Content generation**: Creating materials for multiple items
- **Data transformation**: Converting formats, enriching records

---

## Checklist

Before starting any bulk automation task, confirm:

- [ ] Plan created and approved
- [ ] Script has all required CLI arguments
- [ ] Progress tracking implemented
- [ ] Error handling with continue-on-error
- [ ] Rate limit handling for APIs
- [ ] Agent definition created
- [ ] Dry-run test passed
- [ ] Single item test passed
- [ ] Test mode (2 items) passed
- [ ] Resumability verified
- [ ] Full batch executed
- [ ] Final dry-run shows 0 remaining
- [ ] Results documented
