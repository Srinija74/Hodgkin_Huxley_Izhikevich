"""
hh_izhikevich.py
================
Demonstrates the step-by-step reduction of the Hodgkin-Huxley (1952) model
from 4D to 2D, and compares the resulting 2D reduced system with the
phenomenological Izhikevich (2003) model.
 
Reduction pipeline
------------------
  4D  →  3D : quasi-static approximation  m ≈ m_∞(V)   (τ_m ≪ τ_h, τ_n)
  3D  →  2D : Rinzel (1985) reduction     h ≈ φ(n)      (fitted from HH trajectory)
  2D system : state = (V, n), exact HH kinetics for dn/dt
 
Izhikevich comparison
---------------------
The canonical 0.04v²+5v+140 parabola is Izhikevich's own phenomenological
choice — it cannot be algebraically derived from HH because the V-nullcline
of the 2D reduced system is S-shaped (R²≈0.50 for a quadratic fit).
The Izhikevich model is therefore presented as a parallel phenomenological
model, not as an analytic consequence of the reduction.
"""
 
import matplotlib
matplotlib.use("Agg")
 
import os, warnings
os.makedirs("plots", exist_ok=True)
warnings.filterwarnings("ignore")
 
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from sklearn.linear_model import LinearRegression
 
plt.rcParams.update({"figure.dpi": 120, "font.size": 11})
 
# ── colour palette ────────────────────────────────────────────────────────────
C_HH  = "black"
C_2D  = "#e05c2a"   # burnt orange — 2-D reduced
C_IZH = "#2a7ae0"   # steel blue   — Izhikevich
C_NC  = "#2ca02c"   # green        — nullclines
 
 
# =============================================================================
# Section 1 — HH parameters and rate functions
# =============================================================================
C_m  = 1.0;   g_Na = 120.0; g_K = 36.0; g_L = 0.3
E_Na = 50.0;  E_K  = -77.0; E_L = -54.387
 
def alpha_m(V): return 0.1*(V+40)/(1-np.exp(-(V+40)/10))
def beta_m(V):  return 4.0*np.exp(-(V+65)/18)
def alpha_h(V): return 0.07*np.exp(-(V+65)/20)
def beta_h(V):  return 1.0/(1+np.exp(-(V+35)/10))
def alpha_n(V): return 0.01*(V+55)/(1-np.exp(-(V+55)/10))
def beta_n(V):  return 0.125*np.exp(-(V+65)/80)
 
def x_inf(a, b, V): return a(V) / (a(V) + b(V))
def tau_x(a, b, V): return 1.0  / (a(V) + b(V))
 
 
# =============================================================================
# Section 2 — Full 4D Hodgkin-Huxley simulation
# =============================================================================
def hh_ode(t, y, I_ext=10.0):
    V, m, h, n = y
    dV = (I_ext
          - g_Na*m**3*h*(V-E_Na)
          - g_K *n**4  *(V-E_K)
          - g_L        *(V-E_L)) / C_m
    dm = alpha_m(V)*(1-m) - beta_m(V)*m
    dh = alpha_h(V)*(1-h) - beta_h(V)*h
    dn = alpha_n(V)*(1-n) - beta_n(V)*n
    return [dV, dm, dh, dn]
 
V0  = -65.0
y0  = [V0,
       x_inf(alpha_m, beta_m, V0),
       x_inf(alpha_h, beta_h, V0),
       x_inf(alpha_n, beta_n, V0)]
t   = np.arange(0, 100, 0.01)
 
sol_hh = solve_ivp(hh_ode, (0,100), y0,
                   method="RK45", t_eval=t, max_step=0.025, args=(10.0,))
V_hh, m_hh, h_hh, n_hh = sol_hh.y
 
n_spk_hh = int(np.sum((V_hh[1:]>0) & (V_hh[:-1]<=0)))
print(f"[HH 4D]  spikes = {n_spk_hh}  V ∈ [{V_hh.min():.1f}, {V_hh.max():.1f}] mV")
 
# ── Plot 1: HH action potential ───────────────────────────────────────────────
fig, axes = plt.subplots(2, 1, figsize=(10,5), sharex=True)
axes[0].plot(t, V_hh, C_HH, lw=1.2)
axes[0].set_ylabel("V  (mV)")
axes[0].set_title("Hodgkin–Huxley (4D)  —  I = 10 µA/cm²")
axes[1].plot(t, m_hh, label="m  fast activation")
axes[1].plot(t, h_hh, label="h  slow inactivation")
axes[1].plot(t, n_hh, label="n  K⁺ activation")
axes[1].set_xlabel("Time (ms)"); axes[1].set_ylabel("Gate value")
axes[1].legend(ncol=3, fontsize=9)
plt.tight_layout()
fig.savefig("plots/01_hh_action_potential.png", dpi=150); plt.close(fig)
print("→ saved 01_hh_action_potential.png")
 
 
# =============================================================================
# Section 3 — Timescale separation: justify m ≈ m_∞(V)
# =============================================================================
V_r = np.linspace(-80, 40, 500)
tm = tau_x(alpha_m, beta_m, V_r)
tn = tau_x(alpha_n, beta_n, V_r)
th = tau_x(alpha_h, beta_h, V_r)
 
