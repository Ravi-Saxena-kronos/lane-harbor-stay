from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lane.agents import AGENT_REGISTRY
from lane.packet import HandoffPacket
from lane.policies import after_agent_failure, should_stop_chain
from lane.registry import chain_for
from lane.repo_context import SharedRepoContext


@dataclass
class RunLog:
    run_id: str
    trigger: str
    started_at: str
    steps: list[dict[str, Any]] = field(default_factory=list)
    final_packet: dict[str, Any] | None = None
    finished_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "runId": self.run_id,
            "trigger": self.trigger,
            "startedAt": self.started_at,
            "steps": self.steps,
            "finalPacket": self.final_packet,
            "finishedAt": self.finished_at,
        }


class Orchestrator:
    def __init__(self, repo_path: str | Path):
        self.repo = SharedRepoContext(repo_path)

    def run(self, trigger: str, fixture_path: str | None = None) -> tuple[HandoffPacket, RunLog]:
        apps = chain_for(trigger)
        packet = HandoffPacket.start(trigger=trigger, repo_path=str(self.repo.root))
        if fixture_path:
            packet.artifacts["fixture_path"] = fixture_path
        elif trigger == "ticket":
            packet.artifacts["ticket_path"] = "tickets/SUP-1187.md"

        log = RunLog(
            run_id=packet.run_id,
            trigger=trigger,
            started_at=datetime.now(timezone.utc).isoformat(),
        )

        prev_app: str | None = None
        for app_name in apps:
            if should_stop_chain(packet):
                break

            agent = AGENT_REGISTRY.get(app_name)
            if agent is None:
                packet = packet.set_status("failed").add_error(f"unknown agent: {app_name}")
                break

            packet = packet.with_app(prev_app, app_name)
            try:
                packet = agent.run(packet, self.repo)
            except Exception as exc:  # noqa: BLE001 — orchestrator boundary
                packet = after_agent_failure(packet, app_name, str(exc))

            log.steps.append(
                {
                    "app": app_name,
                    "status": packet.status,
                    "artifactsKeys": sorted(packet.artifacts.keys()),
                    "errors": list(packet.errors),
                }
            )
            prev_app = app_name

            if should_stop_chain(packet) and packet.status == "running":
                packet = packet.set_status("complete")

        if packet.status == "running":
            packet = packet.set_status("complete")

        log.final_packet = packet.to_dict()
        log.finished_at = datetime.now(timezone.utc).isoformat()
        return packet, log

    def write_log(self, log: RunLog, log_dir: str | Path) -> Path:
        out = Path(log_dir)
        out.mkdir(parents=True, exist_ok=True)
        path = out / f"run-{log.run_id}.json"
        path.write_text(json.dumps(log.to_dict(), indent=2), encoding="utf-8")
        return path
