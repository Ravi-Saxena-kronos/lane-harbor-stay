# Lane — orchestrator skeleton

Routes five specialist **agent apps** over one shared repo (`sample-service/`). Agents do not call each other; only the orchestrator chains them.

## Run

From project root (`PROJECT-02`):

```bash
python3 -m lane run --trigger alert
python3 -m lane run --trigger ticket
python3 -m lane run --trigger release
python3 -m lane run --trigger onboard
python3 -m lane run --trigger advisory
```

Options:

- `--repo` — path to Harbor Stay (default: `./sample-service`)
- `--fixture` — override input file for the trigger
- `--log-dir` — write `run-<id>.json` (default: `./lane/runs`)

## Triggers

| Trigger | Chain |
|---------|--------|
| `alert` | incident → ticket_patch → release_gate |
| `ticket` | ticket_patch |
| `release` | release_gate |
| `onboard` | onboarding |
| `advisory` | advisory |

## Layout

- `orchestrator.py` — run loop, error policy, completion
- `packet.py` — handoff JSON between steps
- `registry.py` — trigger → agent list
- `repo_context.py` — pinned repo path and doc index
- `agents/` — one module per agent app
