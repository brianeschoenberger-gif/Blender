from __future__ import annotations

import json
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sailboat_builder.common import collection_triangle_count


ROOT_COLLECTION = "Sailboat"
REQUIRED_CHILD_COLLECTIONS = ["Hull", "Deckhouse", "Rig", "Sails", "Canopy", "Details"]
REQUIRED_OBJECTS = ["Hull", "Mast", "Boom", "MainSail", "Jib"]
REQUIRED_MATERIALS = {
    "hull": "Sailboat_Hull",
    "deck": "Sailboat_Deck",
    "cabin": "Sailboat_Cabin",
    "sail": "Sailboat_Sail",
    "canopy": "Sailboat_Canopy",
    "metal": "Sailboat_Metal",
    "window": "Sailboat_Window",
}


def stage_args() -> list[str]:
    if "--" not in sys.argv:
        raise SystemExit(
            "validate_stage.py requires scene, preview, report, and log paths after '--'."
        )
    return sys.argv[sys.argv.index("--") + 1 :]


def write_report(report_path: Path, payload: dict) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    args = stage_args()
    if len(args) != 4:
        raise SystemExit(
            "Usage: validate_stage.py -- <scene.blend> <preview.png> <report.json> <pipeline.log>"
        )

    scene_path = Path(args[0]).resolve()
    preview_path = Path(args[1]).resolve()
    report_path = Path(args[2]).resolve()
    log_path = Path(args[3]).resolve()

    bpy.ops.wm.open_mainfile(filepath=str(scene_path))

    checks: dict[str, bool] = {}
    warnings: list[str] = []

    root_collection = bpy.data.collections.get(ROOT_COLLECTION)
    checks["root_collection"] = root_collection is not None

    for name in REQUIRED_CHILD_COLLECTIONS:
        checks[f"collection_{name.lower()}"] = (
            root_collection is not None and root_collection.children.get(name) is not None
        )

    for object_name in REQUIRED_OBJECTS:
        checks[f"object_{object_name.lower()}"] = bpy.data.objects.get(object_name) is not None

    for check_name, material_name in REQUIRED_MATERIALS.items():
        checks[f"material_{check_name}"] = bpy.data.materials.get(material_name) is not None

    checks["preview_exists"] = preview_path.exists()

    if root_collection is None:
        triangle_count = 0
        warnings.append("Sailboat root collection is missing.")
    else:
        triangle_count = collection_triangle_count(root_collection)
        if triangle_count == 0:
            warnings.append("Triangle count is zero.")

    status = "pass" if all(checks.values()) else "fail"
    if not checks["preview_exists"]:
        warnings.append("Preview image is missing.")

    payload = {
        "status": status,
        "blender_version": bpy.app.version_string,
        "checks": checks,
        "warnings": warnings,
        "metrics": {
            "triangle_count": triangle_count,
            "object_count": len(bpy.data.objects),
            "material_count": len(bpy.data.materials),
        },
        "artifacts": {
            "scene_blend": str(scene_path),
            "preview_png": str(preview_path),
            "report_json": str(report_path),
            "pipeline_log": str(log_path),
        },
    }
    write_report(report_path, payload)
    print(json.dumps(payload, indent=2))
    return 0 if status == "pass" else 2


if __name__ == "__main__":
    sys.exit(main())
