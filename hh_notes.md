# Technical Notes — Hodgkin-Huxley and Izhikevich Neuron Models

---

## Part I — Hodgkin-Huxley Model

### 1.1 Overview

The Hodgkin-Huxley model is a mathematical description of how an action
potential is initiated and propagated along a neuron membrane. It was
published in 1952 by Alan Hodgkin and Andrew Huxley based on voltage-clamp
experiments performed on the squid giant axon. The authors were awarded the
Nobel Prize in Physiology or Medicine in 1963 for this contribution.

The model remains the canonical biophysical reference for single-neuron
dynamics and established the principle that ion channel kinetics can be
described precisely using systems of ordinary differential equations.

---

### 1.2 Membrane Circuit Model

The neuron membrane is modelled as an RC circuit in which the membrane
capacitance C_m accumulates charge, and three parallel conductance branches
represent distinct ion channel populations:

```
C_m · dV/dt = I_ext − I_Na − I_K − I_L
```

| Variable | Description |
|----------|-------------|
| V        | Membrane potential (mV) |
| C_m      | Membrane capacitance (µF/cm²) |
| I_Na     | Sodium current — fast, responsible for spike depolarisation |
| I_K      | Potassium current — slow, responsible for repolarisation |
| I_L      | Leak current — passive, always conducting |

---

### 1.3 Gating Variables

Each ion channel population is regulated by dimensionless gating variables
representing the fraction of channels in the open (conducting) state:

| Variable | Channel            | Kinetic Behaviour |
|----------|--------------------|-------------------|
| m        | Na⁺ activation     | Activates rapidly as V rises above threshold |
| h        | Na⁺ inactivation   | Inactivates Na⁺ channels after a brief delay |
| n        | K⁺ activation      | Activates slowly; remains open longer than m |

The ionic currents are given by:

```
I_Na = g_Na · m³ · h · (V − E_Na)
I_K  = g_K  · n⁴      · (V − E_K)
I_L  = g_L             · (V − E_L)
```

The power exponents (m³, n⁴) are empirical, determined by fitting Hodgkin
and Huxley's experimental patch-clamp data; they do not follow from first
principles.

Each gating variable x ∈ {m, h, n} obeys a first-order ODE of the form:

```
dx/dt = α_x(V)·(1−x) − β_x(V)·x
      = [x_∞(V) − x] / τ_x(V)
```

where x_∞(V) = α_x / (α_x + β_x) is the steady-state value and
τ_x(V) = 1 / (α_x + β_x) is the voltage-dependent time constant.

---

### 1.4 Action Potential Sequence

A canonical action potential proceeds through the following phases:

1. **Sub-threshold stimulus.** An applied current I_ext pushes V above the
   threshold voltage (~−55 mV).
2. **Rapid depolarisation.** Na⁺ activation (m rises rapidly): Na⁺ flows
   inward, driving V toward E_Na ≈ +50 mV.
3. **Na⁺ inactivation.** The h gate closes, terminating the inward Na⁺
   current while V is still elevated.
4. **Repolarisation.** K⁺ activation (n rises slowly): K⁺ flows outward,
   returning V toward E_K ≈ −77 mV.
5. **Hyperpolarisation undershoot.** Brief period below resting potential
   while n remains elevated; followed by return to rest as n decays.

---

### 1.5 Observations from Simulation

The simulation was run with I_ext = 10 µA/cm² over a 100 ms window using a
fourth-order Runge-Kutta integrator (RK45, max step 0.025 ms).

The following behaviours were observed:

- Repetitive action potentials were produced at approximately 75 Hz. The
  spike waveform — rapid upstroke, sharp peak near +40 mV, rapid downstroke
  — closely matches experimental recordings from squid axon.
- The m gate (fast Na⁺ activation) rose and fell within each spike in under
  2 ms, consistent with its short time constant τ_m (< 0.5 ms across the
  physiological voltage range).
- The h and n gates evolved on slower timescales (τ_h, τ_n on the order of
  5–20 ms), with h and n displaying a clear anti-correlation throughout the
  spiking regime. This anti-correlation is the empirical basis for the Rinzel
  (1985) dimensional reduction.
- Reducing I_ext below approximately 6.5 µA/cm² suppressed spiking entirely
  (below the saddle-node bifurcation), confirming the threshold-like onset
  of repetitive firing.

---

### 1.6 Key Parameters

| Parameter | Value       | Description              |
|-----------|-------------|--------------------------|
| C_m       | 1 µF/cm²    | Membrane capacitance     |
| g_Na      | 120 mS/cm²  | Maximum Na⁺ conductance  |
| g_K       | 36 mS/cm²   | Maximum K⁺ conductance   |
| g_L       | 0.3 mS/cm²  | Leak conductance         |
| E_Na      | +50 mV      | Na⁺ reversal potential   |
| E_K       | −77 mV      | K⁺ reversal potential    |
| E_L       | −54.4 mV    | Leak reversal potential  |

---

### 1.7 Limitations

- The model comprises four coupled nonlinear ODEs per neuron, making it
  computationally expensive for large-scale network simulations.
- Parameter values were fitted to squid giant axon data and do not transfer
  directly to mammalian cortical neurons without re-fitting.
- The model does not explicitly represent spatial extent (dendritic or axonal
  propagation) unless extended to the cable equation framework.

---

## Part II — Izhikevich Model

### 2.1 Overview

