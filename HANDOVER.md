# Handover notes: Siteline 2D→3D prototype

*Informal, honest, and exactly the kind of note you'll get on day one of the real job.*

Hey, congrats, this one's yours now.

Two tools, both proven with the team, both written in an afternoon each:

- **The checker** gives the drafting team leads `worklist.csv` every morning instead of checking folders manually: what to draw, what doesn't belong.
- **The 2D→3D script** takes the drawn outlines and gives the modellers a massed-out `.blend` to start from instead of a blank file. They loved the demo. Then they started using it, and now they have opinions.

## Known quirks

- **AutoCAD keeps dropping `acadlt.err` files into the `01_CAD` folders.** Both tools crash on them. I just delete the file and rerun. One's probably in there now.
- **Marlowe 21 arrived from Bellbrook last week and I never got to run it.** If it breaks things, move the folder out of `projects/` like I've been doing and deal with Kestrel first. Their admin formats `project.json` a bit... creatively.
- **The scaffolding tool creates blank placeholder DXFs, and drafters sometimes save before actually drawing.** The checker counts those as drawn, which is optimistic. The 2D→3D script just crashes on them; I move the file out and rerun. Related: the checklist says the Kestrel WIR is drawn, but the modeller says there's nothing usable in the file.
- **Re-running the 3D script doubles everything up** (`.001` suffixes on every object). It opens the existing `.blend` first so nobody's manual tweaks get lost, which seemed clever at the time. When it gets messy I delete the `.blend` and start fresh, which of course loses the manual tweaks.
- **One of the Alfresco variants shows up on the upper storey in the model.** The drafter swears the drawing is fine, and the checker agrees with them. I haven't had time to look.
- **Ignore the default cube.** Never bothered removing it.
- **Wall height is hardcoded at 2.4 m in the script; the standard says 2450 mm.** A Bellbrook reviewer noticed. Oops.
- **Openings are drawn on their own layer in some files, and the script ignores them completely.** Doors and windows are what the modellers want most; right now they cut every opening by hand.
- **File naming discipline is inconsistent.** Someone saves with weird casing sometimes and the worklist tells them to redraw a thing that exists. Study got dropped from the Kestrel range in June and its drawing is still in the folder. And the `.bak` next to where the Balcony Ridgeline drawing should be: I'm fairly sure that *is* the drawing (AutoCAD backup naming), never confirmed it.
- **The standard file is meant to be the single source of truth**: naming, layers, every dimension. That's the whole Siteline philosophy: configuration over code, so a new builder or convention is a data change, not a release. I definitely hardcoded a few bits while demoing. Worth a look before a second standard ever arrives.

## Where this is heading

Right now the only way to interact with any of this is running scripts and opening a CSV, which is fine for me and useless for everyone else. The direction, so you can build with it in mind rather than against it:

- The team leads will need a proper UI to interact with this. Not now, but nothing you build should assume a human at a terminal forever.
- Feedback has to flow back to the drafters and modellers: why a file was flagged, what to fix, what's next for them. Today that's me explaining things on Teams, which doesn't scale.
- One day this may grow a client-facing side, builders checking their own project's status. That changes who you can trust and what you expose.
- Eventually it runs centrally on a schedule rather than on somebody's laptop, though probably not in the early phases.

None of that is in scope for your four hours. It's context for the calls you make.

The modellers want 3D output they can trust and build on, and everyone wants the worklist to be dependable. Pick what you can ship properly in the time you've got; anything you didn't get to, just say so in `STATUS.md`.

If this were real you'd ping me questions on Teams and I'd answer same-day. For the exercise, write the questions you *would have asked* into `STATUS.md`. I genuinely want to know what you'd have asked.