print(f"\n[Timescales]")
print(f"  τ_m ∈ [{tm.min():.3f}, {tm.max():.3f}] ms  ← fastest")
print(f"  τ_n ∈ [{tn.min():.3f}, {tn.max():.3f}] ms")
print(f"  τ_h ∈ [{th.min():.3f}, {th.max():.3f}] ms")
print(f"  mean τ_n/τ_m ≈ {np.mean(tn)/np.mean(tm):.0f}×  →  m ≈ m_∞(V) valid")
 
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.semilogy(V_r, tm, lw=2, label=r"$\tau_m$  (fast — eliminated)")
ax.semilogy(V_r, tn, lw=2, label=r"$\tau_n$")
ax.semilogy(V_r, th, lw=2, label=r"$\tau_h$")
ax.set_xlabel("V (mV)"); ax.set_ylabel("Time constant (ms, log)")
ax.set_title("Step 1: Gate timescales — justifying m ≈ m∞(V)  (4D → 3D)")
ax.legend()
plt.tight_layout()
fig.savefig("plots/02_timescale_separation.png", dpi=150); plt.close(fig)
print("→ saved 02_timescale_separation.png")
 
 
# =============================================================================
# Section 4 — Rinzel reduction: fit h ≈ φ(n) from HH trajectory  (3D → 2D)
# =============================================================================
reg_hn      = LinearRegression().fit(n_hh.reshape(-1,1), h_hh)
h_slope     = reg_hn.coef_[0]
h_int       = reg_hn.intercept_
R2_hn       = reg_hn.score(n_hh.reshape(-1,1), h_hh)
 
print(f"\n[Rinzel h–n fit from HH trajectory]")
print(f"  h ≈ {h_slope:.4f}·n + {h_int:.4f}   R² = {R2_hn:.4f}")
 
fig, axes = plt.subplots(1, 2, figsize=(12,4))
 
sc = axes[0].scatter(n_hh[::10], h_hh[::10], s=2, alpha=0.4,
                     c=t[::10], cmap="viridis")
n_fit = np.linspace(n_hh.min(), n_hh.max(), 100)
axes[0].plot(n_fit, h_slope*n_fit+h_int, "r", lw=2,
             label=f"h = {h_slope:.3f}n + {h_int:.3f}  (R²={R2_hn:.3f})")
axes[0].set_xlabel("n  (K⁺ activation)"); axes[0].set_ylabel("h  (Na⁺ inactivation)")
axes[0].set_title("Step 2: h–n anti-correlation  (3D → 2D)")
axes[0].legend(fontsize=9)
fig.colorbar(sc, ax=axes[0], label="Time (ms)")
 
axes[1].plot(V_hh[::5], n_hh[::5], lw=0.6, alpha=0.7, color="steelblue")
axes[1].set_xlabel("V (mV)"); axes[1].set_ylabel("n")
axes[1].set_title("HH trajectory in the V–n phase plane")
plt.tight_layout()
fig.savefig("plots/03_rinzel_reduction.png", dpi=150); plt.close(fig)
print("→ saved 03_rinzel_reduction.png")
 
 
# =============================================================================
# Section 5 — 2D reduced system
#
#   dV/dt = [I − g_Na·m_∞(V)³·(h_s·n+h_i)·(V−E_Na)
#              − g_K·n⁴·(V−E_K) − g_L·(V−E_L)] / C_m
#   dn/dt = α_n(V)·(1−n) − β_n(V)·n
#
# Both m and h are no longer ODEs — m is an algebraic function of V,
# h is an algebraic function of n.  State vector is (V, n) only.
# =============================================================================
 
def reduced_2d(t, y, I_ext=10.0):
    V, n = y
    m   = x_inf(alpha_m, beta_m, V)
    h   = np.clip(h_slope*n + h_int, 0.0, 1.0)
    dV  = (I_ext
           - g_Na*m**3*h*(V-E_Na)
           - g_K *n**4  *(V-E_K)
           - g_L        *(V-E_L)) / C_m
    dn  = alpha_n(V)*(1-n) - beta_n(V)*n
    return [dV, dn]
 
y0_2d   = [V0, x_inf(alpha_n, beta_n, V0)]
sol_2d  = solve_ivp(reduced_2d, (0,100), y0_2d,
                    method="RK45", t_eval=t, max_step=0.025)
