# Medieval House Build Plan

## Summary

- Build this as a scripted, game-ready medieval cottage inspired by the provided multi-view reference, not as a photogrammetric copy.
- Prioritize silhouette, massing, and material breakup first: stone base, timber-framed upper floor, steep central gable, layered roof masses, chimney, porch/lean-to structures, and clustered props.
- Keep the asset modular and parameter-driven so the same generator can later produce nearby variants without rewriting the build logic.

## Reference Read

The reference shows a compact late-medieval / fantasy cottage with these defining traits:

- A tall, steep front gable that dominates the silhouette.
- A heavier stone ground floor and lighter timber-framed plaster upper walls.
- A main roof plus multiple attached secondary roof pieces, not one simple box roof.
- Clear asymmetry from side to side.
- A front-centered arched main door, small balcony/flower box at the upper front, and secondary side entries / lean-tos.
- One prominent chimney and rough, irregular roof edges with patchwork character.
- Dense small props at the base: barrels, crates, plants, fences, steps, posts.

## Asset Strategy

Use one orchestrator plus specialized builder modules:

- `build_medieval_house.py`
  - scene setup
  - collection creation
  - top-level orchestration
- `house_params.py`
  - dimensions
  - roof pitch / overhang
  - floor heights
  - porch sizes
  - opening layout
  - style toggles
- `medieval_house_builder/`
  - `footprint.py`
  - `walls.py`
  - `timber_frame.py`
  - `roof.py`
  - `openings.py`
  - `props.py`
  - `materials.py`
  - `common.py`

## Core Build Order

### 1. Footprint and major masses

Start from a footprint that reflects the reference instead of a plain rectangle:

- Main rectangular house body
- Slight rear extension / side massing offset
- Small attached porch or lean-to masses on at least two sides

Output:

- `House_Base`
- helper empties / reference anchors for front, back, left, right

Goal:

- From a distance, the outline should already read as “storybook medieval house,” not just a box.

### 2. Ground floor stone structure

Build the heavier lower floor first:

- thicker wall body
- subtle irregularity in wall face depth
- arched front doorway cut-in
- optional side doorway
- stone material assignment

Keep the lower floor simpler and chunkier than the upper floor so the contrast reads clearly.

Output:

- `Walls_Ground`
- `Door_Main_Frame`
- `Door_Main`

### 3. Upper floor and front gable

Add the upper timber-framed/plaster body as a separate stage:

- slightly inset or lighter-feeling upper mass
- main front gable face
- upper window placements
- balcony or flower-box support region at the front

This is the style-defining facade. Match the front view in the reference before detailing side views.

Output:

- `Walls_Upper`
- `Gable_Front`
- `Gable_Back`

### 4. Roof system

Treat the roof as several related masses rather than one mesh:

- main steep roof
- smaller side / porch / lean-to roof pieces
- roof ridge cap
- chimney penetration
- deliberate unevenness in eaves and ridge line

The roof is one of the strongest identifiers in the reference, so spend parameter budget here.

Output:

- `Roof_Main`
- `Roof_Porch_Left`
- `Roof_Porch_Right`
- `Roof_Rear` if needed
- `Chimney`

### 5. Timber framing pass

Apply timber framing as explicit strip geometry, not just texture implication:

- vertical posts
- horizontal rails
- diagonal braces
- front gable pattern first
- side-wall framing second

The front gable timber pattern should be the highest-priority decorative pass because it strongly defines the facade.

Output:

- `TimberFrame_Front`
- `TimberFrame_Sides`
- `TimberFrame_Back`

### 6. Openings and facade details

Add openings only after the major wall and roof masses are correct:

- arched front door
- upper front windows
- side windows
- small dormers only if they support silhouette and do not overcomplicate V1
- shutters, balcony rail, flower boxes, canopy pieces

Output:

- `Windows_Main`
- `Shutters`
- `Balcony`
- `Canopies`

### 7. Ground props and storytelling details

The reference includes a lot of clutter around the base. Keep these modular and optional:

- barrels
- crates
- sacks
- fence segments
- planters
- steps
- support posts
- low shrubs / vines if simple enough

These should improve readability and mood but not become the main modeling challenge.

Output:

- `Props_Entry`
- `Props_Side`
- `Fence_Segments`

## Collection Strategy

Use stable collection names so validation remains deterministic:

- `MedievalHouse`
  - `Structure`
  - `Roof`
  - `Timber`
  - `Openings`
  - `Details`
  - `Props`

Minimum required object names:

- `House_Base`
- `Walls_Ground`
- `Walls_Upper`
- `Roof_Main`
- `Chimney`
- `Door_Main`

## Parameter Plan

Keep these exposed in `house_params.py`:

- overall width / depth / total height
- ground floor height
- upper floor height
- roof pitch
- roof overhang
- gable depth
- porch width / depth / height
- chimney width / height / offset
- timber thickness
- window count and spacing
- prop toggles

Useful style toggles:

- `front_balcony`
- `left_lean_to`
- `right_lean_to`
- `extra_chimney`
- `dense_props`
- `shutters`
- `flower_boxes`

## Implementation Rules

- Prefer `bpy.data` API and explicit mesh creation over UI operators.
- Use simple reusable mesh primitives and helper functions where possible.
- Use modifiers only where predictable and low-risk:
  - bevel for broad softening
  - solidify only if truly needed
- Do not rely on cloth, geometry nodes, or scene-state assumptions for V1.
- Keep all objects named and linked explicitly.

## Validation Plan

Update `pipeline_config.json` so validation checks:

- root collection: `MedievalHouse`
- child collections present
- key objects present
- required materials present:
  - stone
  - plaster
  - timber
  - roof
  - metal
  - glass
- both preview renders exist

## Render Review Plan

Use two preview goals:

- full preview:
  - checks overall silhouette and composition
- facade / hull-style close preview:
  - focused on front gable, door, balcony, timber framing, and ground-floor material split

For visual review, prioritize these questions:

1. Does the roof silhouette match the reference’s steep, layered feel?
2. Does the stone-to-timber material split read clearly?
3. Does the front facade feel asymmetrical and handcrafted rather than boxy?
4. Are the porch / lean-to forms helping the shape?
5. Do props support the composition without overwhelming it?

## Milestones

### M1. Blockout

- Main footprint
- Ground floor
- Upper floor
- Main roof
- Chimney

Success criteria:

- recognizable medieval-house silhouette in preview

### M2. Architectural pass

- lean-to roofs
- door / windows
- balcony
- stronger gable massing

Success criteria:

- front and side views resemble the reference structure

### M3. Style pass

- timber framing
- roof edge breakup
- shutters / flower boxes
- porch supports

Success criteria:

- asset reads as handcrafted medieval architecture, not a generic cottage

### M4. Prop and polish pass

- barrels, crates, fence, steps, planters
- final material tuning
- render framing refinements

Success criteria:

- believable game-ready exterior with good readability at medium distance

## Assumptions

- V1 is exterior-only.
- The target is a believable stylized game asset, not a perfect historical reconstruction.
- The best path is modular scripted construction with layered objects, not monolithic mesh code.
- Fine roof damage, ivy growth, and dense irregular sculpting are optional later passes, not part of the base build.
