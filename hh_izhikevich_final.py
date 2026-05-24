# -*- coding: utf-8 -*-
"""
hh_izhikevich.py
================
Computational simulation and derivation of the Hodgkin-Huxley (1952) and
Izhikevich (2003) neuron models, demonstrating the mathematical reduction
from a 4-dimensional biophysical system to a 2-dimensional phenomenological
model via quasi-static approximation, Rinzel reduction, and Taylor expansion
at the saddle-node bifurcation point.

Dependencies:
    numpy, matplotlib, scipy, scikit-learn

Usage:
    python hh_izhikevich.py

Plots are saved to the 'plots/' directory (created automatically).

Author  : Srinija
Date    : 2026
"""

import os
import warnings

os.makedirs("plots", exist_ok=True)
warnings.filterwarnings("ignore")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.integrate import solve_ivp
from sklearn.linear_model import LinearRegression

plt.rcParams.update({"figure.dpi": 120, "font.size": 11})


# =============================================================================
# Section 1 — The Full Hodgkin-Huxley Model
# =============================================================================
# The membrane equation:
#
#   C_m dV/dt = I - g_Na·m³h·(V-E_Na) - g_K·n⁴·(V-E_K) - g_L·(V-E_L)
#
# Each gating variable x ∈ {m, h, n} obeys:
#
#   dx/dt = α_x(V)·(1-x) - β_x(V)·x = [x_∞(V) - x] / τ_x(V)
# =============================================================================

# ── Membrane and conductance parameters ──────────────────────────────────────
C_m  = 1.0    # µF/cm²
g_Na = 120.0  # mS/cm²
g_K  = 36.0   # mS/cm²
g_L  = 0.3    # mS/cm²
E_Na = 50.0   # mV
E_K  = -77.0  # mV
E_L  = -54.387  # mV

# ── Voltage-dependent rate functions ─────────────────────────────────────────
def alpha_m(V): return 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
def beta_m(V):  return 4.0 * np.exp(-(V + 65) / 18)

def alpha_h(V): return 0.07 * np.exp(-(V + 65) / 20)
def beta_h(V):  return 1.0 / (1 + np.exp(-(V + 35) / 10))

def alpha_n(V): return 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
def beta_n(V):  return 0.125 * np.exp(-(V + 65) / 80)

def x_inf(alpha, beta, V): return alpha(V) / (alpha(V) + beta(V))
def tau_x(alpha, beta, V): return 1.0 / (alpha(V) + beta(V))


# ── Hodgkin-Huxley ODE system ─────────────────────────────────────────────────
def hh_ode(t, y, I_ext):
    V, m, h, n = y
    I_Na = g_Na * m**3 * h * (V - E_Na)
    I_K  = g_K  * n**4     * (V - E_K)
    I_L  = g_L             * (V - E_L)
    dV = (I_ext - I_Na - I_K - I_L) / C_m
    dm = alpha_m(V) * (1 - m) - beta_m(V) * m
    dh = alpha_h(V) * (1 - h) - beta_h(V) * h
    dn = alpha_n(V) * (1 - n) - beta_n(V) * n
    return [dV, dm, dh, dn]


# ── Initial conditions and simulation ────────────────────────────────────────
V0 = -65.0
y0 = [
    V0,
    x_inf(alpha_m, beta_m, V0),
    x_inf(alpha_h, beta_h, V0),
    x_inf(alpha_n, beta_n, V0),
]

t = np.arange(0, 100, 0.01)
sol = solve_ivp(
    hh_ode, (0, 100), y0,
    method="RK45", t_eval=t, max_step=0.025, args=(10.0,)
)
V_hh, m_hh, h_hh, n_hh = sol.y

