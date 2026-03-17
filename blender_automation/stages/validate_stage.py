from __future__ import annotations

import json
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from blender_automation.config import load_config


def stage_args() -> list[str]:
    if "--" not in sys.argv:
        raise SystemExit(
            "validate_stage.py requires config, scene, preview, hull preview, report, and log paths after '--'."
        )
    return sys.argv[sys.argv.index("--") + 1 :]


def write_report(report_path: Path, payload: dict) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def collection_triangle_count(collection: bpy.types.Collection) -> int:
    total = 0
    for obj in collection.all_objects:
        if obj.type != "MESH" or obj.data is None:
            continue
        for polygon in obj.data.polygons:
            total += max(1, len(polygon.vertices) - 2)
    return total


def main() -> int:
    args = stage_args()
    if len(args) != 6:
        raise SystemExit(
            "Usage: validate_stage.py -- <config.json> <scene.blend> <preview.png> <hull_preview.png> <report.json> <pipeline.log>"
        )

    config = load_config(args[0])
    scene_path = Path(args[1]).resolve()
    preview_path = Path(args[2]).resolve()
    hull_preview_path = Path(args[3]).resolve()
    report_path = Path(args[4]).resolve()
    log_path = Path(args[5]).resolve()

    bpy.ops.wm.open_mainfile(filepath=str(scene_path))

    checks: dict[str, bool] = {}
    warnings: list[str] = []
    validation = config["validation"]
    root_collection_name = validation["root_collection"]
    root_collection = bpy.data.collections.get(root_collection_name)
    checks["root_collection"] = root_collection is not None

    for name in validation.get("required_child_collections", []):
        checks[f"collection_{name.lower()}"] = (
            root_collection is not None and root_collection.children.get(name) is not None
        )

    for object_name in validation.get("required_objects", []):
        checks[f"object_{object_name.lower()}"] = bpy.data.objects.get(object_name) is not None

    for check_name, material_name in validation.get("required_materials", {}).items():
        checks[f"material_{check_name}"] = bpy.data.materials.get(material_name) is not None

    checks["preview_exists"] = preview_path.exists()
    checks["hull_preview_exists"] = hull_preview_path.exists()

    if root_collection is None:
        triangle_count = 0
        warnings.append(f"{root_collection_name} root collection is missing.")
    else:
        triangle_count = collection_triangle_count(root_collection)
        if triangle_count == 0:
            warnings.append("Triangle count is zero.")

    status = "pass" if all(checks.values()) else "fail"
    if not checks["preview_exists"]:
        warnings.append("Preview image is missing.")
    if not checks["hull_preview_exists"]:
        warnings.append("Hull preview image is missing.")

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
            "hull_preview_png": str(hull_preview_path),
            "report_json": str(report_path),
            "pipeline_log": str(log_path),
        },
    }
    write_report(report_path, payload)
    print(json.dumps(payload, indent=2))
    return 0 if status == "pass" else 2


if __name__ == "__main__":
    sys.exit(main())
