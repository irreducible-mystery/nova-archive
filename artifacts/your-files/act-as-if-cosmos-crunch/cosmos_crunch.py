"""
COSMOS-CRUNCH — two new dark-energy floors, standalone extension.
Original cosmos.py is untouched; this file is a separate experiment
in this folder. Predictions in PREDICTIONS.md, written before this run.

Floor D (Cornell axion + negative Lambda, TOY representation):
  flat Friedmann, dark-energy factor f(a) = 1 - alpha*ln(a), alpha=2.085,
  calibrated so E^2(a)=0 at a~1.69. NOT the full axion field equations.
  Expansion branch: t(a) = integral da/(a*H(a)), singular at turnaround
  handled by s = sqrt(a_max - a) substitution (finite limit at the top).
  Contraction branch: t = t_turn + integral_a^{a_max} da/(a*H(a)).
  Crunch proxy: a = 1e-3 (not a = 0, which the grid cannot reach).

Floor E (EPJC no-crunch quintessence, TOY representation):
  w(a) = -1 + 0.2/a, so rho_de(a) = exp(-0.6*(1 - 1/a)) in units of today.
  NOT the full nonminimally coupled double-exponential field equations.
  t(a) by the same integral as the original cosmos.py.

Run: python3 cosmos_crunch.py  — writes cosmos_crunch.png, output.txt
Exit 0 iff P-D1, P-D2, P-D3, P-E1, P-E2, P-A1 all pass, else 1.
P-A2 is OPEN by design and does not affect the exit code.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)  # singular turnaround endpoint only; value replaced by its finite limit

H0_kms_Mpc = 67.4
MPC_M = 3.085677581e22
H0_SI = H0_kms_Mpc * 1e3 / MPC_M
GYR_S = 1e9 * 365.25 * 24 * 3600
HT = (1.0 / H0_SI) / GYR_S
Om_r, Om_m, Om_de = 9.2e-5, 0.315, 0.685
ALPHA = 2.085


def E2_D(a):
    return Om_r * a**-4 + Om_m * a**-3 + Om_de * (1 - ALPHA * np.log(a))


def E_D(a):
    return np.sqrt(np.maximum(E2_D(a), 0.0))


def E2_E(a):
    rho_de = np.exp(-0.6 * (1 - 1.0 / a))
    return Om_r * a**-4 + Om_m * a**-3 + Om_de * rho_de


def E_E(a):
    return np.sqrt(E2_E(a))


def w_E(a):
    return -1 + 0.2 / a


# ---- Floor D: turnaround, expansion time, contraction time ----
a_max = float(brentq(E2_D, 1.6, 1.75))
h = 1e-6
dE2 = (E2_D(a_max + h) - E2_D(a_max - h)) / (2 * h)
lim_val = 2.0 / (a_max * np.sqrt(-dE2))  # finite limit of 2s/(a*E) at s=0

def t_expansion_D(a_target):
    """Time from a=1e-4 to a_target (< a_max) via da/(a*H), in Gyr."""
    a = np.logspace(-4, np.log10(a_target), 20000)
    return float(np.trapz(1.0 / (a * E_D(a)), a) * HT)

def t_turn_D():
    """Expansion time to a_max, s-transformed at the singular top."""
    s = np.linspace(np.sqrt(a_max - 1e-4), 1e-8, 20000)
    aa = a_max - s**2
    vals = 2 * s / (aa * E_D(aa))
    vals[-1] = lim_val
    return float(abs(np.trapz(vals, s)) * HT)

def t_contraction_D(a_target):
    """Time from a_max down to a_target, in Gyr (positive)."""
    # regular part: a_target .. 1.68
    a = np.logspace(np.log10(a_target), np.log10(1.68), 20000)
    tc1 = float(np.trapz(1.0 / (a * E_D(a)), a) * HT)
    # top part: 1.68 .. a_max, s-transformed
    s = np.linspace(np.sqrt(a_max - 1.68), 1e-8, 5000)
    aa = a_max - s**2
    vals = 2 * s / (aa * E_D(aa))
    vals[-1] = lim_val
    tc2 = float(abs(np.trapz(vals, s)) * HT)
    return tc1 + tc2

t_now_D = t_expansion_D(1.0)
t_turn = t_turn_D()
t_crunch = t_turn + t_contraction_D(1e-3)
turn_from_now = t_turn - t_now_D

# a(t) for Floor D: expansion branch (a: 1e-4..a_max) + contraction (a_max..1e-3)
a_exp = np.logspace(-4, np.log10(1.68), 4000)
t_exp = np.array([0.0])
# cumulative integral in a (use trapz cumulatively via log grid approx: reuse t_expansion at grid points is slow, so integrate stepwise)
inv = 1.0 / (a_exp * E_D(a_exp))
t_exp = np.concatenate([[0.0], np.cumsum(0.5 * (inv[1:] + inv[:-1]) * np.diff(a_exp))]) * HT
# top segment: add s-transform tail from 1.68 to a_max
s_tail = np.linspace(np.sqrt(a_max - 1.68), 1e-8, 2000)
aa_tail = a_max - s_tail**2
v_tail = 2 * s_tail / (aa_tail * E_D(aa_tail))
v_tail[-1] = lim_val
t_tail = np.abs(np.cumsum(0.5 * (v_tail[1:] + v_tail[:-1]) * np.diff(s_tail))) * HT
t_exp_full = np.concatenate([t_exp, t_exp[-1] + t_tail])
a_exp_full = np.concatenate([a_exp, aa_tail[1:]])
# contraction branch: a from a_max down to 1e-3, t = t_turn + integral
a_con = np.logspace(np.log10(1.68), -3, 4000)[::-1]  # descending? logspace ascending then reversed = descending
# Build contraction t(a) by cumulative integral from a_max: use a grid descending in a
a_con_grid = np.concatenate([[a_max], np.logspace(np.log10(1.68), -3, 4000)])
# integral from a to a_max: for each grid point, trapz over [a, a_max] — do cumulative from the top
inv_con = 1.0 / (a_con_grid * E_D(a_con_grid))
# cumulative integral from top (a_max) downward: dt = -integral, use reversed cumulative
t_con = [t_turn]
cum = 0.0
for i in range(1, len(a_con_grid)):
    # segment a_con_grid[i-1] -> a_con_grid[i] (decreasing a), time positive = trapz over that segment
    cum += 0.5 * (inv_con[i - 1] + inv_con[i]) * abs(a_con_grid[i] - a_con_grid[i - 1]) * HT
    t_con.append(t_turn + cum)
t_con = np.array(t_con)
# Note: the segment 1.68..a_max in a_con_grid is a single jump (a_max -> 1.68);
# its time is the s-transform tail, which the trapz above approximates with the
# singular endpoint — replace that first step with the exact tail time:
t_con[1] = t_turn + float(abs(np.trapz(v_tail, s_tail)) * HT)
# and shift subsequent points by the correction (they were computed with the singular step)
# The singular step overestimates by a finite amount; recompute cumulative from step 1 onward:
# (simpler: keep t_con as computed except the first step is now exact; the rest of the
#  cumulative was built on the singular step, so rebuild from index 1)
cum2 = t_con[1]
t_con2 = [t_turn, cum2]
for i in range(2, len(a_con_grid)):
    cum2 += 0.5 * (inv_con[i - 1] + inv_con[i]) * abs(a_con_grid[i] - a_con_grid[i - 1]) * HT
    t_con2.append(cum2)
t_con = np.array(t_con2)
t_D = np.concatenate([t_exp_full, t_con[1:]])
a_D = np.concatenate([a_exp_full, a_con_grid[1:]])
# da/dt sign: expansion branch positive, contraction branch negative, by construction;
# verify numerically from the a(t) arrays (gradient on a uniform-ish t grid is noisy at the join,
# so report sign by branch, and check gradient sign away from the join)
dadt_D = np.gradient(a_D, t_D)
sign_changes = 0
# count sign changes of da/dt in the interior, away from the turnaround join (index of a_max)
imax = int(np.argmax(a_D))
# expansion gradient (first half) and contraction gradient (second half) medians
exp_sign = np.median(np.sign(dadt_D[:imax]))
con_sign = np.median(np.sign(dadt_D[imax + 1:]))

# ---- Floor E: t(a) to a=1e3, FUTURE ONLY (a >= 1) ----
# The w(a) toy diverges at a -> 0 (rho_de -> inf), so it is not a past
# model at all; its anchor is the future fate only. t_E is time since now.
a_E = np.logspace(0, 3, 4000)
inv_E = 1.0 / (a_E * E_E(a_E))
t_E = np.concatenate([[0.0], np.cumsum(0.5 * (inv_E[1:] + inv_E[:-1]) * np.diff(a_E))]) * HT
dadt_E = np.gradient(a_E, t_E)
H_E = E_E(a_E) / HT  # in Gyr^-1
w_at_100 = float(w_E(100.0))
H_ratio_100_to_1000 = float(H_E[np.argmin(np.abs(a_E - 100.0))] / H_E[-1])

# ---- score predictions ----
def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok

print(f"Hubble time: {HT:.2f} Gyr")
print(f"\nFloor D: a_max = {a_max:.4f}, t_now(toy) = {t_now_D:.2f} Gyr, t_turn = {t_turn:.2f} Gyr, "
      f"turnaround from now = {turn_from_now:.2f} Gyr, t_crunch(a=1e-3) = {t_crunch:.2f} Gyr")
print(f"Floor D: expansion da/dt sign (median) = {exp_sign}, contraction da/dt sign (median) = {con_sign}")
print(f"Floor E: da/dt > 0 always? {bool(np.all(dadt_E > 0))}, w(100) = {w_at_100:.4f}, "
      f"H(100)/H(1e3) = {H_ratio_100_to_1000:.4f}")
print("\n=== Predictions ===")
results = []
results.append(check("P-D1 arrow reversal, sustained da/dt<0 to crunch proxy",
                     exp_sign > 0 and con_sign < 0 and t_crunch > t_turn,
                     f"expansion sign {exp_sign}, contraction sign {con_sign}, crunch {t_crunch:.2f} > turn {t_turn:.2f}"))
results.append(check("P-D2 total age within ±3 Gyr of 33.3 Gyr",
                     abs(t_crunch - 33.3) <= 3.0,
                     f"total {t_crunch:.2f} Gyr vs 33.3 (diff {t_crunch - 33.3:+.2f})"))
results.append(check("P-D3 turnaround within [21.8, 27.8] Gyr total age",
                     21.8 <= t_turn <= 27.8,
                     f"t_turn {t_turn:.2f} Gyr"))
results.append(check("P-E1 no da/dt<0 to a=1e3",
                     bool(np.all(dadt_E > 0)),
                     f"min da/dt = {float(np.min(dadt_E)):.3e}"))
results.append(check("P-E2 de Sitter endpoint: w(100) within 0.01 of -1, H(100) within 5% of H(1e3)",
                     abs(w_at_100 + 1) <= 0.01 and abs(H_ratio_100_to_1000 - 1) <= 0.05,
                     f"w(100)={w_at_100:.4f}, H ratio={H_ratio_100_to_1000:.4f}"))
results.append(check("P-A1 dynamical arrow reverses in D, persists in E",
                     exp_sign > 0 and con_sign < 0 and bool(np.all(dadt_E > 0)),
                     "D sign flips, E sign stays positive"))
print("P-A2 thermodynamic entropy arrow: OPEN by design (entropy not computed in any Friedmann toy here).")
n_pass = sum(results)
print(f"\nScore (excluding OPEN P-A2): {n_pass}/6")

# ---- plot (time since now, so the two floors share an axis) ----
t_D_since_now = t_D - t_now_D
turn_since_now = t_turn - t_now_D
fig, axes = plt.subplots(2, 1, figsize=(12, 9))
ax = axes[0]
ax.plot(t_D_since_now, a_D, color="#ff5555", lw=2, label="D: Axion + negative Λ (toy) — turnaround + crunch")
ax.plot(t_E, a_E, color="#22cc66", lw=2, label="E: EPJC no-crunch quintessence (toy) — de Sitter endpoint")
ax.axvline(turn_since_now, color="gray", ls=":", alpha=0.7)
ax.text(turn_since_now, 1.5, f" D turnaround\n a_max={a_max:.2f}, +{turn_since_now:.1f} Gyr from now", fontsize=9, va="top")
ax.axhline(1.0, color="k", ls="--", lw=1, alpha=0.5)
ax.set_xlabel("time since now (Gyr)")
ax.set_ylabel("scale factor a(t)")
ax.set_title("Two new floors: contraction vs eternal expansion")
ax.legend(fontsize=10)
ax.set_xlim(0, max(t_crunch - t_now_D, float(t_E[-1])) * 0.6)
ax.set_ylim(0, 5)
ax = axes[1]
ax.plot(t_D_since_now, a_D, color="#ff5555", lw=2, label="D: turnaround + contraction (da/dt < 0 after turn)")
ax.plot(t_E, a_E, color="#22cc66", lw=2, label="E: monotonic expansion")
ax.axvline(turn_since_now, color="gray", ls=":", alpha=0.7)
ax.set_xlabel("time since now (Gyr, zoom on turnaround region)")
ax.set_ylabel("scale factor a(t)")
ax.set_title("Zoom: Floor D reverses; Floor E does not")
ax.legend(fontsize=10)
ax.set_xlim(0, 80)
ax.set_ylim(0, 3)
fig.suptitle("COSMOS-CRUNCH: does the arrow survive contraction?", fontsize=13)
fig.tight_layout()
fig.savefig("cosmos_crunch.png", dpi=110)
print("\nwrote cosmos_crunch.png")

lines = [
    f"Floor D: a_max={a_max:.4f} t_now_toy={t_now_D:.2f} t_turn={t_turn:.2f} turn_from_now={turn_from_now:.2f} t_crunch={t_crunch:.2f}",
    f"Floor D: expansion sign={exp_sign} contraction sign={con_sign}",
    f"Floor E: da/dt>0 always={bool(np.all(dadt_E > 0))} w(100)={w_at_100:.4f} H(100)/H(1e3)={H_ratio_100_to_1000:.4f}",
    f"Score (excl. OPEN P-A2): {n_pass}/6",
]
with open("output.txt", "w") as f:
    f.write("\n".join(lines) + "\n")
raise SystemExit(0 if n_pass == 6 else 1)
