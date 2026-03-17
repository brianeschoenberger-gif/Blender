# Blender Automation

Reusable headless Blender build-render-validate pipeline for project-specific object generators.

## Usage

Provide a project config JSON and an output directory:

```powershell
$env:BLENDER_EXE="C:\Path\To\blender.exe"
python blender_automation/run_pipeline.py --config sailboat/pipeline_config.json --output sailboat/output/latest --open-preview
```

## Required project config

Each project provides a JSON file with:

- `builder.script`: relative path to the project builder script
- `builder.function`: function to call inside that script
- `validation.root_collection`
- `validation.required_child_collections`
- `validation.required_objects`
- `validation.required_materials`

Optional `render` settings can override the default full-preview and hull-preview camera framing.
