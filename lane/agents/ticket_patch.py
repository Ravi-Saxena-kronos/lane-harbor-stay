from __future__ import annotations

import re
import subprocess
from pathlib import Path

from lane.agents.base import AgentApp
from lane.packet import HandoffPacket
from lane.repo_context import SharedRepoContext


class TicketPatchAgent(AgentApp):
    name = "ticket_patch"

    def _resolve_ticket(self, repo: SharedRepoContext, packet: HandoffPacket) -> Path | None:
        if packet.artifacts.get("ticket_path"):
            p = Path(packet.artifacts["ticket_path"])
            return p if p.is_file() else repo.fixture(packet.artifacts["ticket_path"])
        if packet.artifacts.get("fixture_path") and str(packet.artifacts["fixture_path"]).endswith(".md"):
            return self._resolve_fixture(repo, str(packet.artifacts["fixture_path"]))
        default = repo.fixture("tickets/SUP-1187.md")
        return default if default.is_file() else None

    def _resolve_fixture(self, repo: SharedRepoContext, path: str) -> Path:
        candidate = Path(path)
        if candidate.is_file():
            return candidate
        return repo.fixture(path)

    def run(self, packet: HandoffPacket, repo: SharedRepoContext) -> HandoffPacket:
        ticket_path = self._resolve_ticket(repo, packet)
        if ticket_path is None or not ticket_path.is_file():
            return packet.set_status("needs_input").add_error("ticket_patch: support ticket not found")

        text = ticket_path.read_text(encoding="utf-8")
        has_repro = bool(re.search(r"Idempotency-Key", text)) and bool(re.search(r"18400", text))
        if not has_repro:
            return packet.set_status("needs_input").add_error("ticket_patch: missing repro fields in ticket")

        billing = repo.billing_py
        bug_line = None
        if billing.is_file():
            for i, line in enumerate(billing.read_text(encoding="utf-8").splitlines(), start=1):
                if "charge_card" in line and "idempotency" not in line.lower():
                    bug_line = i
                    break

        # Skeleton: report fix intent; Bob/human applies patch + test later.
        updates = {
            "ticket_path": str(ticket_path.relative_to(repo.root)),
            "patch_target": "harborstay/billing.py",
            "fix_summary": "Move idempotency check before charge_card; add retry idempotency test",
            "bug_hint_line": bug_line,
            "tests_command": repo.test_command(),
        }

        # Optional: run tests if requested (default dry-run for skeleton)
        if packet.artifacts.get("run_tests"):
            result = subprocess.run(
                repo.test_command(),
                cwd=repo.root,
                capture_output=True,
                text=True,
            )
            updates["test_exit_code"] = result.returncode
            updates["test_stdout"] = result.stdout[-2000:]
            if result.returncode != 0:
                return packet.merge_artifacts(updates).set_status("escalated").add_error("ticket_patch: tests failed")

        return packet.merge_artifacts(updates).set_status("running")
