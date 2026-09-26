from __future__ import annotations

from lane.packet import HandoffPacket


def should_stop_chain(packet: HandoffPacket) -> bool:
    return packet.status in ("needs_input", "escalated", "failed", "complete")


def after_agent_failure(packet: HandoffPacket, app_name: str, message: str) -> HandoffPacket:
    """Retry each app once, then escalate."""
    count = packet.retries.get(app_name, 0)
    packet = packet.add_error(f"{app_name}: {message}")
    if count < 1:
        retries = dict(packet.retries)
        retries[app_name] = count + 1
        n = packet.set_status("running")
        n.retries = retries
        return n
    return packet.set_status("escalated")
