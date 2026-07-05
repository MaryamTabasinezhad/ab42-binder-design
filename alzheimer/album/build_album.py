"""Assemble the top-5 binder docking album PDF — DARK theme matching the
ternary_fusions house style. One whole-complex render per design page.
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

BG = (12/255, 14/255, 18/255)          # exact render background
PANEL = (0.10, 0.11, 0.13)             # slightly lifted panel
CFLOWER = "#6494ec"                      # binder blue
ORANGE = "#f0820e"                       # target orange
FG = "#e8ecf2"                           # light text
MUTE = "#9aa3b0"

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
    fig = plt.figure(figsize=(11, 8.5)); fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_facecolor(BG)
    ax.text(0.5, 0.87, "De Novo Binder Docking Album", ha="center",
            fontsize=30, fontweight="bold", color=FG)
    ax.text(0.5, 0.805, "Top 5 designed miniprotein binders — Aβ42 (Alzheimer's) target",
            ha="center", fontsize=15, color="#c3cad6")
    ax.text(0.5, 0.762, "BindCraft campaign  •  ranked by Stage-5 composite score  •  target 9CO4 (receptor-bound Aβ42 fibril)",
            ha="center", fontsize=10.5, color=MUTE)

    ax.text(0.30, 0.70, "■", color=CFLOWER, fontsize=15, ha="center", va="center")
    ax.text(0.325, 0.70, "designed binder", color=FG, fontsize=11, ha="left", va="center")
    ax.text(0.58, 0.70, "■", color=ORANGE, fontsize=15, ha="center", va="center")
    ax.text(0.605, 0.70, "Aβ42 fibril target (9CO4)", color=FG, fontsize=11, ha="left", va="center")

    blurb = ("Each panel is an AlphaFold2-backpropagation binder docked onto the Aβ42 fibril target — "
             "cartoon with a translucent molecular-surface glow, rendered in the campaign house style. "
             "All five bind laterally across the fibril, engaging the designed hotspot cluster (Aβ42 10–16).")
    ax.text(0.5, 0.635, blurb, ha="center", va="top", fontsize=11, color="#d5dbe4", wrap=True,
            bbox=dict(boxstyle="round,pad=0.6", fc=PANEL, ec="#2b303a"))

    cols = ["#", "Design (scaffold_mpnn)", "Len", "i-pTM", "i-pAE", "dG", "SC", "Score", "Iface res\n(bind/tgt)"]
    rows = [[str(r), did.replace("ab42_", ""), str(ln), f"{iptm:.2f}", f"{ipae:.2f}",
             f"{dg:.1f}", f"{shape:.2f}", f"{comp:.3f}", f"{ib}/{it}"]
            for (r, did, sc, ln, iptm, ipae, dg, shape, comp, ib, it) in DES]
    tb = ax.table(cellText=rows, colLabels=cols, cellLoc="center", loc="center",
                  bbox=[0.05, 0.10, 0.90, 0.42])
    tb.auto_set_font_size(False); tb.set_fontsize(10.5)
    relw = [0.35, 2.7, 0.55, 0.75, 0.75, 0.7, 0.55, 0.8, 1.0]
    fw = [w / sum(relw) for w in relw]
    for (rr, cc), cell in tb.get_celld().items():
        cell.set_width(fw[cc]); cell.set_edgecolor("#2b303a")
        cell.set_text_props(color=FG)
        if cc == 1:
            cell.set_text_props(ha="left", color=FG); cell.PAD = 0.03
        if rr == 0:
            cell.set_facecolor("#20364f")
            cell.set_text_props(color="white", fontweight="bold", ha=("left" if cc == 1 else "center"))
        else:
            cell.set_facecolor(PANEL if rr % 2 else "#0e1116")
    ax.text(0.5, 0.055, "Chain A = Aβ42 target (9CO4, C/E/G fibril chains)   •   Chain B = designed binder",
            ha="center", fontsize=9, color=MUTE)
    ax.text(0.5, 0.03, "Prepared 2026-07-05  •  ab42-binder-design campaign",
            ha="center", fontsize=8.5, color="#5f6773")
    pdf.savefig(fig, facecolor=BG); plt.close(fig)

    # ---------------- ONE PAGE PER DESIGN ----------------
    for (r, did, sc, ln, iptm, ipae, dg, shape, comp, ib, it) in DES:
        fig = plt.figure(figsize=(11, 8.5)); fig.patch.set_facecolor(BG)

        hax = fig.add_axes([0, 0.90, 1, 0.10]); hax.axis("off"); hax.set_facecolor(BG)
        hax.text(0.04, 0.55, f"#{r}", fontsize=34, fontweight="bold", color=CFLOWER, va="center")
        hax.text(0.11, 0.66, did.replace("ab42_", ""), fontsize=20, fontweight="bold", color=FG, va="center")
        hax.text(0.11, 0.28,
                 f"scaffold {sc}  •  {ln} aa  •  i-pTM {iptm:.2f}  •  i-pAE {ipae:.2f}  "
                 f"•  ΔG {dg:.1f} kcal/mol  •  shape-comp {shape:.2f}  •  score {comp:.3f}",
                 fontsize=11, color=MUTE, va="center")

        iax = fig.add_axes([0.06, 0.15, 0.88, 0.72]); iax.axis("off"); iax.set_facecolor(BG)
        iax.imshow(mpimg.imread(os.path.join(REN, f"{r:02d}_{did}.png")))

        cax = fig.add_axes([0, 0.02, 1, 0.11]); cax.axis("off"); cax.set_facecolor(BG)
        cap = (f"Binder (blue) docked laterally across the Aβ42 fibril (orange), burying {ib} binder residues "
               f"against {it} target residues and engaging all 6 designed hotspots (Aβ42 10,11,13–16). "
               f"i-pTM {iptm:.2f}, interface PAE {ipae:.2f} Å, Rosetta ΔG {dg:.1f} kcal/mol.")
        cax.text(0.5, 0.5, cap, ha="center", va="center", fontsize=10.5, color="#d5dbe4", wrap=True,
                 bbox=dict(boxstyle="round,pad=0.5", fc=PANEL, ec="#2b303a"))
        pdf.savefig(fig, facecolor=BG); plt.close(fig)

print("ALBUM_WRITTEN", OUT)
