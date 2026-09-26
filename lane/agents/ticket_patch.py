from __future__ import annotations

import re
import subprocess
from pathlib import Path

from lane.agents.base import AgentApp
from lane.patches.billing_idempotency import (
    apply_billing_fix,
    apply_regression_test,
    billing_has_bug,
    run_tests,
)
from lane.packet import HandoffPacket
from lane.repo_context import SharedRepoContext


class TicketPatchAgent(AgentApp):
    name = "ticket_patch"

    def _resolve_ticket(self, repo: SharedRepoContext, packet: HandoffPacket) -> Path | None:
        if packet.artifacts.get("ticket_path"):
            rel = packet.artifacts["ticket_path"]
            p = Path(rel)
            if p.is_file():
                return p
            candidate = repo.root / rel
            if candidate.is_file():
                return candidate
            return repo.fixture(rel)
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
        test_file = repo.root / "tests" / "test_reservations.py"
        had_bug = billing_has_bug(billing)

        updates: dict = {
            "ticket_path": str(ticket_path.relative_to(repo.root)),
            "patch_target": "harborstay/billing.py",
            "fix_summary": "Idempotency check before charge_card; regression test for retry",
            "bug_present_before_patch": had_bug,
        }

        try:
            billing_changed = apply_billing_fix(billing)
            test_added = apply_regression_test(test_file)
        except RuntimeError as exc:
            return packet.merge_artifacts(updates).set_status("escalated").add_error(f"ticket_patch: {exc}")

        updates["billing_patched"] = billing_changed
        updates["regression_test_added"] = test_added

        result = run_tests(repo.root, repo.test_command())
        updates["test_exit_code"] = result.returncode
        updates["tests_command"] = repo.test_command()
        if result.stdout:
            updates["test_stdout_tail"] = result.stdout[-1500:]
        if result.stderr:
            updates["test_stderr_tail"] = result.stderr[-500:]

        packet = packet.merge_artifacts(updates)

        if result.returncode != 0:
            retries = packet.retries.get(self.name, 0)
            if retries < 1:
                packet.retries = {**packet.retries, self.name: retries + 1}
                return packet.set_status("running").add_error("ticket_patch: tests failed after patch (retry allowed)")
            return packet.set_status("escalated").add_error("ticket_patch: tests failed after patch")

        demo = subprocess.run(
            ["python3", "-m", "harborstay.demo"],
            cwd=repo.root,
            capture_output=True,
            text=True,
        )
        updates["demo_exit_code"] = demo.returncode
        updates["demo_output"] = demo.stdout.strip()
        packet = packet.merge_artifacts(updates)

        if demo.returncode != 0:
            return packet.set_status("escalated").add_error("ticket_patch: harborstay.demo failed")

        retry_lines = [line for line in demo.stdout.splitlines() if line.startswith("retry confirmation:")]
        if retry_lines and "charges=2" in retry_lines[0]:
            return packet.set_status("escalated").add_error(
                "ticket_patch: demo still shows double charge on retry"
            )

        return packet.set_status("running")