fig, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
axes[0].plot(t, V_hh, "k", lw=1.2)
axes[0].set_ylabel("V (mV)")
axes[0].set_title("Hodgkin–Huxley Simulation (I = 10 µA/cm²)")
axes[1].plot(t, m_hh, label="m  (fast activation)")
axes[1].plot(t, h_hh, label="h  (slow inactivation)")
axes[1].plot(t, n_hh, label="n  (K⁺ activation)")
axes[1].set_xlabel("Time (ms)")
axes[1].set_ylabel("Gate value")
axes[1].legend(ncol=3)
plt.tight_layout()
plt.savefig("plots/01_hh_action_potential.png", dpi=150)
plt.show()


# =============================================================================
# Section 2 — Timescale Separation: Quasi-Static Approximation for m
# =============================================================================
# If τ_m ≪ τ_n, τ_h everywhere, then m equilibrates almost instantaneously
# and can be replaced by the algebraic constraint m = m_∞(V), reducing the
# system from 4D to 3D.
# =============================================================================

V_r = np.linspace(-80, 40, 500)
tm = tau_x(alpha_m, beta_m, V_r)
tn = tau_x(alpha_n, beta_n, V_r)
th = tau_x(alpha_h, beta_h, V_r)

print(f"τ_m  [{tm.min():.3f}, {tm.max():.3f}] ms  ← fast")
print(f"τ_n  [{tn.min():.3f}, {tn.max():.3f}] ms")
print(f"τ_h  [{th.min():.3f}, {th.max():.3f}] ms")
print(f"\nmean τ_n / τ_m ≈ {np.mean(tn)/np.mean(tm):.0f}×  →  m ≈ m_∞(V) is valid")

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.semilogy(V_r, tm, label=r"$\tau_m$ (fast)", lw=2)
ax.semilogy(V_r, tn, label=r"$\tau_n$",         lw=2)
ax.semilogy(V_r, th, label=r"$\tau_h$",         lw=2)
ax.set_xlabel("V (mV)")
ax.set_ylabel("Time constant (ms, log scale)")
ax.set_title("Gate Timescales — Justifying the Quasi-Static Approximation")
ax.legend()
plt.tight_layout()
plt.savefig("plots/02_timescale_separation.png", dpi=150)
plt.show()


# =============================================================================
# Section 3 — Phase-Plane Reduction to 2D
# =============================================================================
# With m ≈ m_∞(V) the system is 3D: (V, h, n).  The Rinzel (1985) reduction
# exploits the strong anti-correlation between h and n during spiking:
#   h ≈ 0.89 − 1.1n
# This yields a 2D system in (V, u) where u ≡ n serves as the single
# slow recovery variable.
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# h–n anti-correlation
sc = axes[0].scatter(n_hh[::10], h_hh[::10], s=2, alpha=0.3,
                     c=t[::10], cmap="viridis")
axes[0].set_xlabel("n  (K⁺ activation gate)")
axes[0].set_ylabel("h  (Na⁺ inactivation gate)")
axes[0].set_title("h–n Anti-Correlation (Rinzel Reduction)")
fig.colorbar(sc, ax=axes[0], label="Time (ms)")

# V–n phase portrait
axes[1].plot(V_hh[::5], n_hh[::5], lw=0.5, alpha=0.6, color="steelblue")
axes[1].set_xlabel("V (mV)")
axes[1].set_ylabel("n")
axes[1].set_title("Phase Portrait: the V–n Plane")

plt.tight_layout()
plt.savefig("plots/03_phase_plane.png", dpi=150)
plt.show()


# =============================================================================
# Section 4 — Taylor Expansion at the Saddle-Node Bifurcation
# =============================================================================
# At the bifurcation point V₀: f′(V₀) = 0  (the linear term vanishes).
# Retaining the quadratic remainder:
#   f(V) ≈ f(V₀) + f″(V₀)/2 · (V − V₀)²
# This leads to the parabolic V-nullcline:
#   u = c₀ + c₁V + c₂V²   with c₂ = f″(V₀)/2 > 0
# In Izhikevich's canonical parameterisation: 0.04v² + 5v + 140.
# =============================================================================


# =============================================================================
# Section 5 — Fitting the Quadratic Nullcline to HH Data
# =============================================================================

