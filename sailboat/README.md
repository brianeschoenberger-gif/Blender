# Sailboat Project

This folder contains the sailboat generator, its headless Blender automation harness, and the working reference image used during refinement.

## Main entrypoints

- `build_sailboat.py`: direct Blender script entrypoint
- `automation/run_pipeline.py`: headless build-render-validate runner
- `reference-image.png`: reference image for silhouette and proportion tuning

## Recommended workflow

From the repo root:

```powershell
$env:BLENDER_EXE="C:\Path\To\blender.exe"
python sailboat/automation/run_pipeline.py --output sailboat/output/latest --open-preview
```

This produces:

- `sailboat/output/latest/scene.blend`
- `sailboat/output/latest/preview.png`
- `sailboat/output/latest/hull_preview.png`
- `sailboat/output/latest/report.json`
- `sailboat/output/latest/pipeline.log`
