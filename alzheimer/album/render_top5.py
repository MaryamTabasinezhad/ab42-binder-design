"""
Render the top-5 Abeta42 binder complexes in the ternary_fusions HOUSE STYLE.
Reference: alzheimer/ternary_fusions/*.png
  - 2400x1800, background (12,14,18), ray-traced opaque
  - cartoon DOMINANT + faint translucent molecular-surface glow (transparency 0.88)
  - soft cornflower binder (chain B), orange Abeta42 target (chain A)
Single whole-complex view per design (no zoom), matching the reference figures.
Run headless:  pymol -cq render_top5.py
"""
import os
from pymol import cmd

BASE = "/global/project/hpcg6049/protein/alzheimer"
ACC = os.path.join(BASE, "bindcraft/designs/Accepted")
OUT = os.path.join(BASE, "album/renders")
os.makedirs(OUT, exist_ok=True)

DESIGNS = [
    (1, "ab42_l82_s967366_mpnn11", "ab42_l82_s967366_mpnn11_model2.pdb"),
    (2, "ab42_l89_s578974_mpnn11", "ab42_l89_s578974_mpnn11_model1.pdb"),
    (3, "ab42_l90_s311742_mpnn16", "ab42_l90_s311742_mpnn16_model1.pdb"),
    (4, "ab42_l71_s843399_mpnn18", "ab42_l71_s843399_mpnn18_model1.pdb"),
    (5, "ab42_l90_s311742_mpnn3",  "ab42_l90_s311742_mpnn3_model1.pdb"),
]

W, H = 2400, 1800
TRANSP = 0.88
AMBIENT = 0.32

for rank, did, fname in DESIGNS:
    cmd.reinitialize()
    cmd.set_color("bg_dark", [12/255.0, 14/255.0, 18/255.0])
    cmd.set_color("cflower", [0.39, 0.58, 0.93])   # soft periwinkle blue, matches reference
    cmd.bg_color("bg_dark")
    cmd.set("ray_opaque_background", 1)
    cmd.set("antialias", 2)
    cmd.set("ray_shadows", 1)
    cmd.set("specular", 0.2)
    cmd.set("ambient", AMBIENT)
    cmd.set("cartoon_fancy_helices", 1)
    cmd.set("surface_quality", 1)

    cmd.load(os.path.join(ACC, fname), "cplx")
    cmd.hide("everything")
    cmd.show("cartoon", "cplx")
    cmd.show("surface", "cplx")                     # follows atom color
    cmd.color("cflower", "cplx and chain B")        # binder
    cmd.color("orange",  "cplx and chain A")        # Abeta42 target
    cmd.set("transparency", TRANSP)

    cmd.orient("cplx")
    cmd.zoom("cplx", 3)
    cmd.ray(W, H)
    cmd.png(os.path.join(OUT, f"{rank:02d}_{did}.png"), dpi=300)
    print(f"RENDERED rank{rank} {did}")

print("ALL_RENDERS_DONE")
