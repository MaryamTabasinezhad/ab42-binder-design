"""
Render presentation-quality docking figures for the top-5 Abeta42 binders.
Run headless:  pymol -cq render_top5.py
Chain layout (BindCraft output): chain A = Abeta42 fibril target (9CO4 C/E/G merged),
chain B = designed binder. Hotspots = Abeta42 residues 10,11,13,14,15,16 (each fibril chain).
For each design: an overview (binder vs target surface) + an interface close-up.
"""
import os
from pymol import cmd

BASE = "/global/project/hpcg6049/protein/alzheimer"
ACC = os.path.join(BASE, "bindcraft/designs/Accepted")
OUT = os.path.join(BASE, "album/renders")
os.makedirs(OUT, exist_ok=True)

# (rank, design_id, pdb_file)
DESIGNS = [
    (1, "ab42_l82_s967366_mpnn11", "ab42_l82_s967366_mpnn11_model2.pdb"),
    (2, "ab42_l89_s578974_mpnn11", "ab42_l89_s578974_mpnn11_model1.pdb"),
    (3, "ab42_l90_s311742_mpnn16", "ab42_l90_s311742_mpnn16_model1.pdb"),
    (4, "ab42_l71_s843399_mpnn18", "ab42_l71_s843399_mpnn18_model1.pdb"),
    (5, "ab42_l90_s311742_mpnn3",  "ab42_l90_s311742_mpnn3_model1.pdb"),
]

BINDER = "chain B"
TARGET = "chain A"
W, H = 2000, 1500

# global quality settings
cmd.set("ray_shadows", 1)
cmd.set("antialias", 2)
cmd.set("ray_trace_mode", 0)
cmd.set("cartoon_fancy_helices", 1)
cmd.set("cartoon_highlight_color", "grey60")
cmd.set("cartoon_transparency", 0.0)
cmd.set("surface_quality", 1)
cmd.set("specular", 0.25)
cmd.set("ambient", 0.35)
cmd.set("ray_opaque_background", 1)
cmd.bg_color("white")
cmd.set("depth_cue", 1)

C_BINDER = "marine"
C_TARGET = "wheat"
C_HOT = "orange"

for rank, did, fname in DESIGNS:
    path = os.path.join(ACC, fname)
    cmd.reinitialize()
    # re-apply quality (reinitialize resets settings)
    cmd.set("ray_shadows", 1); cmd.set("antialias", 2)
    cmd.set("cartoon_fancy_helices", 1); cmd.set("surface_quality", 1)
    cmd.set("specular", 0.25); cmd.set("ambient", 0.35)
    cmd.set("ray_opaque_background", 1); cmd.bg_color("white"); cmd.set("depth_cue", 1)
    cmd.set("transparency", 0.45)          # surface transparency
    cmd.set("surface_color", C_TARGET)

    cmd.load(path, "cplx")
    cmd.hide("everything")

    # --- interface selections (proximity based) ---
    cmd.select("if_b", f"(cplx and {BINDER}) within 5 of (cplx and {TARGET})")
    cmd.select("if_t", f"(cplx and {TARGET}) within 5 of (cplx and {BINDER})")
    # hotspot cluster (Abeta res 10-16) on the target, if present
    cmd.select("hot", f"cplx and {TARGET} and resi 10+11+13+14+15+16")

    # =========================================================
    # VIEW 1 — OVERVIEW: binder cartoon against translucent target surface
    # =========================================================
    cmd.show("cartoon", "cplx")
    cmd.color(C_BINDER, f"cplx and {BINDER}")
    cmd.color(C_TARGET, f"cplx and {TARGET}")
    cmd.show("surface", f"cplx and {TARGET}")
    cmd.set("transparency", 0.45)
    cmd.color(C_HOT, "hot")
    cmd.set("cartoon_side_chain_helper", 1)
    cmd.orient("cplx")
    cmd.zoom("cplx", 3)
    cmd.ray(W, H)
    cmd.png(os.path.join(OUT, f"{rank:02d}_{did}_overview.png"), dpi=300)

    # =========================================================
    # VIEW 2 — INTERFACE CLOSE-UP: contact side chains as sticks
    # =========================================================
    cmd.hide("surface")
    cmd.set("cartoon_transparency", 0.55, "cplx")
    cmd.show("sticks", "if_b")
    cmd.show("sticks", "if_t")
    cmd.color(C_BINDER, "if_b and elem C")
    cmd.color(C_TARGET, "if_t and elem C")
    cmd.color(C_HOT, "hot and elem C")
    cmd.show("sticks", "hot")
    cmd.set("stick_radius", 0.18)
    # thin translucent surface on interface target patch for context
    cmd.show("surface", "if_t")
    cmd.set("transparency", 0.7)
    cmd.orient("if_b or if_t")
    cmd.zoom("if_b or if_t", 2)
    cmd.ray(W, H)
    cmd.png(os.path.join(OUT, f"{rank:02d}_{did}_interface.png"), dpi=300)

    # report interface size
    nb = cmd.count_atoms("if_b and name CA")
    nt = cmd.count_atoms("if_t and name CA")
    nh = cmd.count_atoms("hot and name CA")
    print(f"RENDERED rank{rank} {did}: interface binder_res={nb} target_res={nt} hotspot_res_present={nh}")

print("ALL_RENDERS_DONE")
