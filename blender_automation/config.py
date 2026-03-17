from __future__ import annotations

import json
from pathlib import Path


def load_config(config_path: str | Path) -> dict:
    path = Path(config_path).resolve()
    config = json.loads(path.read_text(encoding="utf-8"))
    config["config_path"] = str(path)
    config["project_root"] = str(path.parent.resolve())
    return config