V_2d, n_2d = sol_2d.y
n_spk_2d = int(np.sum((V_2d[1:]>0) & (V_2d[:-1]<=0)))
print(f"\n[2D reduced]  spikes = {n_spk_2d}  V ∈ [{V_2d.min():.1f}, {V_2d.max():.1f}] mV")
 
 
# =============================================================================
# Section 6 — Phase-plane nullclines of the 2D system
#
# V-nullcline: set dV/dt = 0, solve for n at each V  (numerical, brentq)
# n-nullcline: dn/dt = 0  →  n = n_∞(V)             (analytic)
#
# The V-nullcline is S-shaped (2 turning points) — this is what gives the
# system its excitable / oscillatory character.  A single parabola cannot
# capture an S-curve, so R² of a quadratic fit stays ~0.50.
# This is why the Izhikevich parabola is phenomenological, not derived.
# =============================================================================
 
V_sw  = np.linspace(-80, 40, 400)
n_Vn  = np.full_like(V_sw, np.nan)   # V-nullcline
for i, V in enumerate(V_sw):
    m = x_inf(alpha_m, beta_m, V)
    def eq(n, V=V, m=m):
        h = np.clip(h_slope*n + h_int, 0, 1)
        return (10.0
                - g_Na*m**3*h*(V-E_Na)
                - g_K*n**4  *(V-E_K)
                - g_L       *(V-E_L))
    try:
        n_Vn[i] = brentq(eq, 0.0, 1.0, xtol=1e-8)
    except ValueError:
        pass
 
n_nn  = x_inf(alpha_n, beta_n, V_sw)   # n-nullcline
 
# Quadratic fit to V-nullcline (shown to be limited)
ok   = ~np.isnan(n_Vn)
Vv, nv = V_sw[ok], n_Vn[ok]
Xq   = np.column_stack([np.ones_like(Vv), Vv, Vv**2])
cq,_,_,_ = np.linalg.lstsq(Xq, nv, rcond=None)
R2_Vnull = 1 - np.sum((nv - Xq@cq)**2) / np.sum((nv - nv.mean())**2)
print(f"\n[V-nullcline quadratic fit]  R² = {R2_Vnull:.4f}  "
      f"← S-shaped curve, parabola is insufficient")
 
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
 
# Left: phase plane
axes[0].plot(Vv, nv,     C_2D, lw=2.5, label="V-nullcline  (dV/dt = 0)")
axes[0].plot(Vv, Xq@cq, "k--", lw=1.5,
             label=f"Quadratic fit  R² = {R2_Vnull:.2f}")
axes[0].plot(V_sw, n_nn, C_NC, lw=2.5, label="n-nullcline  (dn/dt = 0)")
axes[0].plot(V_2d, n_2d, color="grey", lw=0.7, alpha=0.7, label="2D trajectory")
axes[0].set_xlabel("V (mV)"); axes[0].set_ylabel("n")
axes[0].set_title("Phase plane — 2D reduced system\n"
                  "(V-nullcline is S-shaped → quadratic fit fails)")
axes[0].legend(fontsize=9); axes[0].set_xlim(-82, 45); axes[0].set_ylim(0, 1)
 
# Right: voltage traces
axes[1].plot(t, V_hh, C_HH, lw=1.4, label=f"Full HH  (4D, {n_spk_hh} spikes)")
axes[1].plot(t, V_2d, C_2D, lw=1.2, ls="--",
             label=f"2D reduced  (m=m∞, h=φ(n), {n_spk_2d} spikes)")
axes[1].set_xlabel("Time (ms)"); axes[1].set_ylabel("V (mV)")
axes[1].set_title("Voltage trace: 4D HH  vs.  2D reduced")
axes[1].legend(fontsize=9); axes[1].set_ylim(-85, 60)
plt.tight_layout()
fig.savefig("plots/04_phase_plane_and_reduction.png", dpi=150); plt.close(fig)
print("→ saved 04_phase_plane_and_reduction.png")
 
 
# =============================================================================
# Section 7 — Izhikevich model (canonical phenomenological form)
#
#   dv/dt = 0.04v² + 5v + 140 − u + I
#   du/dt = a·(b·v − u)
#   reset: if v ≥ 30  →  v ← c,  u ← u + d
#
# The parabola 0.04v²+5v+140 is Izhikevich's own choice — it places the
# saddle-node bifurcation near −70 mV with threshold near −55 mV.
# It is NOT algebraically derivable from HH via the reduction above.
# =============================================================================
 
def izhikevich(a, b, c_reset, d, I_ext=10.0, T=200.0, dt=0.1):
    t_iz = np.arange(0, T, dt)
    v    = np.full(len(t_iz), -65.0)
    u    = np.full(len(t_iz),  b * -65.0)
    spks = []
    for i in range(1, len(t_iz)):
        v[i] = v[i-1] + dt*(0.04*v[i-1]**2 + 5*v[i-1] + 140 - u[i-1] + I_ext)
        u[i] = u[i-1] + dt*(a*(b*v[i-1] - u[i-1]))
        if v[i] >= 30:
            v[i]  = c_reset     # reset only current step (no trace corruption)
            u[i] += d
            spks.append(t_iz[i])
    return t_iz, v, u, spks
 
