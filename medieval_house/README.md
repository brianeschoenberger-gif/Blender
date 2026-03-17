# Medieval House Project

Procedural medieval house generator built for the shared Blender automation harness.

## Files

- `build_medieval_house.py`: Blender entrypoint used by the automation pipeline
- `house_params.py`: tunable dimensions + variant toggles
- `medieval_house_builder/`: modular build steps (footprint, walls, roof, openings, details, props, materials)
- `pipeline_config.json`: build/render/validate contract for `blender_automation/run_pipeline.py`

## Run pipeline

From repo root:

```bash
export BLENDER_EXE=/path/to/blender
python blender_automation/run_pipeline.py \
  --config medieval_house/pipeline_config.json \
  --output medieval_house/output/latest
```

## Quick tuning

Edit `DEFAULT_PARAMS` in `house_params.py`:

- `roof_height`, `roof_overhang` for silhouette
- `variant_toggles.extra_front_beam` for stronger timber framing
- `variant_toggles.shutters` and `variant_toggles.stone_steps` for detail level
