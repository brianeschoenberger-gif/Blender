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

    if bpy.data.filepath:
        candidates.append(Path(bpy.data.filepath).resolve().parent)

    candidates.append(Path.cwd())

    dedup: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        dedup.append(candidate)
    return dedup


def _bootstrap_project_root() -> Path:
    for candidate in _candidate_roots():
        if (candidate / "house_params.py").exists() and (candidate / "medieval_house_builder").is_dir():
            if str(candidate) not in sys.path:
                sys.path.insert(0, str(candidate))
            return candidate

    searched = "\n".join(f"- {path}" for path in _candidate_roots())
    raise ModuleNotFoundError(
        "Could not locate medieval_house project root. Ensure build_medieval_house.py runs from its folder.\n"
        f"Searched:\n{searched}"
    )


ROOT = _bootstrap_project_root()


def _reload_local_modules() -> None:
    module_names = [
        "house_params",
        "medieval_house_builder.common",
        "medieval_house_builder.materials",
        "medieval_house_builder.footprint",
        "medieval_house_builder.walls",
        "medieval_house_builder.roof",
        "medieval_house_builder.openings",
        "medieval_house_builder.timber_frame",
        "medieval_house_builder.props",
    ]
    for module_name in module_names:
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])


_reload_local_modules()

from house_params import DEFAULT_PARAMS, MedievalHouseParams
from medieval_house_builder.common import delete_collection_tree, ensure_child_collections, ensure_collection
from medieval_house_builder import (
    build_base,
    build_chimney,
    build_door,
    build_main_roof,
    build_props,
    build_timber_frame,
    build_walls,
    build_windows,
    ensure_materials,
)


def build_medieval_house(params: MedievalHouseParams = DEFAULT_PARAMS) -> bpy.types.Collection:
    print(f"Building medieval house with Blender {bpy.app.version_string}")

    delete_collection_tree(params.name)
    root = ensure_collection(params.name)
    collections = ensure_child_collections(root, ["Structure", "Roof", "Openings", "Details", "Props"])
    materials = ensure_materials()

    build_base(params, collections["Structure"], materials)
    build_walls(params, collections["Structure"], materials)
    build_main_roof(params, collections["Roof"], materials)
    build_chimney(params, collections["Roof"], materials)
    build_door(params, collections["Openings"], materials)
    build_windows(params, collections["Openings"], materials)
    build_timber_frame(params, collections["Details"], materials)
    build_props(params, collections["Props"], materials)

    return root


if __name__ == "__main__":
    build_medieval_house()
