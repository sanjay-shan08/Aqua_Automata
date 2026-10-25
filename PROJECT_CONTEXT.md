# 📋 Project Context & Academic Rationale

## 1. Domain Background

Water quality surveillance is an essential pillar of public health and smart municipal sanitation infrastructure. Traditional automated infrastructure typically depends on:
- Manual operator thresholds (prone to delay and human error).
- Complex machine learning classifiers (often treated as "black boxes" that lack formal safety guarantees).

In safety-critical operations—such as shutting down water pipelines or releasing neutralizers—**mathematical determinism and predictable fail-safes are mandatory**.

---

## 2. Why Finite Automata (FLA)?

Finite State Automata provide rigorous mathematical models that are uniquely suited for embedded IoT controllers and smart sanitation plants:

1. **Deterministic Guarantees:** Given any operational state and sensor input, the next state is uniquely determined with zero ambiguity ($\delta: Q \times \Sigma \to Q$).
2. **Minimal Computational Footprint:** Evaluating an FSM requires $O(1)$ constant time and $O(1)$ memory per symbol, making it executable on ultra-low-power microcontrollers (e.g., ESP32, STM32, Arduino) deployed directly at water pumps.
3. **Formal Verification:** Automata can be formally verified using model checking techniques to guarantee that hazardous conditions always lead to an accept state (lockdown) and never enter an undefined state.
4. **Resilience to Flapping:** By tracking memory through states rather than just checking instantaneous raw numbers, the automaton can distinguish between isolated anomalous spikes and persistent compound contamination.

---

## 3. Dataset Context & Adaptation

### Dataset Source
- **Dataset:** *Water Quality* by MsSmartyPants (Kaggle).
- **Attributes:** 21 columns including concentrations of heavy metals (lead, arsenic, mercury, cadmium), biological contaminants (bacteria, viruses), minerals, and a ground-truth `is_safe` indicator.

### Bridging Continuous Data to Automata
Automata theory requires a discrete input alphabet $\Sigma$. Real-world sensors, however, produce continuous analogue or floating-point signals. 

This project bridges this gap using a **Sensor Abstraction / Discretization Layer**:
- **Chemical Thresholds:** Heavy metals are assessed against established World Health Organization (WHO) and EPA maximum contaminant limits. Exceeding thresholds flags a chemical hazard (`c`).
- **Biological Thresholds:** Bacterial and viral contamination indices are flagged when exceeding pathogen bounds, producing a biological hazard (`b`).
- **Compound Hazards:** When water exhibits both biological and toxic chemical contamination simultaneously, it yields an extreme hazard symbol (`x`).
- **Normal Operation:** Readings within all safe margins yield `0`.

---

## 4. Key Design Decisions

- **Why a DFA over an NFA?**
  Real-world control systems cannot sustain non-deterministic branching or simultaneous ambiguous states without risking safety hazards. A Deterministic Finite Automaton ensures one clear state at every instant.
- **Why an Accept State for Lockdown?**
  In language recognition, the set of accept states $F$ represents language acceptance. In our control model, language acceptance corresponds to detecting a **critical hazard sequence**, triggering automated lockdown and isolation protocols.
- **Recovery Mechanism:**
  The DFA includes recovery transitions ($q_1 \to q_0$, $q_2 \to q_0$, $q_3 \to q_0$) upon receiving clean flushing sequences (`0`), reflecting real-world flush and recalibration procedures.

---

## 5. Course & Submission Information

- **Course:** Formal Language and Automata (FLA) / Theory of Computation (TOC).
- **Core Topics Addressed:**
  - Regular Languages & Alphabet Definition ($\Sigma$).
  - Deterministic Finite Automata (DFA) 5-Tuple Formulation.
  - State Transition Functions ($\delta$) & State Transition Tables.
  - Simulation & Empirical Verification with Real-World Telemetry.