# Steady-state V-nullcline: set dV/dt = 0 with all gates at steady state
V_grid = np.linspace(-80, 40, 500)
m_ss = x_inf(alpha_m, beta_m, V_grid)
h_ss = x_inf(alpha_h, beta_h, V_grid)
n_ss = x_inf(alpha_n, beta_n, V_grid)

u_nullcline = (
    g_Na * m_ss**3 * h_ss * (V_grid - E_Na)
    + g_K  * n_ss**4       * (V_grid - E_K)
    + g_L                  * (V_grid - E_L)
)

X   = np.column_stack([V_grid, V_grid**2])
reg = LinearRegression().fit(X, u_nullcline)
c0      = reg.intercept_
c1, c2  = reg.coef_
R2      = reg.score(X, u_nullcline)

print(f"\nNullcline fit (HH units):")
print(f"  c₀ = {c0:+.4f}   c₁ = {c1:+.4f}   c₂ = {c2:+.4f}   R² = {R2:.4f}")

fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(V_grid, u_nullcline, s=3, alpha=0.4,
           label="HH steady-state nullcline", zorder=3)
ax.plot(V_grid, c0 + c1 * V_grid + c2 * V_grid**2, "r", lw=2,
        label=f"Quadratic fit  (R² = {R2:.3f})")
ax.set_xlabel("V (mV)")
ax.set_ylabel("I_ionic (µA/cm²)")
ax.set_title("V-Nullcline: Steady-State HH vs. Quadratic Approximation")
ax.legend()
plt.tight_layout()
plt.savefig("plots/04_nullcline_fit.png", dpi=150)
plt.show()


# =============================================================================
# Section 6 — The Izhikevich Model
# =============================================================================
# Replacing f(V) with the fitted parabola and writing u as a combined
# recovery variable yields:
#
#   dv/dt = 0.04v² + 5v + 140 − u + I
#   du/dt = a·(bv − u)
#
# Reset rule:  if v ≥ 30 mV  →  v ← c,  u ← u + d
# =============================================================================

# Rescale fitted HH nullcline coefficients to Izhikevich canonical form
k_scale = c2 / 0.04
a2 = c2 / k_scale   # → 0.04
a1 = c1 / k_scale   # → ~5
a0 = c0 / k_scale   # → ~140

print("\nRescaled Izhikevich nullcline coefficients:")
print(f"  a2  (canonical ~0.04)  = {a2:.4f}")
print(f"  a1  (canonical ~5)     = {a1:.4f}")
print(f"  a0  (canonical ~140)   = {a0:.4f}")
print(f"\n  Scale factor k = {k_scale:.4f}")
print(f"  Canonical : 0.04v² + 5v + 140")
print(f"  Derived   : {a2:.4f}v² + {a1:.4f}v + {a0:.4f}")


def izhikevich(a, b, c_reset, d, I_ext=10, T=200, dt=0.1):
    """
    Simulate the Izhikevich neuron model using nullcline coefficients
    derived from the Hodgkin-Huxley fit (a2, a1, a0).

    Parameters
    ----------
    a       : float  — recovery time scale
    b       : float  — subthreshold coupling of u to v
    c_reset : float  — post-spike reset voltage (mV)
    d       : float  — post-spike recovery increment
    I_ext   : float  — applied current (µA/cm²)
    T       : float  — simulation duration (ms)
    dt      : float  — time step (ms)

    Returns
    -------
    t, v, u : ndarrays — time, membrane potential, recovery variable
    spikes  : list    — spike times (ms)
    """
    t      = np.arange(0, T, dt)
    v      = np.full(len(t), -65.0)
    u      = np.full(len(t), b * -65.0)
    spikes = []

    for i in range(1, len(t)):
        v[i] = v[i-1] + dt * (a2 * v[i-1]**2 + a1 * v[i-1] + a0
                               - u[i-1] + I_ext)
        u[i] = u[i-1] + dt * (a * (b * v[i-1] - u[i-1]))
        if v[i] >= 30:
            v[i-1] = 30
            v[i]   = c_reset
            u[i]  += d
            spikes.append(t[i])

    return t, v, u, spikes


