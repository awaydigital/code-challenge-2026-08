# build3d.py - 2d to 3d, quick and dirty but it works!
# run from the repo root:
#   blender --background --python tools/blender/build3d.py -- projects/bellbrook/kestrel38
import bpy
import json
import os
import sys


def read_outline(path):
    # dxf is just code/value line pairs, easy enough to read by hand
    lines = open(path).read().splitlines()
    pairs = list(zip(lines[0::2], lines[1::2]))
    verts = []
    x = 0.0
    inpoly = False
    for code, val in pairs:
        code = code.strip()
        if code == "0":
            if inpoly:
                break  # end of the polyline
            inpoly = val.strip() == "LWPOLYLINE"
            continue
        if inpoly and code == "10":
            x = float(val)
        if inpoly and code == "20":
            verts.append((x, float(val)))
    return verts


def build_room(name, verts_mm, z):
    import bmesh
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((x / 1000.0, y / 1000.0, z)) for x, y in verts_mm]
    floor = bm.faces.new(vs)
    ret = bmesh.ops.extrude_edge_only(bm, edges=list(bm.edges))
    for g in ret["geom"]:
        if isinstance(g, bmesh.types.BMVert):
            g.co.z = z + 2.4  # wall height, close enough for the demo
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def add_outline(name, verts_mm, z):
    # keep the 2d linework in the file, the modellers like tracing over it
    curve = bpy.data.curves.new(name + "_2d", "CURVE")
    curve.dimensions = "3D"
    spline = curve.splines.new("POLY")
    spline.points.add(len(verts_mm) - 1)
    for point, (x, y) in zip(spline.points, verts_mm):
        point.co = (x / 1000.0, y / 1000.0, z, 1.0)
    spline.use_cyclic_u = True
    obj = bpy.data.objects.new(name + "_2d", curve)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def run(project_dir):
    project = json.load(open(os.path.join(project_dir, "project.json")))
    out_dir = os.path.join(project_dir, "02_Blender")
    os.makedirs(out_dir, exist_ok=True)
    blend = os.path.abspath(os.path.join(out_dir, project["code"] + ".blend"))

    if os.path.exists(blend):
        bpy.ops.wm.open_mainfile(filepath=blend)  # don't lose my manual tweaks

    cad = os.path.join(project_dir, "01_CAD")
    count = 0
    for level in sorted(os.listdir(cad)):
        z = (int(level[1]) - 1) * 2.8  # storey height, near enough
        for f in sorted(os.listdir(os.path.join(cad, level))):
            if f.endswith(".dxf"):
                verts = read_outline(os.path.join(cad, level, f))
                build_room(f[:-4], verts, z)
                add_outline(f[:-4], verts, z)
                count += 1
                print("built " + f[:-4])

    bpy.ops.wm.save_as_mainfile(filepath=blend)
    print("saved " + blend + " - " + str(count) + " rooms")


if __name__ == "__main__":
    args = sys.argv
    target = args[args.index("--") + 1] if "--" in args else args[1]
    run(target)
