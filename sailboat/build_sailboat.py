from __future__ import annotations

import importlib
import sys
from pathlib import Path

import bpy


def _candidate_roots() -> list[Path]:
    candidates: list[Path] = []

    file_hint = globals().get("__file__")
    if file_hint:
        candidates.append(Path(file_hint).resolve().parent)

    try:
        blend_path = bpy.data.filepath
    except Exception:
        blend_path = ""
    if blend_path:
        candidates.append(Path(blend_path).resolve().parent)

    for text in bpy.data.texts:
        filepath = getattr(text, "filepath", "")
        if filepath:
            candidates.append(Path(filepath).resolve().parent)

    candidates.append(Path.cwd())

    unique_candidates: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        unique_candidates.append(candidate)
    return unique_candidates


def _bootstrap_project_root() -> Path:
    for candidate in _candidate_roots():
        if (candidate / "sailboat_params.py").exists() and (candidate / "sailboat_builder").is_dir():
            if str(candidate) not in sys.path:
                sys.path.insert(0, str(candidate))
            return candidate

    searched = "\n".join(f"- {path}" for path in _candidate_roots())
    raise ModuleNotFoundError(
        "Could not locate the sailboat project root. Open build_sailboat.py from its real folder or "
        "add the project directory to sys.path before running.\n"
        f"Searched:\n{searched}"
    )


ROOT = _bootstrap_project_root()


def _reload_local_modules() -> None:
    module_names = [
        "sailboat_params",
        "sailboat_builder.common",
        "sailboat_builder.materials",
        "sailboat_builder.hull",
        "sailboat_builder.deckhouse",
        "sailboat_builder.rigging",
        "sailboat_builder.sails",
        "sailboat_builder.details",
    ]

    for module_name in module_names:
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])


_reload_local_modules()

from sailboat_params import DEFAULT_PARAMS, SailboatParams
from sailboat_builder.common import (
    collection_triangle_count,
    delete_collection_tree,
    ensure_child_collections,
    ensure_collection,
    make_empty,
)
from sailboat_builder.deckhouse import build_deckhouse
from sailboat_builder.details import build_details
from sailboat_builder.hull import build_hull
from sailboat_builder.materials import ensure_materials
from sailboat_builder.rigging import build_rigging
from sailboat_builder.sails import build_sails


def build_sailboat(params: SailboatParams = DEFAULT_PARAMS) -> bpy.types.Collection:
    print(f"Building sailboat with Blender {bpy.app.version_string}")

    delete_collection_tree(params.name)
    root_collection = ensure_collection(params.name)
    root_empty = make_empty(f"{params.name}_Root", root_collection)
    root_empty.empty_display_type = "PLAIN_AXES"

    collections = ensure_child_collections(
        root_collection,
        ["Hull", "Deckhouse", "Rig", "Sails", "Canopy", "Details"],
    )
    materials = ensure_materials(params)

    context = {
        "root_empty": root_empty,
        "root_collection": root_collection,
        "collections": collections,
        "materials": materials,
    }

    hull_data = build_hull(params, context)
    deckhouse_data = build_deckhouse(params, context)
    rigging_data = build_rigging(params, context)
    sails_data = build_sails(params, context, rigging_data)
    build_details(params, context, hull_data, deckhouse_data, rigging_data, sails_data)

    print(f"Estimated triangle count: {collection_triangle_count(root_collection)}")
    return root_collection


if __name__ == "__main__":
    build_sailboat()
