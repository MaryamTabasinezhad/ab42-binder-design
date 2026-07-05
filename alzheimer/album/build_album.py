"""Assemble the top-5 binder docking album PDF from rendered PNGs + Stage-5 metrics.
Run in an env with matplotlib (colabfold):  python build_album.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import image as mpimg

BASE = "/global/project/hpcg6049/protein/alzheimer/album"
REN = os.path.join(BASE, "renders")
OUT = os.path.join(BASE, "Top5_Binder_Docking_Album.pdf")

BLUE = "#1f6fd6"
WHEAT = "#c8a45a"
ORANGE = "#e8820e"
DARK = "#222222"

# rank, id, scaffold, length, i_pTM, i_pAE, dG, SC, composite, iface_b, iface_t
DES = [
    (1, "ab42_l82_s967366_mpnn11", "s967366", 82, 0.79, 0.17, -71.8, 0.76, 0.793, 16, 17),
    (2, "ab42_l89_s578974_mpnn11", "s578974", 89, 0.80, 0.19, -70.8, 0.68, 0.733, 18, 23),
    (3, "ab42_l90_s311742_mpnn16", "s311742", 90, 0.86, 0.15, -88.8, 0.76, 0.713, 23, 22),
    (4, "ab42_l71_s843399_mpnn18", "s843399", 71, 0.80, 0.18, -76.6, 0.71, 0.708, 20, 16),
    (5, "ab42_l90_s311742_mpnn3",  "s311742", 90, 0.86, 0.15, -88.0, 0.76, 0.696, 21, 21),
]

with PdfPages(OUT) as pdf:
    # ---------------- COVER ----------------
    fig = plt.figure(figsize=(11, 8.5))
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.text(0.5, 0.86, "De Novo Binder Docking Album", ha="center",
            fontsize=30, fontweight="bold", color=DARK)
    ax.text(0.5, 0.795, "Top 5 designed miniprotein binders — Aβ42 (Alzheimer's) target",
            ha="center", fontsize=15, color="#555555")
    ax.text(0.5, 0.75, "BindCraft campaign  •  ranked by Stage-5 composite score  •  target 9CO4 (receptor-bound Aβ42 fibril)",
            ha="center", fontsize=10.5, color="#777777")

    blurb = (
        "Each design is an AlphaFold2-backpropagation binder docked onto the Aβ42 fibril target. "
        "Left panel: the helical binder (blue) nestled against the target molecular surface (wheat). "
        "Right panel: the binding interface — contacting side chains as sticks, with the designed "
        "hotspot cluster (Aβ42 residues 10–16) in orange. All 5 engage all 6 hotspots."
    )
    ax.text(0.5, 0.66, blurb, ha="center", va="top", fontsize=11, color=DARK, wrap=True,
            bbox=dict(boxstyle="round,pad=0.6", fc="#f4f7fb", ec="#d0d8e2"))
    ax.text(0.12, 0.635, "", fontsize=1)  # spacer

    # summary table
    cols = ["#", "Design (scaffold_mpnn)", "Len", "i-pTM", "i-pAE", "dG", "SC", "Score", "Iface res\n(bind/tgt)"]
    rows = []
    for (r, did, sc, ln, iptm, ipae, dg, shape, comp, ib, it) in DES:
        short = did.replace("ab42_", "")
        rows.append([str(r), short, str(ln), f"{iptm:.2f}", f"{ipae:.2f}",
                     f"{dg:.1f}", f"{shape:.2f}", f"{comp:.3f}", f"{ib}/{it}"])
    tb = ax.table(cellText=rows, colLabels=cols, cellLoc="center", loc="center",
                  bbox=[0.05, 0.10, 0.90, 0.42])
    tb.auto_set_font_size(False); tb.set_fontsize(10.5)
    # custom column widths (Design column much wider so names aren't clipped)
    relw = [0.35, 2.7, 0.55, 0.75, 0.75, 0.7, 0.55, 0.8, 1.0]
    fw = [w / sum(relw) for w in relw]
    for (rr, cc), cell in tb.get_celld().items():
        cell.set_width(fw[cc])
        cell.set_edgecolor("#cccccc")
        if cc == 1:
            cell.set_text_props(ha="left")
            cell.PAD = 0.03
        if rr == 0:
            cell.set_facecolor("#1f6fd6"); cell.set_text_props(color="white", fontweight="bold")
            if cc == 1:
                cell.set_text_props(color="white", fontweight="bold", ha="left")
        elif rr % 2 == 0:
            cell.set_facecolor("#f2f5f9")
    ax.text(0.5, 0.055, "Chain A = Aβ42 target (9CO4, C/E/G fibril chains)   •   Chain B = designed binder",
            ha="center", fontsize=9, color="#888888")
    ax.text(0.5, 0.03, "Prepared 2026-07-05  •  renders: PyMOL 3.1.0 (ray-traced)  •  ab42-binder-design",
            ha="center", fontsize=8.5, color="#aaaaaa")
    pdf.savefig(fig); plt.close(fig)

    # ---------------- ONE PAGE PER DESIGN ----------------
    for (r, did, sc, ln, iptm, ipae, dg, shape, comp, ib, it) in DES:
        fig = plt.figure(figsize=(11, 8.5))
        fig.patch.set_facecolor("white")

        # header
        hax = fig.add_axes([0, 0.90, 1, 0.10]); hax.axis("off")
        hax.text(0.04, 0.55, f"#{r}", fontsize=34, fontweight="bold", color=BLUE, va="center")
        hax.text(0.11, 0.68, did.replace("ab42_", ""), fontsize=20, fontweight="bold",
                 color=DARK, va="center")
        hax.text(0.11, 0.30,
                 f"scaffold {sc}  •  {ln} aa  •  i-pTM {iptm:.2f}  •  i-pAE {ipae:.2f}  "
                 f"•  ΔG {dg:.1f} kcal/mol  •  shape-comp {shape:.2f}  •  score {comp:.3f}",
                 fontsize=11, color="#555555", va="center")

        # images
        axL = fig.add_axes([0.02, 0.16, 0.47, 0.70]); axL.axis("off")
        axR = fig.add_axes([0.51, 0.16, 0.47, 0.70]); axR.axis("off")
        axL.imshow(mpimg.imread(os.path.join(REN, f"{r:02d}_{did}_overview.png")))
        axR.imshow(mpimg.imread(os.path.join(REN, f"{r:02d}_{did}_interface.png")))
        axL.set_title("Overview — binder on target surface", fontsize=12, color=DARK, pad=6)
        axR.set_title("Interface — contact side chains + hotspots", fontsize=12, color=DARK, pad=6)

        # caption
        cax = fig.add_axes([0, 0.02, 1, 0.12]); cax.axis("off")
        cap = (f"The binder buries {ib} residues against {it} Aβ42 residues at the interface, "
               f"engaging all 6 designed hotspots (Aβ42 10,11,13–16; orange). "
               f"Blue = binder (chain B), wheat = Aβ42 target (chain A). "
               f"Predicted binding confidence i-pTM {iptm:.2f} with interface PAE {ipae:.2f} Å and "
               f"Rosetta ΔG {dg:.1f} kcal/mol — a tight, well-packed lateral docking.")
        cax.text(0.5, 0.5, cap, ha="center", va="center", fontsize=10.5, color=DARK, wrap=True,
                 bbox=dict(boxstyle="round,pad=0.5", fc="#f4f7fb", ec="#d0d8e2"))
        pdf.savefig(fig); plt.close(fig)

print("ALBUM_WRITTEN", OUT)
