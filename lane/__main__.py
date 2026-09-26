from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lane.orchestrator import Orchestrator
from lane.registry import DEFAULT_FIXTURES


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lane", description="Lane multi-agent orchestrator")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="Execute a workflow trigger")
    run_p.add_argument(
        "--trigger",
        required=True,
        choices=["alert", "ticket", "release", "onboard", "advisory"],
        help="Workflow trigger",
    )
    run_p.add_argument(
        "--repo",
        default=str(_project_root() / "sample-service"),
        help="Path to Harbor Stay sample repo",
    )
    run_p.add_argument("--fixture", default=None, help="Fixture path relative to repo/fixtures or absolute")
    run_p.add_argument(
        "--log-dir",
        default=str(_project_root() / "lane" / "runs"),
        help="Directory for run JSON logs",
    )

    args = parser.parse_args(argv)

    if args.command == "run":
        fixture = args.fixture or DEFAULT_FIXTURES.get(args.trigger)
        orch = Orchestrator(args.repo)
        packet, log = orch.run(args.trigger, fixture_path=fixture)
        log_path = orch.write_log(log, args.log_dir)

        print(f"Run {packet.run_id} trigger={args.trigger} status={packet.status}")
        if packet.errors:
            print("Errors:")
            for err in packet.errors:
                print(f"  - {err}")
        print(f"Log: {log_path}")
        print(packet.to_json())
        return 0 if packet.status in ("complete", "escalated") else 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
