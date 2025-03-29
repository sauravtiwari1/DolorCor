import matplotlib.pyplot as plt
from collections import defaultdict
import math
import datetime # Added for potential future use or logging, not strictly required by prompt

# --- Prime Number Generation Helper ---
def is_prime(num):
    """Checks if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(count):
    """Generates the first 'count' prime numbers."""
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

# --- Hardcoded Symptom-Disease Matrix ---
disease_symptom_data = {
    "Common Cold": {
        "Fever": 0, "Cough": 1, "Fatigue": 1, "Sore throat": 1,
        "Shortness of breath": 0, "Runny nose": 1, "Body aches": 1,
        "Headache": 1, "Chills": 0, "Loss of taste/smell": 0
    },
    "Influenza": {
        "Fever": 1, "Cough": 1, "Fatigue": 1, "Sore throat": 1,
        "Shortness of breath": 0, "Runny nose": 1, "Body aches": 1,
        "Headache": 1, "Chills": 1, "Loss of taste/smell": 0
    },
    "COVID-19": {
        "Fever": 1, "Cough": 1, "Fatigue": 1, "Sore throat": 1,
        "Shortness of breath": 1, "Runny nose": 0, "Body aches": 1,
        "Headache": 1, "Chills": 1, "Loss of taste/smell": 1
    },
    "Tuberculosis": {
        "Fever": 1, "Cough": 1, "Fatigue": 1, "Sore throat": 0,
        "Shortness of breath": 1, "Runny nose": 0, "Body aches": 0,
        "Headache": 0, "Chills": 1, "Loss of taste/smell": 0
    },
    "Pneumonia": {
        "Fever": 1, "Cough": 1, "Fatigue": 1, "Sore throat": 0,
        "Shortness of breath": 1, "Runny nose": 0, "Body aches": 1,
        "Headache": 1, "Chills": 1, "Loss of taste/smell": 0
    }
}

# --- Generate Mappings ---
# 1. Get unique symptoms and sort
all_symptoms = sorted(list(set(
    symptom for symptoms in disease_symptom_data.values() for symptom in symptoms.keys()
)))

# 2. Assign primes
required_primes = len(all_symptoms)
primes_list = generate_primes(required_primes)
symptom_to_prime = {symptom: primes_list[i] for i, symptom in enumerate(all_symptoms)}
prime_to_symptom = {prime: symptom for symptom, prime in symptom_to_prime.items()}

# 3. Calculate SQF for diseases
disease_to_sqf = {}
sqf_to_disease = defaultdict(list)
for disease, symptoms in disease_symptom_data.items():
    sqf_integer = 1
    for symptom, present in symptoms.items():
        if present == 1:
            prime = symptom_to_prime.get(symptom)
            if prime:
                 sqf_integer *= prime
    if sqf_integer > 0: # Only map if it has some representation
        disease_to_sqf[disease] = sqf_integer
        sqf_to_disease[sqf_integer].append(disease)

# --- Functions (Calculation, Printing, Visualization - Mostly unchanged) ---

def calculate_disease_matches_numeric(user_symptom_primes, disease_sqf_map):
    """Counts matches based on prime factors."""
    match_counts = defaultdict(int)
    if not user_symptom_primes:
        return {}
    for disease, disease_sqf in disease_sqf_map.items():
        count = sum(1 for prime in user_symptom_primes if disease_sqf % prime == 0)
        if count > 0:
            match_counts[disease] = count
    return dict(match_counts)

def print_graph_structure_numeric(user_primes, matched_sqfs, prime_map, sqf_map):
    """Prints the numeric graph structure with string labels."""
    print("\n--- Bipartite Graph Structure (Prime Factors) ---")
    print("Input Symptom Primes (Left):")
    for p in sorted(user_primes): # Sort for consistent output
        print(f"  {prime_map.get(p, 'Unknown')}: {p}")

    print("Matched Disease SQF Integers (Right):")
    for n in sorted(matched_sqfs): # Sort for consistent output
        disease_names = ", ".join(sqf_map.get(n, ['Unknown']))
        print(f"  {disease_names}: {n}")

    print("Edges (Prime Factor -> SQF Integer):")
    for p in sorted(user_primes): # Sort for consistent output
        symptom_name = prime_map.get(p, 'Unknown Prime')
        for n in sorted(matched_sqfs): # Sort for consistent output
            if n % p == 0:
                disease_names = ", ".join(sqf_map.get(n, ['Unknown Disease(s)']))
                print(f"  ({symptom_name} [{p}] -> {disease_names} [{n}])")
    print("--- End of Graph Structure ---")

def visualize_graph_numeric(user_primes, matched_sqfs, prime_map, sqf_map):
    """Visualizes the numeric bipartite graph with string labels."""
    if not user_primes or not matched_sqfs:
        print("\nCannot visualize graph: No valid symptom primes or matched disease SQFs.")
        return

    plot_primes = sorted(list(set(user_primes)))
    plot_sqfs = sorted(list(set(matched_sqfs)))

    plt.figure(figsize=(12, max(len(plot_primes), len(plot_sqfs)) * 0.9))
    x_left, x_right = 0, 1
    y_coords_left = {prime: i for i, prime in enumerate(plot_primes)}
    y_coords_right = {sqf: i for i, sqf in enumerate(plot_sqfs)}

    for prime, i in y_coords_left.items():
        label = f"{prime_map.get(prime, '?')} ({prime})"
        plt.scatter(x_left, i, color='blue', s=150, zorder=2)
        plt.text(x_left - 0.05, i, label, ha='right', va='center', fontsize=9)

    for sqf, j in y_coords_right.items():
        disease_names = ", ".join(sqf_map.get(sqf, ['?']))
        label = f"{disease_names} ({sqf})"
        plt.scatter(x_right, j, color='red', s=150, zorder=2)
        plt.text(x_right + 0.05, j, label, ha='left', va='center', fontsize=9)

    for p, i in y_coords_left.items():
        for n, j in y_coords_right.items():
            if n % p == 0:
                plt.plot([x_left, x_right], [i, j], color='gray', linewidth=1.0, zorder=1)

    plt.xticks([])
    plt.yticks([])
    plt.xlim(-1, 2)
    plt.ylim(-1, max(len(y_coords_left), len(y_coords_right)))
    plt.title("Symptom-Disease Bipartite Graph (Prime Factor Mapping)")
    plt.tight_layout()
    plt.show()

def print_mappings(prime_map, sqf_map):
    """Prints the complete mapping legends."""
    print("\n" + "="*40)
    print("          LEGEND / HASH MAP")
    print("="*40)

    print("\n--- Symptom Primes ---")
    # Sort by prime number for readability
    for prime, symptom in sorted(prime_map.items()):
        print(f"  {prime:<5} -> {symptom}")

    print("\n--- Disease Square-Free Integers (SQF) ---")
    # Sort by SQF number for readability
    for sqf, diseases in sorted(sqf_map.items()):
        # Join if multiple diseases share an SQF
        print(f"  {sqf:<7} -> {', '.join(diseases)}")
    print("="*40 + "\n") # Add extra newline for spacing before input prompt


# --- Main Demo Function ---
def symptom_disease_demo_numeric():
    """Handles prime input, calculates matches, prints results, vectors, graph, and legend."""
    print("--- Symptom Checker (Prime Number Input) ---")

    # --- Print the Legend at the Beginning ---
    print_mappings(prime_to_symptom, sqf_to_disease)

    # Variables to store final vectors
    final_input_vector = []
    final_output_vector = []

    try:
        # Now prompt for input after showing the legend
        input_str = input("Enter symptom prime numbers (comma-separated): ")
        raw_inputs = [s.strip() for s in input_str.split(',') if s.strip()]

        if not raw_inputs:
             print("No input provided.")
             return

        # Validate and convert to primes
        user_symptom_primes = []
        invalid_inputs = []
        valid_symptoms_found = []

        for val_str in raw_inputs:
            try:
                prime_candidate = int(val_str)
                if prime_candidate in prime_to_symptom:
                    if prime_candidate not in user_symptom_primes: # Ensure uniqueness
                        user_symptom_primes.append(prime_candidate)
                        valid_symptoms_found.append(prime_to_symptom[prime_candidate])
                else:
                    invalid_inputs.append(f"{prime_candidate} (Not a valid symptom prime)")
            except ValueError:
                invalid_inputs.append(f"'{val_str}' (Not an integer)")

        user_symptom_primes.sort() # Keep input vector sorted

        if invalid_inputs:
            print(f"\nWarning: The following inputs are invalid: {', '.join(invalid_inputs)}")

        if not user_symptom_primes:
            print("No valid symptom primes provided. Cannot proceed.")
            return # Exit if no valid input after warnings

        print(f"\nProcessing valid primes: {user_symptom_primes}")
        print(f"Corresponding symptoms: {', '.join(sorted(valid_symptoms_found))}")
        final_input_vector = list(user_symptom_primes) # Store for final output

        # Calculate disease matches
        disease_matches = calculate_disease_matches_numeric(user_symptom_primes, disease_to_sqf)

        if not disease_matches:
            print("\nNo diseases found whose SQF representation contains any of the input symptom primes.")
            final_output_vector = [] # Store empty list
        else:
            # Prioritize results
            prioritized_diseases = sorted(
                disease_matches.items(),
                key=lambda item: (-item[1], item[0])
            )

            print("\n--- Potential Diseases (Prioritized by Symptom Prime Factor Count) ---")
            for disease, count in prioritized_diseases:
                sqf = disease_to_sqf.get(disease, 'N/A')
                print(f"- {disease} (SQF: {sqf}, Matches {count} of your symptom primes)")
            print("---")

            # Prepare unique SQFs for graphing and final output vector
            matched_disease_sqfs = sorted(list(set(
                disease_to_sqf[name] for name, count in prioritized_diseases
            )))
            final_output_vector = list(matched_disease_sqfs) # Store for final output

            # Print the graph structure
            print_graph_structure_numeric(user_symptom_primes, matched_disease_sqfs, prime_to_symptom, sqf_to_disease)

            # Visualize the graph
            print("\nGenerating visualization...")
            visualize_graph_numeric(user_symptom_primes, matched_disease_sqfs, prime_to_symptom, sqf_to_disease)

        # --- Output Vectors (Printed before the end) ---
        print("\n" + "="*40)
        print("        INPUT/OUTPUT VECTORS")
        print("="*40)
        print(f"Input Vector (Symptom Primes): {final_input_vector}")
        print(f"Output Vector (Matched Disease SQFs): {final_output_vector}")
        print("="*40)


    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        # import traceback
        # traceback.print_exc() # Uncomment for detailed debugging
        print("Please check input format.")

    # --- Legend is no longer printed here ---

# --- Run the Demo ---
if __name__ == "__main__":
    symptom_disease_demo_numeric()