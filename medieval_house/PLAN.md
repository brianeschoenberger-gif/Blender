# Medieval House Build Plan (Automation Harness)

This plan uses the existing Automation workflow (`blender_automation/run_pipeline.py`) plus the script-first modeling patterns in `blender-object-builder`.

## 1) Intake and reference analysis

1. Confirm the reference image path and copy it into this project folder as `medieval_house/reference-image.png`.
2. Extract key targets from the image:
   - silhouette (height/width/depth ratio)
   - roof pitch and overhang
   - wall material split (timber frame vs plaster/stone)
   - door/window count and placement
   - secondary props (chimney, beams, shutters, steps)
3. Convert observations into a short, measurable spec in `medieval_house/house_params.py` (dimensions, counts, offsets, style toggles).

## 2) Scaffold a project matching the sailboat pattern

Create these files:

- `medieval_house/build_medieval_house.py` (builder entrypoint)
- `medieval_house/house_params.py` (all tunable constants)
- `medieval_house/medieval_house_builder/` package with modular generators:
  - `common.py`
  - `footprint.py`
  - `walls.py`
  - `timber_frame.py`
  - `roof.py`
  - `openings.py`
  - `props.py`
  - `materials.py`
- `medieval_house/pipeline_config.json`
- `medieval_house/README.md`

## 3) Build order (coarse-to-fine)

1. **Footprint + massing**
   - rectangular or L-shaped base block
   - one dominant roof volume
2. **Primary architectural structure**
   - walls and gables
   - roof planes and ridge
   - chimney block
3. **Openings**
   - door and window placeholders first
   - final frames/shutters second
4. **Style-defining details**
   - timber frame strips on wall faces
   - beam protrusions and trim
   - steps/sign/support beams
5. **Material assignment**
   - roof (tile/thatch), timber, plaster/stone, metal accents

Keep every stage runnable so `preview.png` can be reviewed after each increment.

## 4) Data-API-first implementation rules

Use the Blender object builder conventions throughout:

- Prefer `bpy.data` creation over `bpy.ops`.
- Explicitly name meshes/objects/collections.
- Link objects to target collections directly.
- Validate meshes via `mesh.validate()` + `mesh.update()`.
- Avoid relying on active object, selection, cursor, or UI context.

## 5) Collection and naming strategy

Use deterministic names so validation is stable:

- Root: `MedievalHouse`
- Child collections:
  - `Structure`
  - `Roof`
  - `Openings`
  - `Details`
  - `Props`
- Required objects (minimum):
  - `House_Base`
  - `House_Roof_Main`
  - `House_Door_Main`
  - `House_Chimney`

## 6) Validation contract in pipeline config

Define `pipeline_config.json` to include:

- `builder.script = medieval_house/build_medieval_house.py`
- `builder.function = build_medieval_house`
- `validation.root_collection = MedievalHouse`
- expected child collections, key objects, and required materials
- render framing for full-house preview and detail close-up

## 7) Iteration loop (recommended)

Run after every meaningful change:

```bash
python blender_automation/run_pipeline.py \
  --config medieval_house/pipeline_config.json \
  --output medieval_house/output/latest
```

Review in this order:

1. `report.json` for missing collection/object/material signals
2. `preview.png` for silhouette and proportion
3. targeted module edits (not broad rewrites)

## 8) Milestone plan

- **M1 (Blockout):** recognizable medieval house massing + clean validation pass
- **M2 (Architectural):** openings, chimney, and roof details aligned to reference
- **M3 (Styling):** timber-frame language + materials + prop polish
- **M4 (Final):** proportion tuning to reference and final render exports

## 9) Definition of done

1. Pipeline runs cleanly with no validation failures.
2. Final preview matches reference silhouette and key architectural motifs.
3. Parameters support at least 2 style variants (e.g., steeper roof, extra beams) without code changes.
4. Project README documents how to run and tune the generator.
