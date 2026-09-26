from __future__ import annotations

import subprocess

from lane.agents.base import AgentApp
from lane.packet import HandoffPacket
from lane.repo_context import SharedRepoContext


class ReleaseGateAgent(AgentApp):
    name = "release_gate"

    def run(self, packet: HandoffPacket, repo: SharedRepoContext) -> HandoffPacket:
        gates: dict[str, str] = {}

        if repo.openapi.is_file():
            spec = repo.read_text(repo.openapi)
            if '"200"' in spec and "/confirm" in spec:
                gates["contract_status_code"] = "fail_openapi_expects_200_confirm"
            else:
                gates["contract_status_code"] = "pass"
            if "chargedCents" not in spec:
                gates["contract_charged_field"] = "fail_missing_chargedCents_in_spec"
            else:
                gates["contract_charged_field"] = "pass"
        else:
            gates["contract"] = "skip_no_openapi"

        migration = repo.root / "migrations" / "004_guest_email.sql"
        if migration.is_file() and "guest_email" in migration.read_text(encoding="utf-8"):
            gates["migration_guest_email"] = "fail_api_has_no_guest_email"
        else:
            gates["migration_guest_email"] = "pass"

        result = subprocess.run(
            repo.test_command(),
            cwd=repo.root,
            capture_output=True,
            text=True,
        )
        gates["unit_tests"] = "pass" if result.returncode == 0 else "fail"

        failed = [k for k, v in gates.items() if v.startswith("fail")]
        decision = "go" if not failed else "no-go"

        updates = {
            "release_gates": gates,
            "release_decision": decision,
            "failed_gates": failed,
        }
        packet = packet.merge_artifacts(updates)
        if decision == "no-go":
            return packet.set_status("complete").add_error("release_gate: no-go — gates failed (expected before patch)")
        return packet.set_status("complete")
