# Sailboat Project

This folder contains the sailboat generator, its pipeline config, and the working reference image used during refinement.

## Main entrypoints

- `build_sailboat.py`: direct Blender script entrypoint
- `pipeline_config.json`: config consumed by the shared Blender automation layer
- `reference-image.png`: reference image for silhouette and proportion tuning

## Recommended workflow

From the repo root:

```powershell
$env:BLENDER_EXE="C:\Path\To\blender.exe"
python blender_automation/run_pipeline.py --config sailboat/pipeline_config.json --output sailboat/output/latest --open-preview
```

This produces:

- `sailboat/output/latest/scene.blend`
- `sailboat/output/latest/preview.png`
- `sailboat/output/latest/hull_preview.png`
- `sailboat/output/latest/report.json`
- `sailboat/output/latest/pipeline.log`