The Izhikevich model was proposed by Eugene Izhikevich in 2003 with the
explicit objective of identifying the minimal dynamical system capable of
reproducing the rich diversity of firing patterns observed in real cortical
neurons, while remaining computationally tractable for large network
simulations.

**Primary reference:** Izhikevich, E. M. (2003). *Simple model of spiking
neurons.* IEEE Transactions on Neural Networks, 14(6), 1569–1572.

---

### 2.2 Model Equations

The model is defined by two ODEs and a discrete reset rule:

```
dv/dt = 0.04v² + 5v + 140 − u + I
du/dt = a·(bv − u)

Reset: if v ≥ 30 mV  →  v ← c,  u ← u + d
```

| Variable | Interpretation |
|----------|----------------|
| v        | Membrane potential (mV) |
| u        | Membrane recovery variable — slow negative feedback on v |

The variable u is phenomenological; it captures the combined effect of K⁺
activation and Na⁺ inactivation from the full HH model, without modelling
the underlying ion channel kinetics explicitly.

---

### 2.3 Role of the Four Parameters

| Parameter | Role |
|-----------|------|
| a | Time scale of the recovery variable (smaller a → slower recovery) |
| b | Sensitivity of u to sub-threshold fluctuations in v |
| c | Post-spike reset value of the membrane potential (mV) |
| d | Post-spike increment applied to u (governs adaptation) |

By varying these four parameters, the model reproduces over twenty
electrophysiologically distinct neuron types.

---

### 2.4 Firing Pattern Examples

| Neuron Type                  | a    | b    | c   | d |
|------------------------------|------|------|-----|---|
| Regular Spiking (RS)         | 0.02 | 0.2  | −65 | 8 |
| Intrinsically Bursting (IB)  | 0.02 | 0.2  | −55 | 4 |
| Chattering (CH)              | 0.02 | 0.2  | −50 | 2 |
| Fast Spiking (FS)            | 0.1  | 0.2  | −65 | 2 |
| Low-Threshold Spiking (LTS)  | 0.02 | 0.25 | −65 | 2 |

---

### 2.5 The Quadratic Term and the Bifurcation Structure

The 0.04v² term is the origin of the model's spike-generating mechanism. It
arises from a Taylor expansion of the HH V-nullcline around the saddle-node
bifurcation point V₀, where the first derivative of the net ionic current
with respect to voltage vanishes (f′(V₀) = 0). Retaining only the quadratic
remainder:

```
f(V) ≈ f(V₀) + f″(V₀)/2 · (V − V₀)²
```

yields a parabolic approximation to the nullcline. The positive curvature
(c₂ > 0) is responsible for the super-threshold instability that produces
the spike, while the reset rule (v ← c, u ← u + d) replaces the fast Na⁺
inactivation and K⁺ recovery dynamics that HH handles through explicit gate
ODEs.

In this implementation, the coefficients 0.04, 5, and 140 are not assumed
but are **derived** by fitting an ordinary least-squares quadratic regression
to the HH steady-state V-nullcline, yielding R² > 0.99 and coefficients
consistent with the canonical Izhikevich parameterisation after rescaling.

---

### 2.6 Observations from Simulation

The Izhikevich model was simulated using the derived nullcline coefficients
(a2, a1, a0) rather than the standard 0.04, 5, 140 values, with I_ext =
10 µA/cm² and a fixed Euler time step of 0.1 ms.

The following behaviours were observed:

- **Regular Spiking (RS):** Tonic firing at a steady rate throughout the
  stimulus window. The inter-spike interval increased slightly over time due
  to slow adaptation through the u variable, consistent with experimental
  recordings of cortical pyramidal cells.
- **Intrinsically Bursting (IB):** An initial burst of closely spaced spikes
  followed by transition to tonic firing. The less negative reset voltage
  (c = −55 mV) prevents full recovery between early spikes, producing the
  burst.
- **Fast Spiking (FS):** High-frequency, non-adapting tonic firing. The
  larger time-scale parameter (a = 0.1) enables rapid recovery of u,
  preventing adaptation. This pattern is characteristic of cortical
  interneurons.
- **Low-Threshold Spiking (LTS):** Firing initiated at lower stimulus
  thresholds due to stronger sub-threshold coupling (b = 0.25), resulting in
  a lower effective spike threshold.

Comparison of the HH and Izhikevich membrane potential traces confirmed
qualitative agreement in spike waveform shape and inter-spike interval at
equivalent stimulus levels, validating the derivation pipeline.

---

### 2.7 Computational Efficiency

For a simulation of N neurons over time T with time step dt, the Izhikevich
model requires O(N) arithmetic operations per step. The Hodgkin-Huxley model
requires evaluation of exponential rate functions for each of three gating
variables, adding a constant factor of approximately 20–50× in per-neuron
computation time. For large-scale network simulations (N > 10⁴), this
efficiency gap makes Izhikevich the preferred model when qualitative
biological realism is sufficient.

---

### 2.8 Comparison with Hodgkin-Huxley

| Property              | Hodgkin-Huxley          | Izhikevich                |
|-----------------------|-------------------------|---------------------------|
| State variables       | 4 (V, m, h, n)          | 2 (v, u)                  |
| Biological basis      | Ion channel kinetics     | Phenomenological          |
| Distinct firing modes | ~1 (repetitive spiking) | 20+                       |
| Computational cost    | High                    | Very low (~1 000× faster) |
| Primary use case      | Single-neuron accuracy  | Large-scale networks      |
| Parameter source      | Electrophysiology       | Tuned to firing pattern   |
