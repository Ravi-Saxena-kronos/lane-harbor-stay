from __future__ import annotations

import json
from pathlib import Path

from lane.agents.base import AgentApp
from lane.packet import HandoffPacket
from lane.repo_context import SharedRepoContext


class IncidentAgent(AgentApp):
    name = "incident"

    def _resolve_fixture(self, repo: SharedRepoContext, path: str) -> Path:
        candidate = Path(path)
        if candidate.is_file():
            return candidate
        return repo.fixture(path)

    def run(self, packet: HandoffPacket, repo: SharedRepoContext) -> HandoffPacket:
        rel = packet.artifacts.get("fixture_path")
        if not rel:
            return packet.set_status("needs_input").add_error("incident: missing fixture_path in artifacts")

        alert_path = self._resolve_fixture(repo, str(rel))
        if not alert_path.is_file():
            return packet.set_status("needs_input").add_error(f"incident: alert file not found: {rel}")

        alert = json.loads(alert_path.read_text(encoding="utf-8"))
        runbook_text = repo.read_text(repo.runbook) if repo.runbook.is_file() else ""

        updates = {
            "alert": alert,
            "suspected_files": ["harborstay/billing.py"],
            "recommended_action": "patch_idempotency_before_charge",
            "customer_status_note": alert.get("customerImpact", "Investigating booking issues."),
            "runbook_stale_hint": "billing-worker" in runbook_text,
        }
        return packet.merge_artifacts(updates).set_status("running")
