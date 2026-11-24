#!/usr/bin/env python3
"""
The Held engine — a Belnap-Dunn four-valued valuation toy for the "Held" piece.

The piece poses one question to a sealed vessel: "am I here?"
Two sensor channels report evidence about it. The engine fuses their reports
in the four-valued Belnap-Dunn lattice (the formal home of the tetralemma:
{Belnap 1977, Dunn 1976}) and renders all four corners simultaneously:

    {T}    yes     -> light
    {F}    no      -> withdrawal
    {T,F}  both    -> interference (the two eating each other)
    {}     neither -> the frame turns around: the piece displays the
                     conditions of its own asking (holders, sensor liveness)
                     instead of going dark.

The honest point of the toy: in Belnap-Dunn, "neither" is a FIRST-CLASS
valuation — "told neither true nor false" — not an absence. A renderer that
reads the information state is formally licensed to turn the frame around.
The caveat is in the README: the table is the "this" of the tetralemma,
not the ladder Nagarjuna kicked away.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------- values

NEITHER = frozenset()            # {}  - told neither true nor false
T       = frozenset({True})      # {T} - told true only
F       = frozenset({False})     # {F} - told false only
BOTH    = frozenset({True, False})  # {T,F} - told both

NAMES = {NEITHER: "neither", T: "yes", F: "no", BOTH: "both"}
GLYPH = {NEITHER: "{}", T: "{T}", F: "{F}", BOTH: "{T,F}"}
COLOR = {NEITHER: "#9e9e9e", T: "#ffd54f", F: "#4a6fa5", BOTH: "#e06c75"}

def join(a, b):
    """Evidence combination: union. Two sensors' reports fused."""
    return a | b

def meet(a, b):
    """Common ground: intersection."""
    return a & b

def neg(a):
    """Belnap negation: swap T and F."""
    return frozenset({not x for x in a})

# ---------------------------------------------------------------- scenario

TICKS = 120
SENSOR_STATES = ["silent", "true", "false"]  # what one sensor may report per tick

def scenario():
    """Four phases of a performance: held / disputed / released / withdrawn."""
    s1 = np.full(TICKS, "silent", dtype=object)
    s2 = np.full(TICKS, "silent", dtype=object)
    # 0-29: all tethers held, sensors agree the vessel is here
    s1[0:30] = "true";  s2[0:30] = "true"
    # 30-59: two tethers released, sensors disagree
    s1[30:60] = "true"; s2[30:60] = "false"
    # 60-89: all released, sensors silent -> NEITHER
    # (already silent)
    # 90-119: held again, sensors report absence -> NO
    s1[90:120] = "false"; s2[90:120] = "false"
    return s1, s2

def sensor_value(reading):
    return {"true": T, "false": F, "silent": NEITHER}[reading]

def valuation_series():
    s1, s2 = scenario()
    vals = np.array([join(sensor_value(a), sensor_value(b))
                     for a, b in zip(s1, s2)], dtype=object)
    return s1, s2, vals

# ---------------------------------------------------------------- rendering

def render_channels(vals):
    """
    Four simultaneous render channels, one per corner.

    yes:        light intensity
    no:         withdrawal depth (darkness with intent)
    both:       interference — yes and no beating against each other
    neither:    the frame turns — meta-display of the asking conditions.
                In this toy: 1.0 whenever the engine has no information,
                annotated with what the frame shows instead
                (holders: 0/4, sensors live: 2/2).
    """
    n = len(vals)
    light = np.zeros(n)
    withdraw = np.zeros(n)
    interfere = np.zeros(n)
    frameturn = np.zeros(n)
    t = np.arange(n)
    for i, v in enumerate(vals):
        if v == T:
            light[i] = 1.0
        elif v == F:
            withdraw[i] = 1.0
        elif v == BOTH:
            # interference: the two channels eating each other
            light[i] = 0.5 + 0.5 * np.sin(2 * np.pi * i / 8)
            withdraw[i] = 0.5 - 0.5 * np.sin(2 * np.pi * i / 8)
            interfere[i] = 1.0
        else:  # NEITHER
            # not darkness: the frame turns around
            frameturn[i] = 1.0
    return light, withdraw, interfere, frameturn

