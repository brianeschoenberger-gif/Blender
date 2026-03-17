"""Validate the blender-object-builder skill with stdlib-only checks.

Run this after changing the skill so self-updates do not leave it in a broken state.
"""

from __future__ import annotations

import compileall
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "SKILL.md",
    ROOT / "agents" / "openai.yaml",
    ROOT / "references" / "pitfalls.md",
    ROOT / "references" / "patterns.md",
    ROOT / "references" / "maintenance.md",
    ROOT / "references" / "sources.md",
    ROOT / "scripts" / "create_mesh_object.py",
    ROOT / "scripts" / "create_object_in_collection.py",
    ROOT / "scripts" / "run_blender_headless.example.txt",
]


def validate_frontmatter(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter.")
        return errors

    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append("SKILL.md frontmatter is not closed correctly.")
        return errors

    frontmatter = parts[1]
    if "name: blender-object-builder" not in frontmatter:
        errors.append("SKILL.md frontmatter must declare the correct skill name.")
    if "description:" not in frontmatter:
        errors.append("SKILL.md frontmatter must include a description.")
    return errors


def validate_openai_yaml(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    required_snippets = [
        'display_name: "Blender Object Builder"',
        'short_description: "Script-first Blender object creation"',
        'default_prompt:',
    ]
    for snippet in required_snippets:
        if snippet not in text:
            errors.append(f"agents/openai.yaml is missing: {snippet}")
    return errors


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {path}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    errors.extend(validate_frontmatter(ROOT / "SKILL.md"))
    errors.extend(validate_openai_yaml(ROOT / "agents" / "openai.yaml"))

    if not compileall.compile_dir(ROOT / "scripts", quiet=1, force=True):
        errors.append("Python script compilation failed.")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