neuron_types = {
    "Regular Spiking (RS)":        dict(a=0.02, b=0.2,  c_reset=-65, d=8),
    "Intrinsically Bursting (IB)": dict(a=0.02, b=0.2,  c_reset=-55, d=4),
    "Fast Spiking (FS)":           dict(a=0.1,  b=0.2,  c_reset=-65, d=2),
    "Low-Threshold Spiking (LTS)": dict(a=0.02, b=0.25, c_reset=-65, d=2),
}
 
fig, axes = plt.subplots(2, 2, figsize=(13,7), sharex=True)
for ax, (name, params) in zip(axes.flat, neuron_types.items()):
    t_iz, v_iz, _, spks = izhikevich(**params)
    ax.plot(t_iz, v_iz, C_IZH, lw=0.9)
    ax.set_title(name, fontsize=10); ax.set_ylabel("v (mV)"); ax.set_ylim(-90, 45)
    fr = len(spks) / 0.2
    ax.text(0.97, 0.97, f"{fr:.0f} Hz",
            transform=ax.transAxes, ha="right", va="top", fontsize=9, color=C_IZH)
for ax in axes[1]: ax.set_xlabel("Time (ms)")
fig.suptitle("Izhikevich model — canonical phenomenological form\n"
             "dv/dt = 0.04v² + 5v + 140 − u + I", fontsize=11)
plt.tight_layout()
fig.savefig("plots/05_izhikevich_firing_patterns.png", dpi=150); plt.close(fig)
print("→ saved 05_izhikevich_firing_patterns.png")
 
 
# =============================================================================
# Section 8 — Three-way comparison: HH  |  2D reduced  |  Izhikevich RS
# =============================================================================
t_iz, v_iz, _, spks_iz = izhikevich(0.02, 0.2, -65, 8, I_ext=10, T=100)
n_spk_iz = len(spks_iz)
print(f"\n[Izhikevich RS]  spikes = {n_spk_iz}")
 
fig, axes = plt.subplots(3, 1, figsize=(11,7), sharex=True)
 
axes[0].plot(t, V_hh, C_HH, lw=1.3)
axes[0].set_ylabel("V (mV)")
axes[0].set_title(f"Full Hodgkin–Huxley  (4D)   —  {n_spk_hh} spikes")
axes[0].set_ylim(-85, 60)
 
axes[1].plot(t, V_2d, C_2D, lw=1.3)
axes[1].set_ylabel("V (mV)")
axes[1].set_title(f"2D reduced  (m=m∞, h=φ(n))  —  {n_spk_2d} spikes")
axes[1].set_ylim(-85, 60)
 
axes[2].plot(t_iz, v_iz, C_IZH, lw=1.3)
axes[2].set_ylabel("v (mV)")
axes[2].set_xlabel("Time (ms)")
axes[2].set_title(f"Izhikevich RS  (phenomenological 2D)  —  {n_spk_iz} spikes")
axes[2].set_ylim(-85, 60)
 
fig.suptitle("Three-way comparison: HH  →  2D reduced  →  Izhikevich", fontsize=12)
plt.tight_layout()
fig.savefig("plots/06_three_way_comparison.png", dpi=150); plt.close(fig)
print("→ saved 06_three_way_comparison.png")
 
 
# =============================================================================
# Section 9 — Derivation summary
# =============================================================================
print("\n" + "="*62)
print("REDUCTION PIPELINE SUMMARY")
print("="*62)
print(f"  {'Step':<40} {'Dim':>4}  {'Method'}")
print("  " + "-"*58)
print(f"  {'Full Hodgkin-Huxley  (V, m, h, n)':<40} {'4D':>4}  —")
print(f"  {'Quasi-static: m → m_∞(V)':<40} {'3D':>4}  τ_m ≪ τ_h, τ_n")
rinzel_label = f"Rinzel: h ≈ {h_slope:.3f}·n + {h_int:.3f}  (R²={R2_hn:.3f})"
print(f"  {rinzel_label:<40} {'2D':>4}  linear fit on HH orbit")
print("  " + "-"*58)
print(f"\n  V-nullcline quadratic fit R² = {R2_Vnull:.3f}")
print(f"  → S-shaped curve: parabola is insufficient")
print(f"  → Izhikevich parabola (0.04v²+5v+140) is phenomenological")
print(f"\n  2D reduced spikes : {n_spk_2d}  (full HH: {n_spk_hh})")
print("="*62)
print("\nAll plots saved to  plots/")
 
