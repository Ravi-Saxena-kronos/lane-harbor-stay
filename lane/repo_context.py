from __future__ import annotations

from pathlib import Path


class SharedRepoContext:
    """Pinned view of the Harbor Stay (or other) repository for every agent in a run."""

    def __init__(self, repo_path: str | Path):
        self.root = Path(repo_path).resolve()
        if not self.root.is_dir():
            raise FileNotFoundError(f"Repo path not found: {self.root}")

    @property
    def billing_py(self) -> Path:
        return self.root / "harborstay" / "billing.py"

    @property
    def openapi(self) -> Path:
        return self.root / "openapi.yaml"

    @property
    def runbook(self) -> Path:
        return self.root / "docs" / "runbook.md"

    @property
    def architecture(self) -> Path:
        return self.root / "docs" / "architecture.md"

    @property
    def deps_manifest(self) -> Path:
        return self.root / "deps" / "manifest.json"

    def fixture(self, *parts: str) -> Path:
        return self.root / "fixtures" / Path(*parts)

    def read_text(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def test_command(self) -> list[str]:
        return ["python3", "-m", "unittest", "discover", "-s", "tests"]
