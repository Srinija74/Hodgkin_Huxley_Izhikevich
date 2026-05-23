# Hodgkin_Huxley_Izhikevich
# Neuron Models — Hodgkin-Huxley & Izhikevich

Simulations of two foundational computational neuron models, built during my semester break after first year ECE at IIT Guwahati.

I've always been drawn to the intersection of math and biology — and these two models sit right at it. A neuron firing is, at its core, a nonlinear dynamical system. That framing made everything click.

---

## Models

### Hodgkin-Huxley (1952)
Models the neuron membrane as an electrical circuit with voltage-gated ion channels. Biologically detailed, computationally expensive, and historically one of the most important models in all of neuroscience.

### Izhikevich (2003)
A two-variable reduction that trades some biological detail for massive computational efficiency — while still reproducing over 20 distinct neuron firing patterns observed in real neurons.

---

## Results

### Hodgkin-Huxley — Action Potential
![HH Action Potential](hodgkin_huxley/plots/action_potential.png)

### Izhikevich — Firing Patterns
![Izhikevich Firing Patterns](izhikevich/plots/firing_patterns.png)

---

## Repo Structure

```
neuron-models/
├── hodgkin_huxley/
│   ├── hh_model.py         # Core simulation
│   ├── plots/              # Generated figures
│   └── notes.md            # My understanding of the model
├── izhikevich/
│   ├── izh_model.py        # Core simulation
│   ├── plots/              # Generated figures
│   └── notes.md            # My understanding of the model
└── references.md           # Papers and resources
```

---

## How to Run

```bash
pip install numpy matplotlib scipy sklearn

# Hodgkin-Huxley and Izhikevich
python hh_izhikevich.py

```

Plots are saved automatically to the respective `plots/` folders.

---

## Background

I'm a first-year ECE student exploring computational neuroscience out of curiosity. No formal training in neuroscience — just found these models fascinating from a signals and systems perspective.

See `references.md` for everything I read/watched to understand these.
