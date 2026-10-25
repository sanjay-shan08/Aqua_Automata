import csv

# ==========================================
# PHASE 1 & 2: Formal Definitions & DFA
# ==========================================
# ALPHABET (Sigma):
# '0' = Safe / Normal
# 'b' = Biological hazard (Bacteria/Viruses)
# 'c' = Chemical hazard (Arsenic, Lead, Mercury)
# 'x' = Critical (Both Bio and Chem)

# STATES (Q):
# q0 = Ideal_Safe
# q1 = Bio_Warning
# q2 = Chem_Warning
# q3 = Lockdown_Critical

class WaterQualityDFA:
    def __init__(self):
        # 5-Tuple Definition
        self.states = {'q0', 'q1', 'q2', 'q3'}
        self.alphabet = {'0', 'b', 'c', 'x'}
        self.start_state = 'q0'
        self.accept_states = {'q3'} # q3 triggers the final critical alarm
        
        # State Transition Table (Delta)
        self.transitions = {
            'q0': {'0': 'q0', 'b': 'q1', 'c': 'q2', 'x': 'q3'},
            'q1': {'0': 'q0', 'b': 'q1', 'c': 'q3', 'x': 'q3'}, # Bio warning escalates to Critical if chem appears
            'q2': {'0': 'q0', 'b': 'q3', 'c': 'q2', 'x': 'q3'}, # Chem warning escalates to Critical if bio appears
            'q3': {'0': 'q0', 'b': 'q3', 'c': 'q3', 'x': 'q3'}  # Critical requires '0' (safe flush) to reset
        }
        
        self.current_state = self.start_state

    def reset(self):
        self.current_state = self.start_state

    def process_symbol(self, symbol):
        """Processes a single symbol and transitions to the next state."""
        if symbol not in self.alphabet:
            raise ValueError(f"Invalid symbol: {symbol}")
            
        prev_state = self.current_state
        self.current_state = self.transitions[self.current_state][symbol]
        return prev_state, self.current_state

    def process_string(self, input_string):
        """Processes a sequence of symbols over time."""
        print(f"--- Simulating Input String: '{input_string}' ---")
        for symbol in input_string:
            prev, new = self.process_symbol(symbol)
            print(f"Read '{symbol}' | {prev} --> {new}")
        
        if self.current_state in self.accept_states:
            print("ALERT: System ended in ACCEPT state (Lockdown Triggered!)\n")
        else:
            print("Status: System operational.\n")

# ==========================================
# PREPROCESSING: Dataset to Alphabet
# ==========================================
def discretize_water_data(csv_filepath, limit=20):
    """Reads the Kaggle dataset and converts continuous data into DFA alphabet symbols."""
    input_sequence = ""
    
    with open(csv_filepath, 'r') as file:
        reader = csv.DictReader(file)
        count = 0
        
        for row in reader:
            if count >= limit:
                break
                
            # Parse real world continuous values
            bacteria = float(row['bacteria'])
            viruses = float(row['viruses'])
            arsenic = float(row['arsenic'])
            lead = float(row['lead'])
            mercury = float(row['mercury'])
            
            # Define thresholds (WHO guidelines approx)
            bio_hazard = bacteria > 0.1 or viruses > 0.05
            chem_hazard = arsenic > 0.01 or lead > 0.01 or mercury > 0.002
            
            # Map to Alphabet
            if bio_hazard and chem_hazard:
                symbol = 'x'
            elif bio_hazard:
                symbol = 'b'
            elif chem_hazard:
                symbol = 'c'
            else:
                symbol = '0'
                
            input_sequence += symbol
            count += 1
            
    return input_sequence

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    print("Initializing Smart Sanitation Water Quality DFA...")
    dfa = WaterQualityDFA()
    
    # Generate the input string from the first 20 rows of our Kaggle dataset
    dataset_string = discretize_water_data('waterQuality1.csv', limit=20)
    
    print(f"Generated string from Dataset: {dataset_string}\n")
    
    # Simulate the DFA with the real-world string
    dfa.process_string(dataset_string)
