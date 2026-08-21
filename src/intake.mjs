// intake.mjs — Siteline intake check, quick prototype v2 (this one works!)
// usage: npm run intake

import fs from "node:fs";
import path from "node:path";

const standard = JSON.parse(fs.readFileSync("standards/siteline-2026-08-001.json", "utf8"));

function expectedArtefacts(project) {
  const out = [];
  for (const room of project.rooms) {
    for (const variant of room.variants) {
      if (room.facadeDriven) {
        for (const facade of project.facades) {
          out.push(project.code + "_" + room.level + "_" + room.name + "-" + room.seq + "_" + variant + "_" + facade);
        }
      } else {
        out.push(project.code + "_" + room.level + "_" + room.name + "-" + room.seq + "_" + variant + "_Any");
      }
    }
  }
  return out;
}

function scanCad(dir) {
  const found = [];
  for (const level of fs.readdirSync(dir)) {
    for (const f of fs.readdirSync(path.join(dir, level))) {
      if (f.endsWith(".dxf")) {
        found.push(f.replace(".dxf", ""));
      }
    }
  }
  return found;
}

function main() {
  const rows = [];
  let drawn = 0;
  let missing = 0;

  for (const builder of fs.readdirSync("projects")) {
    for (const projName of fs.readdirSync(path.join("projects", builder))) {
      const project = JSON.parse(
        fs.readFileSync(path.join("projects", builder, projName, "project.json"), "utf8")
      );
      console.log("== " + project.name + " (" + project.code + ")");

      const expected = expectedArtefacts(project);
      const found = scanCad(path.join("projects", builder, projName, "01_CAD"));

      for (const artefact of expected) {
        if (found.includes(artefact)) {
          drawn++;
        } else {
          missing++;
          rows.push(artefact + ",DRAW,");
          console.log("  DRAW    " + artefact);
        }
      }

      for (const orphan of found.filter((f) => !expected.includes(f))) {
        rows.push(orphan + ",ORPHAN,file does not match any expected artefact");
        console.log("  ORPHAN  " + orphan);
      }
    }
  }

  fs.writeFileSync("worklist.csv", "artefact,action,notes\n" + rows.join("\n") + "\n");

  console.log("");
  console.log("done: " + drawn + " drawn, " + missing + " to draw. worklist.csv written.");
  console.log("progress: " + Math.round((drawn / (drawn + missing)) * 100) + "%");
}

main();
