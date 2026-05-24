# References

All primary literature, textbooks, lecture series, and software resources
consulted in the course of this project are listed below, organised by
category.

---

## Primary Literature

**Hodgkin, A. L. & Huxley, A. F. (1952).**
*A quantitative description of membrane current and its application to
conduction and excitation in nerve.*
Journal of Physiology, 117(4), 500–544.
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1392413/

> The foundational paper establishing the four-variable conductance-based
> model of the squid giant axon action potential. The introduction and
> experimental methods sections are accessible to readers without a
> neuroscience background. The mathematical formulation in Sections 2–4
> is directly implemented in this repository.

---

**Izhikevich, E. M. (2003).**
*Simple model of spiking neurons.*
IEEE Transactions on Neural Networks, 14(6), 1569–1572.
https://www.izhikevich.org/publications/spikes.pdf

> Introduces the two-variable phenomenological model and demonstrates its
> ability to reproduce over twenty distinct cortical firing patterns. The
> parameter table (Table 1) provides the (a, b, c, d) values used in this
> repository.

---

**Rinzel, J. (1985).**
*Excitation dynamics: insights from simplified membrane models.*
Federation Proceedings, 44(15), 2944–2946.

> Establishes the empirical anti-correlation between the h and n gating
> variables during repetitive spiking, providing the justification for
> collapsing the three-dimensional (V, h, n) system to two dimensions.
> This reduction is reproduced in Section 3 of the simulation script.

---

## Textbooks

**Dayan, P. & Abbott, L. F. (2001).**
*Theoretical Neuroscience: Computational and Mathematical Modeling of Neural Systems.*
MIT Press.
Free PDF: http://www.gatsby.ucl.ac.uk/~lmate/biblio/dayanabbott.pdf

> The standard graduate-level textbook for computational neuroscience.
> Chapter 5 (Model Neurons I: Neuroelectronics) provides a thorough
> treatment of conductance-based models, including the HH formalism and
> its reductions.

---

**Izhikevich, E. M. (2007).**
*Dynamical Systems in Neuroscience: The Geometry of Excitability and Bursting.*
MIT Press.
Free PDF: https://www.izhikevich.org/publications/dsn.pdf

> Covers the mathematical foundations underlying both models: bifurcation
> theory, phase-plane analysis, and the classification of neuron excitability
> types. Chapters 4–6 are directly relevant to the reduction pipeline
> implemented in this repository.

---

## Video Lectures

**Kirsanov, A.** (YouTube channel: @ArtemKirsanov)
https://www.youtube.com/@ArtemKirsanov

> Provides detailed visual explanations of both the Hodgkin-Huxley and
> Izhikevich models, covering the biophysical motivation, mathematical
> structure, and phase-plane geometry. These lectures served as the primary
> introductory resource for this project and are recommended as a first
> point of entry prior to consulting the primary literature.

---

**Neuromatch Academy — Computational Neuroscience (W1D1: Neuron Models)**
https://compneuro.neuromatch.io/

> A freely available online course covering the fundamentals of neuron
> modelling, including the HH model and its reductions, with accompanying
> Python tutorials.

---

**MIT OpenCourseWare — 9.40 Introduction to Neural Computation (Spring 2018)**
https://ocw.mit.edu/courses/9-40-introduction-to-neural-computation-spring-2018/

> Lecture notes and problem sets covering conductance-based neuron models,
> integrate-and-fire approximations, and synaptic dynamics.

---

## Software and Code References

**SciPy — scipy.integrate.solve_ivp**
https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html

> The ODE solver used to integrate the four-dimensional HH system. The RK45
> method with max_step = 0.025 ms was selected to resolve the fast m-gate
> dynamics accurately.

---

**Izhikevich, E. M. — Original MATLAB implementation**
https://www.izhikevich.org/publications/figure1.m

> The author's own reference implementation, used to cross-check the Python
> implementation of the firing pattern simulations.

---

## Supplementary Online Resources

**Izhikevich, E. M. — Personal website**
https://www.izhikevich.org/

> Repository of the author's publications, including freely available PDFs
> and interactive demonstrations of the Izhikevich model.

---

**Scholarpedia — Hodgkin-Huxley model**
http://www.scholarpedia.org/article/Hodgkin-Huxley_model

> Peer-reviewed encyclopaedia article providing a concise conceptual overview
> of the HH model, its historical context, and extensions.
