# Blender Automation Harness

This folder lets Codex run the sailboat generator in headless Blender, render both an overall preview and a hull-focused preview, and emit a structural validation report.

## Usage

Set `BLENDER_EXE` to the full path of your Blender executable, then run:

```powershell
python sailboat/automation/run_pipeline.py --output sailboat/output/latest
```

To open the rendered preview automatically after a successful run:

```powershell
python sailboat/automation/run_pipeline.py --output sailboat/output/latest --open-preview
```

## Artifacts

- `scene.blend`
- `preview.png`
- `hull_preview.png`
- `report.json`
- `pipeline.log`

## Stage order

1. `build_stage.py` creates the sailboat scene and saves `scene.blend`.
2. `render_stage.py` opens the saved scene and renders `preview.png` plus `hull_preview.png`.
3. `validate_stage.py` opens the saved scene and writes `report.json`.
