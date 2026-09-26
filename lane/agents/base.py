from __future__ import annotations

from abc import ABC, abstractmethod

from lane.packet import HandoffPacket
from lane.repo_context import SharedRepoContext


class AgentApp(ABC):
    name: str

    @abstractmethod
    def run(self, packet: HandoffPacket, repo: SharedRepoContext) -> HandoffPacket:
        raise NotImplementedError

    def done(self, packet: HandoffPacket) -> bool:
        return packet.status == "complete"