neuron_types = {
    "Regular Spiking (RS)":          dict(a=0.02, b=0.2,  c_reset=-65, d=8),
    "Intrinsically Bursting (IB)":   dict(a=0.02, b=0.2,  c_reset=-55, d=4),
    "Fast Spiking (FS)":             dict(a=0.1,  b=0.2,  c_reset=-65, d=2),
    "Low-Threshold Spiking (LTS)":   dict(a=0.02, b=0.25, c_reset=-65, d=2),
}

fig, axes = plt.subplots(2, 2, figsize=(13, 7), sharex=True)
for ax, (name, params) in zip(axes.flat, neuron_types.items()):
    t_iz, v_iz, u_iz, spks = izhikevich(**params)
    ax.plot(t_iz, v_iz, "k", lw=0.9)
    ax.set_title(name, fontsize=10)
    ax.set_ylabel("v (mV)")
    ax.set_ylim(-90, 45)
    fr = len(spks) / 0.2 if spks else 0
    ax.text(0.97, 0.97, f"{fr:.0f} Hz",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9, color="steelblue")
for ax in axes[1]:
    ax.set_xlabel("Time (ms)")
fig.suptitle(
    f"Izhikevich Model — Derived from HH Nullcline Fit\n"
    f"(a2 = {a2:.4f},  a1 = {a1:.4f},  a0 = {a0:.4f})",
    fontsize=11,
)
plt.tight_layout()
plt.savefig("plots/05_izhikevich_firing_patterns.png", dpi=150)
plt.show()


# ── Side-by-side comparison ───────────────────────────────────────────────────
t_iz, v_iz, _, _ = izhikevich(0.02, 0.2, -65, 8, I_ext=10, T=100)

fig, axes = plt.subplots(2, 1, figsize=(11, 5), sharex=True)
axes[0].plot(t, V_hh, "k", lw=1.2, label="Hodgkin–Huxley (4D)")
axes[0].set_ylabel("V (mV)")
axes[0].legend(loc="upper right")
axes[0].set_ylim(-85, 60)

axes[1].plot(t_iz, v_iz, color="firebrick", lw=1.2,
             label=f"Izhikevich — derived  "
                   f"(a2 = {a2:.3f},  a1 = {a1:.3f},  a0 = {a0:.2f})")
axes[1].set_ylabel("v (mV)")
axes[1].set_xlabel("Time (ms)")
axes[1].legend(loc="upper right")
axes[1].set_ylim(-85, 60)

fig.suptitle("HH vs. Izhikevich Derived from HH Nullcline Fit", fontsize=11)
plt.tight_layout()
plt.savefig("plots/06_hh_vs_izhikevich.png", dpi=150)
plt.show()


# =============================================================================
# Section 7 — Summary of the Derivation
# =============================================================================

print("\n" + "=" * 58)
print("DERIVATION SUMMARY")
print("=" * 58)
print(f"{'Step':<38} {'Dimension':>9}")
print("-" * 58)
print(f"{'Full Hodgkin-Huxley model':<38} {'4D':>9}")
print(f"{'Quasi-static m → m_∞(V)':<38} {'3D':>9}")
print(f"{'Rinzel reduction: h ≈ φ(n)':<38} {'2D':>9}")
print(f"{'Taylor expansion at bifurcation':<38} {'2D':>9}")
print("-" * 58)
print(f"\nFitted nullcline (HH units):")
print(f"  u = {c0:.2f} + {c1:.4f}·V + {c2:.4f}·V²    R² = {R2:.4f}")
print(f"\nRescaled (Izhikevich units):")
print(f"  u = {a0:.2f} + {a1:.4f}·v + {a2:.4f}·v²")
print(f"\nCanonical Izhikevich:")
print(f"  u = 140 + 5·v + 0.04·v²")
print("=" * 58)
print("\nPlots saved to:  plots/")
