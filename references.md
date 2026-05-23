# References

Everything I read, watched, or used to understand these models.

---
## How I Actually Learned This

- **Artem Kirsanov** (YouTube) — the single best visual explanation of both models I found.
  Seriously, watch his videos before reading anything else.
  https://www.youtube.com/@ArtemKirsanov

- **Claude & Gemini** — used these to ask follow-up questions, work through the math,
  and check my understanding. Basically an interactive textbook.

---

## If You Want to Go Deeper (I haven't fully read these yet)

## Original Papers

- **Hodgkin & Huxley (1952)** — *A Quantitative Description of Membrane Current and its Application to Conduction and Excitation in Nerve* — Journal of Physiology
  - The original paper. Dense but worth reading at least the introduction.
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1392413/

- **Izhikevich (2003)** — *Simple Model of Spiking Neurons* — IEEE Transactions on Neural Networks
  - Much more readable than HH. The parameter table alone is worth it.
  - https://www.izhikevich.org/publications/spikes.pdf

---

## Books

- **Theoretical Neuroscience** — Dayan & Abbott (2001)
  - The standard textbook. Chapter 5 covers conductance-based models (HH).
  - Free PDF: http://www.gatsby.ucl.ac.uk/~lmate/biblio/dayanabbott.pdf

- **Dynamical Systems in Neuroscience** — Izhikevich (2007)
  - Covers the mathematical foundations — bifurcations, phase planes, attractors.
  - Free PDF: https://www.izhikevich.org/publications/dsn.pdf

---

## Video Lectures

- **Neuromatch Academy** — Computational Neuroscience (free, online)
  - https://compneuro.neuromatch.io/
  - W1D1 covers the basics of neuron models

- **MIT 9.40 — Introduction to Neural Computation**
  - Lectures available on MIT OpenCourseWare
  - https://ocw.mit.edu/courses/9-40-introduction-to-neural-computation-spring-2018/

---

## Code References

- Scipy `solve_ivp` documentation — used for integrating the HH ODEs
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html

- Izhikevich's own MATLAB code (useful for cross-checking)
  - https://www.izhikevich.org/publications/figure1.m

---

## Other Useful Links

- Izhikevich's personal website — has PDFs of all his papers + interactive demos
  - https://www.izhikevich.org/

- Scholarpedia article on HH model — good for conceptual understanding
  - http://www.scholarpedia.org/article/Hodgkin-Huxley_model
