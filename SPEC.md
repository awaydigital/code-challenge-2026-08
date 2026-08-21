# Spec: Siteline 2D→3D, and the extension backlog

## The domain, in five sentences

A **project** (`project.json`) lists rooms; each room has variants, and facade-driven rooms fan out per facade (others use the reserved facade `Any`). Every room × variant (× facade) is an **artefact**, and its name is computed from the template in the **standard** (`standards/siteline-2026-08-001.json`), never typed by hand. Drafters produce one DXF per artefact under `01_CAD/<level>/`, containing the room's outline. The **checker** derives the work list by comparing expected artefacts against the drawings on disk. The **2D→3D script** turns each outline into its 2D linework plus a rough open-top room shell, stacked per storey, in the project's `.blend`, which is the modelling team's starting point.

Two principles from the real system apply to everything you build:

1. **Configuration over code.** The standard file owns the values (naming template, separators, reserved words, layer names, dimensions). Code owns only the logic. A second standard with different values must work without a code change.
2. **Evidence over assertion.** Progress is derived from what's actually on disk, never from what anyone claims. Worth knowing: the checker currently counts a zero-byte file as "drawn".

## The backlog: pick what you can ship well

Deliberately unordered. Each item states why the production team wants it. All dimension values come from the standard's `dimensions` block, not from constants in code.

- **B1: Real walls.** Rooms currently extrude as zero-thickness shells. Give walls actual thickness (`wallThicknessMm`) and the correct height (`wallHeightMm`; note the script currently hardcodes a different number).
- **B2: Floor slabs.** A slab (`slabThicknessMm`) under each room, so the massing model stops floating.
- **B3: Openings.** Some DXFs carry `LINE` segments on the `OPENINGS` layer marking door/window gaps along the outline. Cut them into the walls: doors from floor to `doorHeightMm`, windows from `windowSillMm` to `windowHeadMm`. (For this exercise, treat any opening ≤ 1000 mm wide as a door and wider ones as windows.) This is what the modelling team wants most, and the hardest item here.
- **B4: Levels.** Storeys are stacked with a hardcoded 2.8 m, and a room's level comes from the folder its file sits in, never from the artefact name. Use `storeyHeightMm`, and trust the artefact name.
- **B5: Evidence export.** After building, write `02_Blender/{project}.facts.json` listing the objects created (artefact name, level, whatever else is useful), then teach the checker to read it and report the `model3d` stage: per-stage progress and a `MODEL` action on the worklist for drawn-but-unmodelled artefacts. An entry that matches no expected artefact should be reported, not counted.
- **B6: Safe re-runs.** Re-running `build3d.py` currently duplicates every object (`.001` suffixes). Make re-runs update in place. The same principle for the checker: a malformed project (try `marlowe21`) is quarantined and reported precisely while every other project still processes; stray files never crash a run; a failure partway doesn't lose the output.
- **B7: Foundations.** Tests, a CI workflow (GitHub Actions), TypeScript for checker code you add or change, and config values read from the standard everywhere instead of hardcoded.
- **B8: Serve it.** The first concrete step toward the direction in `HANDOVER.md` (a UI, feedback flowing back to the team, eventually central runs): a minimal read-only HTTP endpoint (latest worklist as JSON, plus a health check) fit for the office network. Auth is a token read from the environment, never from source, and requests that fail auth are logged. Add a paragraph to your STATUS production note on how you'd deploy and monitor it.

There is no correct subset. Depth beats breadth: one or two items shipped at production standard, with the baseline problems you noticed either fixed or written down, is a strong submission.

## Open questions: decide and document in `STATUS.md`

1. A file that differs from an expected artefact only by letter case (`kes38_...`): a match, a rename task, or an error? (The drafters are on Windows, where the filesystem doesn't care.)
2. `KES38_L1_Study-01_Base_Any.dxf` belongs to a room no longer in the project. What should the worklist say about it?
3. A `.bak` file sits where a missing artefact's `.dxf` should be. Evidence or noise?
4. What counts as CAD evidence: the file exists? is non-empty? contains a parseable outline? Define the tier, and what the checker should report for the file that fails it.

## DXF, in one minute (no CAD knowledge required)

A DXF is plain text: alternating lines of *group code* and *value*.

| Thing | How it appears |
|---|---|
| Units | `$INSUNITS` in the HEADER; `4` = millimetres |
| Room outline | one `LWPOLYLINE` entity on layer `OUTLINE` (layer = code `8`); code `90` = vertex count, `70` = `1` means closed; vertices are `10`/`20` (x/y) pairs in mm, in shared project coordinates (each room sits at its true position in the floor plan) |
| Door/window gap | a `LINE` on layer `OPENINGS`: `10`/`20` = start x/y, `11`/`21` = end x/y, lying along the outline |

The sample files are simplified (no TABLES/BLOCKS sections). Parse them by hand or use a library (`dxf-parser` on npm, `ezdxf` in Python). Your choice; note it in `STATUS.md`. Some strict libraries may want fuller files; text-level parsing is perfectly acceptable.

## Running Blender headless

```bash
blender --background --python tools/blender/build3d.py -- projects/bellbrook/kestrel38
```

Arguments after `--` reach the script. The default startup scene applies (yes, that's where the cube comes from). Blender's Python is self-contained; if you add Python dependencies, say how they get installed in your README.
