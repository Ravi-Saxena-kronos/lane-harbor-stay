from __future__ import annotations

import json
import uuid
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class HandoffPacket:
    run_id: str
    trigger: str
    from_app: str | None
    to_app: str | None
    repo_path: str
    repo_revision: str
    status: str  # running | complete | needs_input | escalated | failed
    artifacts: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    retries: dict[str, int] = field(default_factory=dict)

    @staticmethod
    def start(trigger: str, repo_path: str, repo_revision: str = "working-tree") -> HandoffPacket:
        return HandoffPacket(
            run_id=str(uuid.uuid4()),
            trigger=trigger,
            from_app=None,
            to_app=None,
            repo_path=repo_path,
            repo_revision=repo_revision,
            status="running",
            artifacts={},
        )

    def with_app(self, from_app: str | None, to_app: str | None) -> HandoffPacket:
        n = deepcopy(self)
        n.from_app = from_app
        n.to_app = to_app
        return n

    def merge_artifacts(self, updates: dict[str, Any]) -> HandoffPacket:
        n = deepcopy(self)
        n.artifacts.update(updates)
        return n

    def set_status(self, status: str) -> HandoffPacket:
        n = deepcopy(self)
        n.status = status
        return n

    def add_error(self, message: str) -> HandoffPacket:
        n = deepcopy(self)
        n.errors.append(message)
        return n

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
