from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from blender_automation.config import load_config


def stage_args() -> list[str]:
    if "--" not in sys.argv:
        raise SystemExit("build_stage.py requires a config path and scene output path after '--'.")
    return sys.argv[sys.argv.index("--") + 1 :]


def load_builder_callable(config: dict):
    project_root = Path(config["project_root"])
    builder_script = project_root / config["builder"]["script"]
    module_name = f"blender_project_builder_{builder_script.stem}"
    spec = importlib.util.spec_from_file_location(module_name, builder_script)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load builder script: {builder_script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    function_name = config["builder"]["function"]
    build_fn = getattr(module, function_name, None)
    if build_fn is None:
        raise SystemExit(f"Builder function '{function_name}' not found in {builder_script}")
    return build_fn


def main() -> int:
    args = stage_args()
    if len(args) != 2:
        raise SystemExit("Usage: build_stage.py -- <config.json> <scene.blend>")

    config = load_config(args[0])
    scene_path = Path(args[1]).resolve()
    scene_path.parent.mkdir(parents=True, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    build_fn = load_builder_callable(config)
    build_fn()
    bpy.ops.wm.save_as_mainfile(filepath=str(scene_path))
    print(f"Saved scene to {scene_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
