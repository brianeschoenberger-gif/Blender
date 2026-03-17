from __future__ import annotations

from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from build_sailboat import build_sailboat


def stage_args() -> list[str]:
    if "--" not in sys.argv:
        raise SystemExit("build_stage.py requires a scene output path after '--'.")
    return sys.argv[sys.argv.index("--") + 1 :]


def main() -> int:
    args = stage_args()
    if len(args) != 1:
        raise SystemExit("Usage: build_stage.py -- <scene.blend>")

    scene_path = Path(args[0]).resolve()
    scene_path.parent.mkdir(parents=True, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    build_sailboat()
    bpy.ops.wm.save_as_mainfile(filepath=str(scene_path))
    print(f"Saved scene to {scene_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
