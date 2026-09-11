"""Render 3 architecture variants (shared / method1 / method2) at identical
dimensions so the trunk stays perfectly in place when the site swaps images.

Adapted from make_audio_pathway_figure.py."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# palette
TRUNK_FC, TRUNK_EC = "#eef0f3", "#3f434c"
DINO_FC, DINO_EC = "#dbe7f6", "#2f6bb0"
TOK_IMG, TOK_WRIST, TOK_PROP, TOK_ACT = "#9fc0e4", "#cadcef", "#dcdfe4", "#f2d9a9"
AUD_FC, AUD_EC = "#fce2ca", "#E0812A"          # method 1 = orange
HIST_FC, HIST_EC = "#dbe7f6", "#2f6bb0"        # method 2 = blue
PINK_FC, PINK_EC = "#f6dbe6", "#b03470"        # shared audio pipeline = pink
LOSS_C = "#b0282d"
TXT = "#15171a"

FS, FSS = 8.2, 6.9
DASH = (0, (3, 2))

X_IN, W_IN = 1.0, 16.0
X_ENC, W_ENC = 20.5, 15.0
X_PLUS = 43.5
X_TOK, W_TOK = 47.5, 12.0
X_TR, W_TR = 65.0, 15.0
X_OUT, W_OUT = 84.0, 15.0

Y_PRO, H_PRO = 86.0, 10.0
Y_OVH, H_OVH = 68.0, 12.0
Y_WR, H_WR = 52.0, 12.0
Y_ACT, H_ACT = 36.0, 11.0
TOK_TOP, TOK_BOT = 96.0, 38.0
Y_AUD, H_AUD = 3.0, 15.0


def box(ax, x, y, w, h, label, fc=TRUNK_FC, ec=TRUNK_EC, fs=FS, lw=1.1, ls="-",
        tc=TXT, r=1.6):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls, zorder=2,
        mutation_aspect=0.42))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, color=tc, zorder=3, linespacing=1.4)


def arrow(ax, p0, p1, color=TRUNK_EC, lw=1.15, ls="-", rad=0.0, z=4, halo=False):
    p = FancyArrowPatch(
        p0, p1, arrowstyle="-|>", mutation_scale=8.5, linewidth=lw, linestyle=ls,
        color=color, connectionstyle=f"arc3,rad={rad}", zorder=z,
        shrinkA=1.5, shrinkB=1.5)
    if halo:
        p.set_path_effects([pe.withStroke(linewidth=lw + 3.0, foreground="white")])
    ax.add_patch(p)


def note(ax, x, y, s, color=TXT, fs=FSS, ha="center", va="center", style="italic"):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color, style=style,
            zorder=6, linespacing=1.35)


def draw_trunk(ax):
    box(ax, X_IN, Y_PRO, W_IN, H_PRO, "Proprio  $q_t$")
    box(ax, X_IN, Y_OVH, W_IN, H_OVH, "Overhead RGB\n$720\\times1280$")
    box(ax, X_IN, Y_WR, W_IN, H_WR, "Wrist RGB $\\times$2\n$480\\times640$")
    box(ax, X_IN, Y_ACT, W_IN, H_ACT, "Action queries\n$\\times$50 (learned)",
        fc="#fbf1dd", ec="#a8802e")

    box(ax, X_ENC, Y_PRO, W_ENC, H_PRO, "Linear")
    box(ax, X_ENC, Y_WR, W_ENC, (Y_OVH + H_OVH) - Y_WR,
        "DINOv2 ViT-S/14\nfrozen", fc=DINO_FC, ec=DINO_EC)

    for y, h in ((Y_PRO, H_PRO), (Y_OVH, H_OVH), (Y_WR, H_WR)):
        arrow(ax, (X_IN + W_IN, y + h / 2), (X_ENC, y + h / 2))

    segs = [("proprio  1", TOK_PROP, 8.0),
            ("overhead patches\n700", TOK_IMG, 22.0),
            ("wrist patches\n2 $\\times$ 140", TOK_WRIST, 14.0),
            ("action queries\n50", TOK_ACT, 14.0)]
    y, anchors = TOK_TOP, {}
    for lbl, fc, h in segs:
        y -= h
        box(ax, X_TOK, y, W_TOK, h, lbl, fc=fc, ec="#5b626d", fs=FSS, lw=0.9, r=1.0)
        anchors[lbl.split("\n")[0]] = y + h / 2
    note(ax, X_TOK + W_TOK / 2, TOK_TOP + 4.5, "token sequence\n1031 per frame")

    arrow(ax, (X_ENC + W_ENC, Y_PRO + H_PRO / 2), (X_TOK, anchors["proprio  1"]))
    arrow(ax, (X_ENC + W_ENC, Y_WR + H_WR / 2), (X_TOK, anchors["wrist patches"]))
    arrow(ax, (X_IN + W_IN, Y_ACT + H_ACT / 2), (X_TOK, anchors["action queries"]))

    box(ax, X_TR, TOK_BOT - 2.0, W_TR, TOK_TOP - TOK_BOT + 2.0,
        "Transformer\n$\\times$3 blocks\n\nself-attention,\nsame-frame only")
    arrow(ax, (X_TOK + W_TOK, (TOK_BOT + TOK_TOP) / 2), (X_TR, (TOK_BOT + TOK_TOP) / 2))

    box(ax, X_OUT, 78.0, W_OUT, 10.0, "action head")
    box(ax, X_OUT, 62.0, W_OUT, 11.0, "action chunk\n$50\\times D$")
    xc = X_OUT + W_OUT / 2
    arrow(ax, (X_TR + W_TR, 83.0), (X_OUT, 83.0))
    arrow(ax, (xc, 78.0), (xc, 73.0))
    arrow(ax, (xc, 62.0), (xc, 57.5), color=LOSS_C, ls=":")
    ax.text(xc, 54.0, "$\\mathcal{L}_{\\mathrm{BC}}$", ha="center", va="center",
            fontsize=9.5, color=LOSS_C, zorder=6)
    return anchors["overhead patches"]


def draw_shared_audio(ax):
    """Common pink audio pipeline: A(x,y,t) -> Resize -> Patch Pool."""
    ymid = Y_AUD + H_AUD / 2
    box(ax, X_IN, Y_AUD, W_IN, H_AUD,
        "$A(x,y,t)$\n$50\\times 90$", fc=PINK_FC, ec=PINK_EC, fs=FSS)
    box(ax, X_ENC, Y_AUD, W_ENC, H_AUD, "Resize +\nPatch Pool\n$20\\times 35$",
        fc=PINK_FC, ec=PINK_EC, fs=FSS)
    arrow(ax, (X_IN + W_IN, ymid), (X_ENC, ymid), color=PINK_EC)


def draw_shared_ovh_edge(ax, ov_mid):
    """Direct DINO -> overhead-patches edge (no + node)."""
    arrow(ax, (X_ENC + W_ENC, Y_OVH + H_OVH / 2), (X_TOK, ov_mid))


def draw_method1(ax):
    """Orange: attention loss branch."""
    ymid = Y_AUD + H_AUD / 2
    box(ax, 37.5, Y_AUD, 13.0, H_AUD,
        "Target Attn.\n$p_{b,t}$  $20\\times 35$",
        fc=AUD_FC, ec=AUD_EC, fs=FSS)
    arrow(ax, (X_ENC + W_ENC, ymid), (37.5, ymid), color=AUD_EC)
    note(ax, 44.0, Y_AUD - 3.0,
         "Method 1  ·  Visuo-Acoustic Attention", color=AUD_EC, fs=7.6, style="normal")

    # attention read from final transformer block
    box(ax, 64.0, 18.5, 17.0, 13.0,
        "attention  $q^{\\theta}_{b,t}$\naction $\\rightarrow$ image\nfinal block",
        fc="#ffffff", ec=AUD_EC, ls=DASH, fs=FSS)
    arrow(ax, (X_TR + W_TR / 2, TOK_BOT - 2.0), (X_TR + W_TR / 2, 31.5),
          color=AUD_EC, ls=DASH)
    box(ax, 83.0, 7.0, 16.0, 13.0,
        "$D_{\\mathrm{KL}}(p_{b,t}\\,\\Vert\\,q^{\\theta}_{b,t})$",
        fc="#ffffff", ec=AUD_EC, ls=DASH, fs=8.4)
    arrow(ax, (81.0, 23.0), (83.0, 17.5), color=AUD_EC, ls=DASH)
    arrow(ax, (50.5, ymid), (83.0, 12.0), color=AUD_EC, rad=-0.07)
    ax.text(91.0, 3.0, "$\\lambda\\,\\mathcal{L}_{\\mathrm{attn}}$", ha="center",
            va="center", fontsize=9.5, color=AUD_EC, zorder=6)


def draw_method2(ax, ov_mid):
    """Blue: history-as-input branch."""
    ymid = Y_AUD + H_AUD / 2
    box(ax, 37.5, Y_AUD, 13.0, H_AUD,
        "per-patch MLP\n$1{\\rightarrow}384{\\rightarrow}384$",
        fc=HIST_FC, ec=HIST_EC, fs=FSS)
    arrow(ax, (X_ENC + W_ENC, ymid), (37.5, ymid), color=HIST_EC)
    note(ax, 44.0, Y_AUD - 3.0,
         "Method 2  ·  Visuo-Acoustic History", color=HIST_EC, fs=7.6, style="normal")

    # DINO -> + -> overhead tokens
    arrow(ax, (X_ENC + W_ENC, Y_OVH + H_OVH / 2), (X_PLUS - 2.3, ov_mid))
    arrow(ax, (X_PLUS + 2.3, ov_mid), (X_TOK, ov_mid))
    arrow(ax, (44.0, Y_AUD + H_AUD), (X_PLUS, ov_mid - 2.6),
          color=HIST_EC, halo=True, z=5)
    ax.plot([X_PLUS], [ov_mid], marker="o", markersize=11, markerfacecolor="white",
            markeredgecolor=HIST_EC, markeredgewidth=1.4, zorder=7, clip_on=False)
    ax.text(X_PLUS, ov_mid, "+", ha="center", va="center", fontsize=10,
            color=HIST_EC, zorder=8)
    note(ax, X_PLUS + 1.5, ov_mid + 7.0, "elementwise\naddition",
         color=HIST_EC, style="normal")


def make(kind, out_path):
    fig, ax = plt.subplots(figsize=(10.2, 4.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(-6, 110)
    ax.axis("off")

    ov_mid = draw_trunk(ax)
    draw_shared_audio(ax)

    if kind == "shared":
        draw_shared_ovh_edge(ax, ov_mid)
    elif kind == "method1":
        draw_shared_ovh_edge(ax, ov_mid)
        draw_method1(ax)
    elif kind == "method2":
        draw_method2(ax, ov_mid)
    else:
        raise ValueError(kind)

    fig.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.005)
    fig.savefig(out_path, dpi=220, bbox_inches=None, facecolor="white")
    plt.close(fig)
    print(f"wrote {out_path}  ({os.path.getsize(out_path)/1024:.0f} KB)")


def main():
    out_dir = "/Users/daehwakim/Desktop/research/Robo-Synesthesia/website/static/images/arch"
    os.makedirs(out_dir, exist_ok=True)
    for kind in ("shared", "method1", "method2"):
        make(kind, os.path.join(out_dir, f"{kind}.png"))


if __name__ == "__main__":
    main()
