# Sailboat Refinement Plan (Current Generator -> Reference Match)

This plan focuses on moving the generated model significantly closer to `reference-image.png` using the existing modular builder pipeline.

## 1) Establish a repeatable visual diff loop

1. Render both full and hull previews after every change via `blender_automation/run_pipeline.py`.
2. Keep camera/lens fixed in `pipeline_config.json` while iterating so proportion changes are comparable.
3. For each iteration, score these buckets (1–5):
   - hull sheer + freeboard silhouette
   - mast/sail proportions
   - deckhouse + window placement
   - cockpit/canopy silhouette
   - bow/stern rails and deck hardware density

**Goal:** each iteration changes only one or two buckets so regressions are easy to spot.

---

## 2) Correct global proportions first (biggest visual wins)

Target the highest-impact parameters in `sailboat_params.py` before fine details.

### 2.1 Hull stance and sheer

Tune these first:
- `hull_length`, `beam`, `hull_height`
- `hull_profile` control points (beam falloff + keel/deck shaping)
- `deck_height` and `deck_profile`

Desired direction vs current render:
- Slightly cleaner, flatter topside run amidships with gentle rise toward bow.
- Fuller mid-body but soft taper into stern.
- More distinct blue bootstripe alignment near waterline.

### 2.2 Rig proportions

Tune:
- `mast_height`, `mast_x`, `boom_length`, `boom_z`
- `jib_foretriangle_height`
- sail camber + paneling behavior in `sails.py`

Desired direction:
- Tall, slender mast profile with foretriangle similar to reference.
- Boom/foot line sitting just above deckhouse/cockpit line.
- Main and jib leeches appearing less “baggy” and more controlled.

---

## 3) Refine hull geometry and deck break lines

Work in `sailboat_builder/hull.py` and associated profile sampling.

1. Improve sectional fairness in bow entry and stern run.
2. Sharpen deck-to-hull transition where the rub rail/cove stripe reads in side view.
3. Ensure bow overhang and transom curvature match reference silhouette.
4. Verify normals/smoothing so highlights run continuously along topsides.

**Acceptance check:** at thumbnail size, the hull outline should read as the same “family” as the reference even before details.

---

## 4) Deckhouse and cockpit canopy silhouette

Work primarily in `deckhouse.py`.

1. Rebuild deckhouse side profile to a lower, sleeker cabin trunk.
2. Re-space window openings to match reference rhythm (long side window + smaller ports).
3. Rework bimini/canopy arc: lower forward edge, slightly crowned top, aft extension over cockpit.
4. Tighten canopy support geometry and junctions at deck.

**Why now:** in this reference, canopy + cabin windows are the second-strongest identity cues after hull/sails.

---

## 5) Sail shaping and rigging cleanup

Work in `sails.py` and `rigging.py`.

1. Add more realistic sail edge control (luff straightness, smoother roach, restrained camber gradient).
2. Add subtle cloth twist/flattening from tack to head (small values only).
3. Reposition forestay/backstay/shrouds to align with mast and chainplate locations.
4. Keep rigging thin and understated to avoid overpowering silhouette.

---

## 6) Detail pass (only after silhouette matches)

Work in `details.py`.

1. Bow pulpit/pushpit rails: align heights and bends to reference.
2. Stanchions/lifelines: spacing consistency and clean termination near stern.
3. Cleats/winches/deck fittings: reduce or add density to match the visible deck clutter level.
4. Portlight/porthole placement and sizing along hull side.

**Rule:** if a detail competes with major shape mismatches, defer it.

---

## 7) Material and shading calibration

Work in `materials.py`.

1. Hull gelcoat: brighter white base, slightly broader specular, cleaner reflections.
2. Blue accents (stripe + canvas): deeper saturated navy and more consistent hue across parts.
3. Sail fabric: translucent light gray with subtle panel seam contrast.
4. Metal rails/fittings: lower roughness variation, avoid noisy highlights.
5. Window glass: darker tint with controlled transparency.

---

## 8) Validation + quality gates

Keep existing structural checks in `pipeline_config.json`, and add visual gates:

1. Side-view overlay check against `reference-image.png` (manual or scripted image overlay).
2. Triangle count sanity: avoid runaway mesh complexity while refining.
3. Naming/collection integrity unchanged so automation still passes.
4. Final pass in both full and hull preview cameras.

---

## 9) Suggested execution sequence (8 iterations)

1. Baseline render + scorecard.
2. Global hull proportions.
3. Rig proportions.
4. Hull fairness and deck break lines.
5. Deckhouse + canopy silhouette.
6. Sail shape + rigging placement.
7. Detail and hardware pass.
8. Materials polish + final validation.

This sequence maximizes visual impact early and prevents spending time polishing details on incorrect proportions.
