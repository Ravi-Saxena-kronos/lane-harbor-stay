# IBM Bob task sessions (judging deliverable)

IBM asks teams to export **Bob task session** reports from **real work** on the repo—not toy demos.  
This folder holds screenshots and exported history for those sessions.

## What to upload here

For each session:

1. Screenshot of the **task session summary** (consumption summary).
2. Exported **task history** markdown from Bob (History → export), if available.

**Do not** commit API keys, credentials, or `.env` files.

## Recommended sessions (matches IBM Bob onboarding)

Run these in **Agent mode** with workspace root = this repository.

| # | IBM pattern | File / scope | Bob prompt (copy-paste) |
|---|-------------|--------------|-------------------------|
| 1 | **Review existing code** | `sample-service/harborstay/billing.py` | See [docs/EVALUATE-IBM-BOB.md](../docs/EVALUATE-IBM-BOB.md#1-review-existing-code) |
| 2 | **Generate tests** | `sample-service/harborstay/inventory.py` | See [docs/EVALUATE-IBM-BOB.md](../docs/EVALUATE-IBM-BOB.md#2-generate-tests) |
| 3 | **Understand unfamiliar code** | `lane/` + `sample-service/` | See [docs/EVALUATE-IBM-BOB.md](../docs/EVALUATE-IBM-BOB.md#3-understand-unfamiliar-code) |

## Naming files

```text
bob_sessions/
  01-review-billing-screenshot.png
  01-review-billing-history.md
  02-tests-inventory-screenshot.png
  03-onboarding-codebase-screenshot.png
```

## Already done (hackathon build)

You may also keep earlier sessions (e.g. `release_gate.py`, runbook) under `submission/bob-screenshots/`—copy or link them here for one place judges expect.
