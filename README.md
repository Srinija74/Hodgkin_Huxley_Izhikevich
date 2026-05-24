# Neuron Models — Hodgkin-Huxley & Izhikevich

Computational simulation and mathematical derivation of two foundational
neuron models, implemented as part of an independent study undertaken during
the semester break following the first year of an Electrical and Computer
Engineering programme at IIT Guwahati.

The central objective of this project is not merely to simulate the two models
in isolation, but to derive the Izhikevich model **directly and rigorously
from the Hodgkin-Huxley equations** — making the mathematical reduction
explicit at every step.

---

## Models

### Hodgkin-Huxley (1952)

The Hodgkin-Huxley model represents the neuron membrane as an equivalent
electrical circuit with voltage-gated ion channels. It is governed by a system
of four coupled ordinary differential equations (ODEs) describing the membrane
potential and three gating variables for Na⁺ activation, Na⁺ inactivation,
and K⁺ activation:

```
C_m dV/dt = I − g_Na·m³h·(V−E_Na) − g_K·n⁴·(V−E_K) − g_L·(V−E_L)
```

The model is biologically detailed and remains the gold standard for
single-neuron accuracy, but is computationally expensive at scale.

### Izhikevich (2003)

The Izhikevich model is a two-variable reduction that collapses the
four-dimensional HH system into a pair of ODEs augmented by a discrete reset
rule:

```
dv/dt = 0.04v² + 5v + 140 − u + I
du/dt = a·(bv − u)
if v ≥ 30 mV:  v ← c,  u ← u + d
```

Despite its simplicity, the model reproduces more than twenty distinct firing
patterns observed in real cortical neurons, and is approximately 1 000× more
computationally efficient than Hodgkin-Huxley.

---

## Derivation Pipeline

The script implements the full reduction in a series of documented steps:

| Step | Operation | Resulting Dimension |
|------|-----------|:-------------------:|
| 1 | Full Hodgkin-Huxley system | 4D |
| 2 | Quasi-static approximation: m ≈ m_∞(V) | 3D |
| 3 | Rinzel (1985) reduction: h ≈ φ(n) | 2D |
| 4 | Taylor expansion at the saddle-node bifurcation | 2D |
| 5 | Ordinary least-squares fit to HH nullcline | 2D |
| 6 | Rescaling to canonical Izhikevich form | 2D |

The Izhikevich nullcline coefficients (0.04, 5, 140) are **recovered
from biophysical data** rather than assumed, providing a direct mathematical
bridge between the two models.

---

## Repository Structure

```
Hodgkin_Huxley_Izhikevich/
├── hh_izhikevich.py    # Complete simulation and derivation (single script)
├── hh_notes.md         # Technical notes on both models
├── references.md       # Primary literature and supplementary resources
└── README.md           # This file
```

Generated plots are written to a `plots/` directory created automatically at
runtime:

```
plots/
├── 01_hh_action_potential.png
├── 02_timescale_separation.png
├── 03_phase_plane.png
├── 04_nullcline_fit.png
├── 05_izhikevich_firing_patterns.png
└── 06_hh_vs_izhikevich.png
```

---

## Installation and Usage

**Requirements**

```
python >= 3.8
numpy
matplotlib
scipy
scikit-learn
```

**Install dependencies**

```bash
pip install numpy matplotlib scipy scikit-learn
```

**Run the simulation**

```bash
python hh_izhikevich.py
```

All six plots are saved to the `plots/` directory and displayed interactively.
Console output summarises the timescale separation ratios, nullcline fit
coefficients, and the final derivation table.

---

## Results

The simulation produces the following outputs:

**Plot 1 — HH Action Potential.** Membrane voltage and gate dynamics (m, h, n)
over 100 ms under a constant stimulus of 10 µA/cm².

**Plot 2 — Timescale Separation.** Log-scale comparison of τ_m, τ_n, and τ_h
across the physiological voltage range, confirming that m equilibrates
approximately 50–100× faster than n and h.

**Plot 3 — Phase Plane.** Demonstration of the h–n anti-correlation (Rinzel
reduction) and the V–n phase portrait of the simulated trajectory.

**Plot 4 — Nullcline Fit.** Ordinary least-squares regression of a quadratic
polynomial to the HH steady-state V-nullcline (R² > 0.99), yielding
coefficients consistent with the canonical Izhikevich parameterisation.

**Plot 5 — Izhikevich Firing Patterns.** Four neuron types (Regular Spiking,
Intrinsically Bursting, Fast Spiking, Low-Threshold Spiking) simulated using
the derived nullcline coefficients.

**Plot 6 — HH vs. Izhikevich.** Direct comparison of membrane potential
traces from both models under identical stimulus conditions.

---

## Background

This project was undertaken as an independent exploration of computational
neuroscience, motivated by the author's interest in the intersection of
nonlinear dynamical systems and biological signal processing — topics closely
related to the signals and systems curriculum in Electrical and Computer
Engineering. No prior formal training in neuroscience was assumed.

For the primary literature and supplementary learning resources consulted,
refer to `references.md`.

---

## Acknowledgements

The mathematical exposition draws substantially on the following sources:

- Hodgkin, A. L. & Huxley, A. F. (1952). *A quantitative description of
  membrane current and its application to conduction and excitation in nerve.*
  Journal of Physiology, 117(4), 500–544.
- Izhikevich, E. M. (2003). *Simple model of spiking neurons.* IEEE
  Transactions on Neural Networks, 14(6), 1569–1572.
- Rinzel, J. (1985). *Excitation dynamics: insights from simplified membrane
  models.* Federation Proceedings, 44(15), 2944–2946.
