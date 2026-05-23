# Hodgkin-Huxley Model — Notes

## What is it?

A mathematical model of how an action potential is initiated and propagated in a neuron. Published in 1952 by Alan Hodgkin and Andrew Huxley based on experiments on the squid giant axon. They won the Nobel Prize in Physiology/Medicine in 1963 for this work.

---

## The Core Idea

The neuron membrane separates charge — like a capacitor. Ion channels in the membrane let specific ions flow in or out depending on the membrane voltage. This flow of ions *is* the electrical signal.

Hodgkin and Huxley modelled this as a circuit:

```
I_ext = C_m * (dV/dt) + I_Na + I_K + I_L
```

Where:
- `V` — membrane voltage (mV)
- `C_m` — membrane capacitance
- `I_Na` — sodium current (fast, responsible for the spike)
- `I_K` — potassium current (slower, responsible for repolarization)
- `I_L` — leak current (passive, always open)

---

## The Gating Variables

Each ion channel has gating variables that describe what fraction of channels are open:

| Variable | Channel | Behaviour |
|----------|---------|-----------|
| `m` | Na⁺ activation | Opens fast when V rises |
| `h` | Na⁺ inactivation | Closes Na⁺ channels after they open |
| `n` | K⁺ activation | Opens slower, stays open longer |

The currents are:
```
I_Na = g_Na * m³ * h * (V - E_Na)
I_K  = g_K  * n⁴     * (V - E_K)
I_L  = g_L           * (V - E_L)
```

The exponents (m³, n⁴) are empirical — they came from fitting the experimental data, not from first principles.

---

## What Happens During a Spike

1. A stimulus pushes V above a threshold (~-55 mV)
2. Na⁺ channels open (m rises fast) → Na⁺ rushes in → V shoots up
3. Na⁺ channels inactivate (h drops) → Na⁺ flow stops
4. K⁺ channels open (n rises slowly) → K⁺ flows out → V drops back
5. Brief hyperpolarization (undershoot), then return to rest

---

## Why It Matters

- First quantitative model that explained *how* neurons fire
- Still used today as the gold standard for biological accuracy
- Showed that ion channel dynamics could be described with ODEs — opened up the entire field of computational neuroscience

---

## Limitations

- Computationally expensive (4 coupled ODEs per neuron)
- Hard to scale to large networks
- Parameters are specific to squid axon — don't directly transfer to all neurons

---

## My Observations from the Simulation

*(Fill this in after you run the code — what did you notice? Did the spike shape match what you expected? What happened when you changed the stimulus current?)*

---

## Key Parameters Used

| Parameter | Value | Description |
|-----------|-------|-------------|
| `C_m` | 1 µF/cm² | Membrane capacitance |
| `g_Na` | 120 mS/cm² | Max Na⁺ conductance |
| `g_K` | 36 mS/cm² | Max K⁺ conductance |
| `g_L` | 0.3 mS/cm² | Leak conductance |
| `E_Na` | 50 mV | Na⁺ reversal potential |
| `E_K` | -77 mV | K⁺ reversal potential |
| `E_L` | -54.4 mV | Leak reversal potential |
