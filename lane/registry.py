from __future__ import annotations

TRIGGER_CHAINS: dict[str, list[str]] = {
    "alert": ["incident", "ticket_patch", "release_gate"],
    "ticket": ["ticket_patch"],
    "release": ["release_gate"],
    "onboard": ["onboarding"],
    "advisory": ["advisory"],
}

DEFAULT_FIXTURES: dict[str, str] = {
    "alert": "alerts/ALT-2041.json",
    "ticket": "tickets/SUP-1187.md",
    "advisory": "advisories/HARBOR-2026-014.json",
}


def chain_for(trigger: str) -> list[str]:
    key = trigger.lower().strip()
    if key not in TRIGGER_CHAINS:
        raise ValueError(f"Unknown trigger '{trigger}'. Choose from: {', '.join(TRIGGER_CHAINS)}")
    return list(TRIGGER_CHAINS[key])
