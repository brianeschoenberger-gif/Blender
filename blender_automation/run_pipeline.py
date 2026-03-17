from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
STAGES_DIR = ROOT / "stages"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a reusable headless Blender build/render/validate pipeline."
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to the project pipeline config JSON.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Directory for scene.blend, previews, report.json, and pipeline.log",
    )
    parser.add_argument(
        "--open-preview",
        action="store_true",
        help="Open preview.png after a successful pipeline run.",
    )
    return parser.parse_args()


def resolve_blender_exe() -> Path:
    blender_exe = os.environ.get("BLENDER_EXE", "").strip()
    if not blender_exe:
        raise SystemExit(
            "BLENDER_EXE is required. Set it to the full path of blender.exe before running the pipeline."
        )

    blender_path = Path(blender_exe).expanduser()
    if not blender_path.exists() or not blender_path.is_file():
        raise SystemExit(f"BLENDER_EXE does not point to a valid file: {blender_path}")
    return blender_path


def blender_command(
    blender_exe: Path, stage_script: Path, stage_args: list[str]
) -> list[str]:
    return [
        str(blender_exe),
        "--background",
        "--factory-startup",
        "--python-exit-code",
        "1",
        "--python",
        str(stage_script),
        "--",
        *stage_args,
    ]


def run_stage(
    name: str,
    blender_exe: Path,
    stage_script: Path,
    stage_args: list[str],
    log_path: Path,
    working_dir: Path,
    allow_failure: bool = False,
) -> int:
    command = blender_command(blender_exe, stage_script, stage_args)
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"\n=== {name.upper()} ===\n")
        log_file.write(f"COMMAND: {' '.join(shlex.quote(part) for part in command)}\n")
        log_file.flush()

        process = subprocess.run(
            command,
            cwd=working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        log_file.write(process.stdout)
        log_file.write(f"\nEXIT CODE: {process.returncode}\n")

    if process.returncode != 0 and not allow_failure:
        raise SystemExit(
            f"{name} stage failed with exit code {process.returncode}. See {log_path}"
        )
    return process.returncode


def open_preview(preview_path: Path) -> None:
    if sys.platform.startswith("win"):
        os.startfile(str(preview_path))
        return
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.Popen([opener, str(preview_path)])


def main() -> int:
    args = parse_args()
    blender_exe = resolve_blender_exe()
    config_path = Path(args.config).resolve()
    if not config_path.exists():
        raise SystemExit(f"Config file not found: {config_path}")

    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    project_root = config_path.parent
    scene_path = output_dir / "scene.blend"
    preview_path = output_dir / "preview.png"
    hull_preview_path = output_dir / "hull_preview.png"
    report_path = output_dir / "report.json"
    log_path = output_dir / "pipeline.log"

    if log_path.exists():
        log_path.unlink()

    run_stage(
        "build",
        blender_exe,
        STAGES_DIR / "build_stage.py",
        [str(config_path), str(scene_path)],
        log_path,
        project_root,
    )
    run_stage(
        "render",
        blender_exe,
        STAGES_DIR / "render_stage.py",
        [str(config_path), str(scene_path), str(preview_path), str(hull_preview_path)],
        log_path,
        project_root,
    )
    validate_exit = run_stage(
        "validate",
        blender_exe,
        STAGES_DIR / "validate_stage.py",
        [
            str(config_path),
            str(scene_path),
            str(preview_path),
            str(hull_preview_path),
            str(report_path),
            str(log_path),
        ],
        log_path,
        project_root,
        allow_failure=True,
    )

    if report_path.exists():
        report = json.loads(report_path.read_text(encoding="utf-8"))
        status = report.get("status", "unknown")
        print(f"Pipeline completed with status: {status}")
        if status != "pass":
            return 2
    elif validate_exit != 0:
        raise SystemExit(
            f"validate stage failed with exit code {validate_exit}. See {log_path}"
        )

    print(f"Artifacts written to {output_dir}")
    if args.open_preview and preview_path.exists():
        open_preview(preview_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
