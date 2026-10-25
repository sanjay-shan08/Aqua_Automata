# 🏛️ System Architecture

This document describes the architectural layout, data discretization pipeline, finite state machine design, and software components for the Automated Water Quality Monitoring System.

---

## 1. High-Level Architecture Overview

The system bridges continuous environmental telemetry with formal language processing. It is split into two primary layers:
1. **Perception & Discretization Layer:** Ingests multivariate sensor data, validates against biochemical thresholds, and encodes observations into discrete symbols.
2. **Automaton Engine (Control Layer):** Consumes the encoded sequence, executes deterministic state transitions, and enforces escalation/safety protocols.

```mermaid
flowchart TD
    subgraph Data_Source ["Data Telemetry Layer"]
        CSV[Kaggle Dataset: waterQuality1.csv]
        IoT[Continuous Sensor Readings]
    end

    subgraph Preprocessing ["Discretization & Encoding Layer"]
        Discretizer["discretize_water_data()"]
        Thresholds["WHO Safety Threshold Evaluator<br/>(Bacteria, Viruses, Arsenic, Lead, Mercury)"]
    end

    subgraph Automaton ["DFA Core Engine"]
        FSM["WaterQualityDFA<br/>(Q, Σ, δ, q0, F)"]
        TransitionEngine["State Transition Logic"]
    end

    subgraph Output ["Actuation & Observability Layer"]
        CLI["simulation_runner.py (CLI / ANSI Display)"]
        Lockdown["Accept State (q3): Safety Shutdown Protocol"]
    end

    CSV --> Discretizer
    IoT -.-> Discretizer
    Discretizer --> Thresholds
    Thresholds -->|"Symbol stream (0, b, c, x)"| FSM
    FSM --> TransitionEngine
    TransitionEngine --> CLI
    TransitionEngine -->|If state == q3| Lockdown
```

---

## 2. Discretization Engine Pipeline

The discretization component (`discretize_water_data`) reads continuous floating-point measurements and evaluates them according to safety rules:

```mermaid
flowchart TD
    Start([Row Sample Input]) --> Read[Read bacteria, viruses, arsenic, lead, mercury]
    Read --> CheckBio{"bacteria > 0.1 OR<br/>viruses > 0.05?"}
    Read --> CheckChem{"arsenic > 0.01 OR<br/>lead > 0.01 OR<br/>mercury > 0.002?"}

    CheckBio -->|Yes| BioTrue[bio_hazard = True]
    CheckBio -->|No| BioFalse[bio_hazard = False]

    CheckChem -->|Yes| ChemTrue[chem_hazard = True]
    CheckChem -->|No| ChemFalse[chem_hazard = False]

    BioTrue & ChemTrue -->|Both True| SymX["Emit 'x' (Compound Hazard)"]
    BioTrue & ChemFalse -->|Bio Only| SymB["Emit 'b' (Biological Hazard)"]
    BioFalse & ChemTrue -->|Chem Only| SymC["Emit 'c' (Chemical Hazard)"]
    BioFalse & ChemFalse -->|None| Sym0["Emit '0' (Safe / Normal)"]
```

---

## 3. Finite Automata State Transition Graph

The deterministic finite automaton operates on alphabet $\Sigma = \{0, b, c, x\}$ across states $Q = \{q_0, q_1, q_2, q_3\}$.

```mermaid
stateDiagram-v2
    direction LR

    [*] --> q0 : Start (q0)

    q0 --> q0 : '0' (Safe)
    q0 --> q1 : 'b' (Bio Warning)
    q0 --> q2 : 'c' (Chem Warning)
    q0 --> q3 : 'x' (Critical)

    q1 --> q0 : '0' (Flush / Recovery)
    q1 --> q1 : 'b' (Continued Bio)
    q1 --> q3 : 'c' or 'x' (Escalation to Lockdown)

    q2 --> q0 : '0' (Flush / Recovery)
    q2 --> q2 : 'c' (Continued Chem)
    q2 --> q3 : 'b' or 'x' (Escalation to Lockdown)

    q3 --> q0 : '0' (Manual / Full Safe Flush)
    q3 --> q3 : 'b', 'c', 'x' (Maintained Lockdown)
```

---

## 4. Software Component Design

### 4.1 `WaterQualityDFA` ([`water_quality_automaton.py`](file:///c:/Users/sanja/Desktop/Sanjay/ProCoded/FLA/water_quality_automaton.py))
- **`states`:** Python set containing $\{'q0', 'q1', 'q2', 'q3'\}$.
- **`alphabet`:** Set of permissible input tokens $\{'0', 'b', 'c', 'x'\}$.
- **`start_state`:** `'q0'`.
- **`accept_states`:** $\{'q3'\}$.
- **`transitions`:** Nested dictionary mapping $(q, \sigma) \to q'$ ensuring $O(1)$ constant time transition evaluations.
- **Methods:**
  - `reset()`: Resets `current_state` to `start_state`.
  - `process_symbol(symbol)`: Validates symbol against alphabet, executes transition, returns `(prev_state, new_state)`.
  - `process_string(input_string)`: Evaluates a sequence of symbols and checks acceptance.

### 4.2 `simulation_runner.py` ([`simulation_runner.py`](file:///c:/Users/sanja/Desktop/Sanjay/ProCoded/FLA/simulation_runner.py))
- **Terminal Presentation Layer:** Uses ANSI escape sequences to provide visual feedback for state transitions (`Safe`: Green, `Warning`: Yellow, `Lockdown`: Red).
- **Time Delay Simulation:** Integrates non-blocking artificial delays via `time.sleep` to mimic real-world IoT sensor sampling intervals.
- **Dataset Integration:** Seamlessly chains continuous CSV discretization into the discrete FSM engine.
