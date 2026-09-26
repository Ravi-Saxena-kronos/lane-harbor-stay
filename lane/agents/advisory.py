from __future__ import annotations

import json

from lane.agents.base import AgentApp
from lane.packet import HandoffPacket
from lane.repo_context import SharedRepoContext


class AdvisoryAgent(AgentApp):
    name = "advisory"

    def run(self, packet: HandoffPacket, repo: SharedRepoContext) -> HandoffPacket:
        rel = packet.artifacts.get("fixture_path", "advisories/HARBOR-2026-014.json")
        path = repo.fixture(rel) if not str(rel).startswith("/") else repo.root / rel
        if not path.is_file():
            return packet.set_status("needs_input").add_error(f"advisory: fixture not found: {rel}")

        advisory = json.loads(path.read_text(encoding="utf-8"))
        manifest = json.loads(repo.read_text(repo.deps_manifest)) if repo.deps_manifest.is_file() else {}
        packages = {p["name"]: p["version"] for p in manifest.get("packages", [])}

        pkg = advisory.get("package", "")
        current = packages.get(pkg)
        fixed = advisory.get("fixedVersion", "")
        affected = current is not None and current != fixed

        updates = {
            "advisory": advisory,
            "package": pkg,
            "current_version": current,
            "recommended_version": fixed,
            "service_status": {repo.root.name: "needs_bump" if affected else "ok"},
            "action": f"bump {pkg} to {fixed} in deps/manifest.json" if affected else "none",
        }
        status = "complete" if not affected else "running"
        return packet.merge_artifacts(updates).set_status(status)
