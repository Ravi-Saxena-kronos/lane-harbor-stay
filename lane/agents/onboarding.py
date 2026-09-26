from __future__ import annotations

from lane.agents.base import AgentApp
from lane.packet import HandoffPacket
from lane.repo_context import SharedRepoContext


class OnboardingAgent(AgentApp):
    name = "onboarding"

    def run(self, packet: HandoffPacket, repo: SharedRepoContext) -> HandoffPacket:
        arch_ok = repo.architecture.is_file() and "billing.py" in repo.read_text(repo.architecture)
        runbook_text = repo.read_text(repo.runbook) if repo.runbook.is_file() else ""
        stale = "billing-worker" in runbook_text or "confirm.js" in runbook_text
        billing_exists = repo.billing_py.is_file()

        if stale and billing_exists and "services/billing-worker" in runbook_text:
            return (
                packet.merge_artifacts(
                    {
                        "module_map": ["harborstay/api.py", "harborstay/billing.py", "harborstay/inventory.py"],
                        "doc_drift": True,
                        "drift_detail": "runbook points at billing-worker; code is in harborstay/billing.py",
                    }
                )
                .set_status("escalated")
                .add_error("onboarding: doc drift — update runbook before starter task")
            )

        updates = {
            "module_map": ["harborstay/api.py", "harborstay/billing.py", "harborstay/inventory.py"],
            "architecture_trusted": arch_ok,
            "starter_task": "Read confirm_reservation in harborstay/billing.py and trace Idempotency-Key handling",
            "doc_drift": stale,
        }
        return packet.merge_artifacts(updates).set_status("complete")
