# Code Challenge 2026-08

Hiring exercise for **Lead Software Engineer, AI Delivery (Founding)** at Away Digital Group.

This mirrors the actual job. I do the discovery and build working prototypes; you turn them into production systems and own them: the reliability, the security, the support. This pack is a miniature week-one handover: a working 2D→3D drawing pipeline, a backlog, and four hours.

> **Everything in this pack is representative only.** It's modelled on a real internal system you'd work on, but all code, data, builders, projects, rules, names and dimensions are invented and heavily simplified. The baseline is *deliberately* prototype-grade.

## Start here

1. Read `HANDOVER.md`. It's my honest note to whoever takes this over. Five minutes.
2. Run both tools and open the result:

```bash
npm run intake                                    # the checker → worklist.csv
npm run build3d -- projects/bellbrook/kestrel38   # 2D→3D → 02_Blender/KES38.blend (open it in Blender)
```

3. Pick from the backlog in `SPEC.md` (it also explains the domain and the DXF format), write your plan in `STATUS.md`, and start the clock.

You need Node 20+ and Blender 4.x or newer (free, tested on 5.0). No npm installs. The checker side is Node, with TypeScript encouraged for anything you add or change; the Blender side is Python. You don't need to know Blender or CAD going in. On Windows, Blender's installer doesn't always add itself to PATH; use the full path to `blender.exe` or add it yourself.

## Rules

- **Four focused hours is a hard cap**, any time within 5 days of receiving this. We trust you to keep to it. Setup and reading don't count; the clock starts when you begin your plan in `STATUS.md`. Log your actual time and stop at four hours. Unfinished is fine, we'll discuss whatever's left at the interview.
- **AI tooling is expected.** Claude Code, Codex, Cursor, whatever you work best with, and use it as much as you like. You must be able to explain and defend every line you submit: the follow-up interview includes walking through your code and making a small live change to it.
- **Ship what you pick properly**: error handling, tests for what you add, documentation.
- **The baseline is yours.** Fix it, refactor it or work around it, but anything you notice and choose not to touch deserves a line in `STATUS.md`.
- **`git init` at the start and commit as you go.** We read the history to see how you sequenced the work.

## Deliverables

1. The code.
2. Tests, runnable with one documented command.
3. A `README.md` replacing this one: a new developer sets up and runs everything inside 10 minutes.
4. `STATUS.md`, weighted as heavily as the code:
   - your plan, written before you code, kept unedited (append, don't rewrite)
   - an honest time log
   - what you picked and why; what's done and what's not
   - what you noticed about the baseline and how you handled it
   - your calls on the open questions in `SPEC.md`, plus the questions you'd have asked me if this were real
   - AI notes: what tooling, where it excelled, at least one place you overrode or corrected it
   - how you'd run this in production: where it runs, how it's triggered, where secrets and access live, and how someone finds out it broke
   - what next week and next month look like if you own this

## Submission

Don't fork this repo; forks are public and would hand your solution to every other candidate. Download a copy and `git init` fresh. Within your 5-day window, share a **private** GitHub repo with `danny-awaydigital` invited as a collaborator, and please keep the challenge and your solution private.

## How it's assessed

What you shipped and whether it actually works; the judgement in what you picked; what you noticed about the baseline (the sample data has problems the handover hints at); tests; an honest `STATUS.md`; and whether you controlled your AI tooling or it controlled you.

Good luck. The cap is real: stop at four hours and tell us where you got to.