def plot_channels(path):
    s1, s2, vals = valuation_series()
    light, withdraw, interfere, frameturn = render_channels(vals)
    t = np.arange(TICKS)

    fig, axes = plt.subplots(6, 1, figsize=(12, 10), sharex=True,
                             gridspec_kw={"height_ratios": [1, 1, 1, 1, 1, 1.2]})
    fig.suptitle('Held — the vessel asks "am I here?"\n'
                 'four corners rendered simultaneously (Belnap–Dunn valuation engine)',
                 fontsize=13, y=0.98)

    # top strip: the fused valuation itself
    ax = axes[0]
    for v in (T, F, BOTH, NEITHER):
        mask = np.array([x == v for x in vals])
        ax.fill_between(t, 0, 1, where=mask, color=COLOR[v], alpha=0.85,
                        step="mid", label=f"{NAMES[v]} {GLYPH[v]}")
    ax.set_ylim(0, 1); ax.set_yticks([])
    ax.set_ylabel("fused\nvaluation", rotation=0, ha="right", va="center", fontsize=9)
    ax.legend(loc="upper right", fontsize=8, ncol=4)

    strips = [
        (axes[1], light, COLOR[T], "yes → light"),
        (axes[2], withdraw, COLOR[F], "no → withdrawal"),
        (axes[3], interfere, COLOR[BOTH], "both → interference"),
        (axes[4], frameturn, COLOR[NEITHER], "neither → the frame turns"),
    ]
    for ax, ch, c, label in strips:
        ax.fill_between(t, 0, ch, color=c, alpha=0.8, step="mid")
        ax.set_ylim(0, 1.1); ax.set_yticks([])
        ax.set_ylabel(label, rotation=0, ha="right", va="center", fontsize=9)

    # bottom: what the frame shows during "neither"
    ax = axes[5]
    ax.axis("off")
    ax.text(0.01, 0.85, 'neither {}  →  the piece shows its own asking conditions:',
            fontsize=10, va="top")
    ax.text(0.01, 0.55, 'holders: 0/4  ·  sensors live: 2/2  ·  last disagreement: tick 59  ·\n'
                        '"no one is holding — the question is unasked, not unanswered."',
            fontsize=9, va="top", family="monospace",
            bbox=dict(boxstyle="round,pad=0.4", fc="#f5f5f5", ec="#9e9e9e"))
    for x in (30, 60, 90):
        for a in axes[:5]:
            a.axvline(x, color="black", lw=0.8, ls="--", alpha=0.5)
    for a, lab in zip(axes[:5], [""] * 5):
        pass
    axes[0].text(15, 1.25, "held — agree", ha="center", fontsize=8)
    axes[0].text(45, 1.25, "disputed", ha="center", fontsize=8)
    axes[0].text(75, 1.25, "released", ha="center", fontsize=8)
    axes[0].text(105, 1.25, "held — absent", ha="center", fontsize=8)
    axes[5].set_xlabel("tick")

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(path, dpi=120)
    print("wrote", path)

def fusion_table():
    """3x3 fusion table: two sensors x {true, false, silent}."""
    rows = ["true", "false", "silent"]
    table = {}
    for a in rows:
        for b in rows:
            table[(a, b)] = join(sensor_value(a), sensor_value(b))
    return table

def plot_lattice(path):
    table = fusion_table()
    rows = ["true", "false", "silent"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Belnap–Dunn: fusion table and the information order", fontsize=13)

    # left: fusion table
    ax1.axis("off")
    ax1.set_title("join (union) of two sensor reports", fontsize=11)
    cell = 0.26
    for i, a in enumerate(rows):
        for j, b in enumerate(rows):
            v = table[(a, b)]
            x, y = 0.22 + j * cell, 0.60 - i * cell
            box = FancyBboxPatch((x, y), cell * 0.92, cell * 0.8,
                                 boxstyle="round,pad=0.02",
                                 fc=COLOR[v], ec="black", alpha=0.85)
            ax1.add_patch(box)
            ax1.text(x + cell * 0.46, y + cell * 0.40, f"{GLYPH[v]}\n{NAMES[v]}",
                     ha="center", va="center", fontsize=9)
        ax1.text(0.16, 0.60 - i * cell + cell * 0.40, f"S1={a}", fontsize=9,
                 va="center", ha="right")
    for j, b in enumerate(rows):
        ax1.text(0.22 + j * cell + cell * 0.46, 0.90, f"S2={b}", fontsize=9,
                 ha="center")

    # right: information-order Hasse diagram (neither at bottom)
    ax2.axis("off")
    ax2.set_title("information order: more evidence rises", fontsize=11)
    pos = {NEITHER: (0.5, 0.12), T: (0.28, 0.5), F: (0.72, 0.5), BOTH: (0.5, 0.88)}
    for a, b in [(NEITHER, T), (NEITHER, F), (T, BOTH), (F, BOTH)]:
        ax2.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], "k-", lw=1.5)
    for v, (x, y) in pos.items():
        circ = plt.Circle((x, y), 0.09, fc=COLOR[v], ec="black", zorder=3)
        ax2.add_patch(circ)
        ax2.text(x, y, f"{GLYPH[v]}\n{NAMES[v]}", ha="center", va="center",
                 fontsize=9, zorder=4)
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
    ax2.text(0.5, 0.02, "join = union: sensor reports accumulate, never cancel",
             ha="center", fontsize=9, style="italic")

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(path, dpi=120)
    print("wrote", path)

def self_check():
    """Verify the lattice algebra the toy depends on."""
    assert join(T, F) == BOTH
    assert join(T, NEITHER) == T
    assert join(NEITHER, NEITHER) == NEITHER
    assert meet(T, F) == NEITHER
    assert meet(BOTH, T) == T
    assert neg(T) == F and neg(F) == T and neg(BOTH) == BOTH and neg(NEITHER) == NEITHER
    # disagreement never cancels to nothing; silence never overwrites evidence
    s1, s2, vals = valuation_series()
    assert vals[45] == BOTH      # disputed phase
    assert vals[75] == NEITHER   # released phase
    assert vals[15] == T         # held, agree
    assert vals[105] == F        # held, absent
    print("self-check: lattice algebra + scenario phases OK")

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    self_check()
    plot_channels(os.path.join(here, "channels.png"))
    plot_lattice(os.path.join(here, "lattice.png"))
