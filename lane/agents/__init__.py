from lane.agents.advisory import AdvisoryAgent
from lane.agents.incident import IncidentAgent
from lane.agents.onboarding import OnboardingAgent
from lane.agents.release_gate import ReleaseGateAgent
from lane.agents.ticket_patch import TicketPatchAgent

AGENT_REGISTRY = {
    "incident": IncidentAgent(),
    "ticket_patch": TicketPatchAgent(),
    "release_gate": ReleaseGateAgent(),
    "onboarding": OnboardingAgent(),
    "advisory": AdvisoryAgent(),
}
