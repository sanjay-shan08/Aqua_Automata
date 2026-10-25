import time
from water_quality_automaton import WaterQualityDFA, discretize_water_data

# ANSI Colors for beautiful CLI output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
CYAN = '\033[96m'

def print_state_transition(symbol, prev_state, current_state):
    """Helper function to print color-coded state transitions."""
    def colorize(state):
        if state == 'q0': return f"{GREEN}{state} (Safe){RESET}"
        if state == 'q1': return f"{YELLOW}{state} (Bio_Warning){RESET}"
        if state == 'q2': return f"{YELLOW}{state} (Chem_Warning){RESET}"
        if state == 'q3': return f"{RED}{state} (LOCKDOWN){RESET}"
        return state

    print(f"  [Sensor Input: {CYAN}{symbol}{RESET}] | Transition: {colorize(prev_state)} --> {colorize(current_state)}")

def run_scenario(name, test_string, dfa, speed=0.3):
    """Simulates real-time sensor data entering the automaton."""
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"SCENARIO: {name}")
    print(f"Data Stream: {test_string}")
    print(f"{CYAN}{'='*60}{RESET}")
    
    dfa.reset() # Important: Reset FSM back to q0 before each test
    
    for symbol in test_string:
        prev_raw = dfa.current_state
        _, curr_raw = dfa.process_symbol(symbol)
        print_state_transition(symbol, prev_raw, curr_raw)
        time.sleep(speed) # Simulates delay between sensor readings
        
    print("-" * 60)
    if dfa.current_state in dfa.accept_states:
        print(f"[!] FINAL STATUS: {RED}CRITICAL HAZARD DETECTED. SYSTEM LOCKDOWN INITIATED.{RESET}")
    else:
        print(f"[*] FINAL STATUS: {GREEN}WATER QUALITY WITHIN ACCEPTABLE PARAMETERS.{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

if __name__ == "__main__":
    import sys
    print(f"\n{CYAN}Initializing Smart Sanitation Automata Simulation...{RESET}")
    dfa = WaterQualityDFA()
    
    # ---------------------------------------------------------
    # TEST SUITE
    # ---------------------------------------------------------
    
    # Scenario 1: Perfectly safe water over time
    run_scenario("Normal Operation (Ideal Conditions)", "0000000", dfa, speed=0.2)
    
    # Scenario 2: Minor biological anomaly that clears up naturally
    run_scenario("Temporary Bio-Hazard & Recovery", "00b000", dfa, speed=0.3)
    
    # Scenario 3: Escalation (Bio warning followed immediately by Chem hazard)
    run_scenario("Compound Hazard Escalation", "00bcc", dfa, speed=0.4)
    
    # Scenario 4: Real data from the Kaggle dataset
    print(f"{YELLOW}Loading Kaggle Dataset...{RESET}")
    kaggle_string = discretize_water_data('waterQuality1.csv', limit=15)
    run_scenario("Kaggle Real-World Data Feed", kaggle_string, dfa, speed=0.2)
