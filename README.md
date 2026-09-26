# Lane — multi-agent dev-ops orchestrator

**Team:** [Double Charge Club](https://lablab.ai) · **IBM Bob 2.0 Hackathon**

Lane is one **orchestrator** that runs five specialist **agent apps** over a single shared codebase. The orchestrator decides what runs, when it runs, what data is passed between steps, how errors are handled, and when a workflow is complete. Agents do not call each other directly.

Demo repository: **Harbor Stay** — a fictional inn reservation API with intentional drift (billing bug, stale runbook, OpenAPI mismatch) for workflow demos.

## Architecture

```
Trigger (alert | ticket | release | onboard | advisory)
        │
        ▼
   Orchestrator (lane/)
        │
        ├── incident      → alerts & on-call
        ├── ticket_patch  → support ticket → patch + tests
        ├── release_gate  → contract / migration / tests
        ├── onboarding    → repo map & doc drift
        └── advisory      → dependency rollout
        │
        ▼
   sample-service/  (Harbor Stay — shared repo context)
```

| Trigger   | Agent chain |
|-----------|-------------|
| `alert`   | incident → ticket_patch → release_gate |
| `ticket`  | ticket_patch |
| `release` | release_gate |
| `onboard` | onboarding |
| `advisory`| advisory |

## Quick start

Requirements: **Python 3.10+**, standard library only for Harbor Stay.

```bash
git clone https://github.com/Ravi-Saxena-kronos/lane-harbor-stay.git
cd lane-harbor-stay

# Harbor Stay (sample service)
cd sample-service
python3 -m unittest discover -s tests -v
python3 -m harborstay.demo

# Lane (from repository root)
cd ..
python3 -m lane run --trigger ticket
python3 -m lane run --trigger alert
```

Optional — install Lane into your virtualenv:

```bash
pip install -e .
python3 -m lane run --trigger alert --repo ./sample-service
```

Run logs are written to `lane/runs/run-<uuid>.json`.

## IBM Bob 2.0

Bob was used in **Agent mode** to build and extend Harbor Stay, the orchestrator, and agent apps (including the **ticket_patch** flow that applies the idempotency billing fix and regression test). Task session summaries are included in the hackathon submission.

## Project layout

| Path | Description |
|------|-------------|
| [`sample-service/`](sample-service/) | Harbor Stay API, tests, fixtures, docs |
| [`lane/`](lane/) | Orchestrator, handoff packets, agent apps |
| [`submission/`](submission/) | Cover assets and Bob screenshots |
| [`DOUBLE-CHARGE-CLUB-PLAYBOOK.md`](DOUBLE-CHARGE-CLUB-PLAYBOOK.md) | Team playbook |

## License

MIT — see [LICENSE](LICENSE).
