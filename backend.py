# --- Dependencies ---
from collections import defaultdict
import math
import sys # To check if matplotlib was successfully imported

# Attempt to import matplotlib for visualization
try:
    import matplotlib.pyplot as plt
    matplotlib_available = True
except ImportError:
    matplotlib_available = False
    print("Warning: matplotlib not found. Graph visualization will be skipped.")
    print("Install using: pip install matplotlib")

# --- Prime Number Generation Helper ---
# (Kept as is)
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

# --- Symptom-Disease Data - MIXED COMMON & RARE DISEASES ---
# (Kept as is from the previous version)
disease_symptom_data_optimized = {
    # --- Common Diseases ---
    "Common Cold": {"Cough", "Sore throat", "Runny nose", "Sneezing", "Fatigue"},
    "Influenza": {"Fever", "Cough", "Sore throat", "Runny nose", "Body aches", "Fatigue", "Headache", "Chills"},
    "Strep Throat": {"Fever", "Sore throat", "Headache", "Swollen Tonsils", "Fatigue", "Nausea"},
    "Seasonal Allergies": {"Runny nose", "Sneezing", "Itchy eyes", "Cough"},

    # --- Rare Diseases ---
    "Acute Intermittent Porphyria (AIP)": {"Severe abdominal pain", "Nausea", "Muscle weakness", "Confusion", "Anxiety", "Tachycardia"},
    "Creutzfeldt-Jakob Disease (CJD)": {"Rapid cognitive decline", "Memory loss", "Myoclonus", "Ataxia", "Confusion", "Visual disturbances"},
    "Fibrodysplasia Ossificans Progressiva (FOP)": {"Malformed great toe", "Localized painful swelling", "Reduced joint mobility", "Difficulty breathing"},
    "Fatal Familial Insomnia (FFI)": {"Progressive severe insomnia", "Panic attacks", "Hallucinations", "Ataxia", "Memory loss", "Autonomic dysfunction"},
    "Guillain-Barré Syndrome (GBS)": {"Muscle weakness", "Tingling in extremities", "Unsteady walk (Ataxia)", "Difficulty breathing", "Autonomic dysfunction", "Pain"},

    # --- Another common illness for context ---
    "Gastroenteritis (Stomach Flu)": {"Nausea", "Vomiting", "Diarrhea", "Abdominal pain", "Fever", "Headache"}
}

# --- Action Plan Data ---
# Provides generic, non-diagnostic suggestions. Emphasizes professional consultation.
disease_action_plan = {
    "Common Cold": "Action: Rest, stay hydrated, use over-the-counter remedies for symptom relief if needed. Consult a doctor if symptoms worsen, are severe, or persist beyond 10-14 days.",
    "Influenza": "Action: Consult a healthcare professional promptly for potential diagnosis and antiviral treatment, especially if in a high-risk group. Rest, fluids, and fever management are crucial.",
    "Strep Throat": "Action: See a doctor for a rapid strep test or throat culture. Antibiotics are usually required if positive. Complete the full course if prescribed.",
    "Seasonal Allergies": "Action: Identify and avoid triggers if possible. Over-the-counter antihistamines or nasal sprays may help. Consult a doctor or allergist for persistent or severe symptoms.",
    "Gastroenteritis (Stomach Flu)": "Action: Focus on hydration (small sips of clear fluids). Rest. Gradually reintroduce bland foods. Seek medical attention if dehydration, high fever, severe pain, or bloody stools occur.",

    # Rare/Serious Conditions - Emphasize Urgency
    "Acute Intermittent Porphyria (AIP)": "Action: This possibility requires URGENT medical evaluation by a healthcare professional, potentially in an emergency setting, for diagnosis and management.",
    "Creutzfeldt-Jakob Disease (CJD)": "Action: These symptoms require URGENT specialist neurological evaluation. Consult a healthcare professional immediately.",
    "Fibrodysplasia Ossificans Progressiva (FOP)": "Action: Requires specialist consultation (e.g., geneticist, rheumatologist) for diagnosis and management plan. Avoid trauma/injections if suspected.",
    "Fatal Familial Insomnia (FFI)": "Action: These symptoms require URGENT specialist neurological and sleep evaluation. Consult a healthcare professional immediately.",
    "Guillain-Barré Syndrome (GBS)": "Action: This possibility requires URGENT medical evaluation, often in a hospital setting, due to potential for rapid progression and breathing issues.",

    # Default Action
    "Default": "Action: Consult a healthcare professional for an accurate diagnosis and appropriate treatment plan."
}


# --- Generate Mappings ---
# (Calculations kept as is)
all_symptoms = sorted(list(set(
    symptom for symptoms_set in disease_symptom_data_optimized.values() for symptom in symptoms_set
)))
required_primes = len(all_symptoms)
primes_list = generate_primes(required_primes)
symptom_to_prime = {symptom: primes_list[i] for i, symptom in enumerate(all_symptoms)}
prime_to_symptom = {prime: symptom for symptom, prime in symptom_to_prime.items()}

disease_to_sqf = {}
sqf_to_disease = defaultdict(list)
for disease, symptoms_set in disease_symptom_data_optimized.items():
    sqf_integer = 1
    for symptom in symptoms_set:
        prime = symptom_to_prime.get(symptom)
        if prime:
            sqf_integer *= prime
    disease_to_sqf[disease] = sqf_integer
    sqf_to_disease[sqf_integer].append(disease)


# --- Functions ---

def calculate_disease_matches_numeric(user_symptom_primes, disease_sqf_map):
    # (Kept as is)
    match_counts = defaultdict(int)
    if not user_symptom_primes:
        return {}
    for disease, disease_sqf in disease_sqf_map.items():
        count = 0
        for prime in user_symptom_primes:
            if disease_sqf % prime == 0:
                count += 1
        if count > 0:
            match_counts[disease] = count
    return dict(match_counts)

# (Text-based print_graph_structure_numeric is no longer called, replaced by visualize)

def print_mappings(prime_map, sqf_map):
    # (Kept as is, adjusted spacing)
    print("\n" + "="*70) # Wider for longer names
    print("                    LEGEND / HASH MAP (Rare Diseases Included)")
    print("="*70)
    print("\n--- Symptom Primes ---")
    max_symptom_len = max(len(s) for s in prime_map.values()) if prime_map else 10
    items_per_line = 2 # Adjust as needed for screen width
    sorted_symptoms = sorted(prime_map.items())
    for i in range(0, len(sorted_symptoms), items_per_line):
        line = ""
        for j in range(items_per_line):
            if i + j < len(sorted_symptoms):
                prime, symptom = sorted_symptoms[i+j]
                line += f"  {prime:<5} -> {symptom:<{max_symptom_len}}  "
        print(line)

    print("\n--- Disease Square-Free Integers (SQF) ---")
    max_disease_len = max(len(d) for diseases in sqf_map.values() for d in diseases) if sqf_map else 20
    for sqf, diseases in sorted(sqf_map.items()):
         # Ensure disease names wrap reasonably if multiple share an SQF
        disease_str = f"{', '.join(diseases)}"
        print(f"  {sqf:<15} -> {disease_str}")
    print("="*70 + "\n")

# --- NEW Visualization Function ---
def visualize_graph_numeric(user_primes, matched_sqfs, prime_map, sqf_map):
    """Visualizes the numeric bipartite graph with string labels using matplotlib."""
    if not matplotlib_available:
         print("\nVisualization unavailable (matplotlib not installed).")
         return
    if not user_primes or not matched_sqfs:
        print("\nCannot visualize graph: No valid symptoms provided or no matches found.")
        return

    plt.figure(figsize=(14, max(len(user_primes), len(matched_sqfs)) * 0.8 + 1)) # Adjusted size
    x_left, x_right = 0, 1

    # Ensure uniqueness and sorting for consistent plotting
    plot_primes = sorted(list(set(user_primes)))
    plot_sqfs = sorted(list(set(matched_sqfs)))

    # Calculate y-coordinates to space nodes evenly
    y_coords_left = {prime: i for i, prime in enumerate(plot_primes)}
    y_coords_right = {sqf: i for i, sqf in enumerate(plot_sqfs)}

    max_y = max(len(y_coords_left), len(y_coords_right))

    # Plot symptom nodes (left)
    for prime, i in y_coords_left.items():
        label = f"{prime_map.get(prime, '?')} ({prime})"
        plt.scatter(x_left, i, color='skyblue', s=300, zorder=3, edgecolors='black')
        plt.text(x_left - 0.02, i, label, ha='right', va='center', fontsize=9)

    # Plot disease nodes (right)
    for sqf, j in y_coords_right.items():
        # Join if multiple diseases share an SQF
        disease_names = "\n".join(sqf_map.get(sqf, ['?'])) # Use newline for multiples
        label = f"{disease_names}\n(SQF: {sqf})"
        plt.scatter(x_right, j, color='lightcoral', s=300, zorder=3, edgecolors='black')
        plt.text(x_right + 0.02, j, label, ha='left', va='center', fontsize=9)

    # Plot edges (connections)
    for p, i in y_coords_left.items():
        for n, j in y_coords_right.items():
            if n % p == 0: # Check divisibility for connection
                plt.plot([x_left, x_right], [i, j], color='grey', linewidth=1.0, zorder=1, alpha=0.7)

    plt.xticks([])
    plt.yticks([])
    plt.xlim(-0.5, 1.5) # Give more horizontal space for labels
    plt.ylim(-1, max_y)
    plt.title("Symptom (Prime) -> Disease (SQF) Connections", fontsize=14)
    plt.xlabel("Input Symptoms                      Potential Conditions", labelpad=10)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent title overlap
    plt.show()


# --- Main Demo Function (Enhanced with Loop, Graphics, Action Plan) ---
def symptom_disease_demo_numeric():
    """Handles prime input, calculates matches, prints results, vectors, action plans, graph, and offers restart."""
    print("="*70)
    print("          Symptom Checker (Prime Number Mapping - Demo)")
    print("              Includes Common and RARE Disease Data")
    print("="*70)
    print("\n*** DISCLAIMER ***")
    print("This tool is for informational and demonstrational purposes ONLY.")
    print("It is NOT a substitute for professional medical advice, diagnosis, or treatment.")
    print("ALWAYS seek the advice of your physician or other qualified health provider")
    print("with any questions you may have regarding a medical condition.")
    print("NEVER disregard professional medical advice or delay in seeking it")
    print("because of something you have read or interpreted from this tool.")
    print("If you think you may have a medical emergency, call your doctor,")
    print("go to the emergency department, or call 911 immediately.")
    print("="*70)

    # Print the Legend only once at the start
    print_mappings(prime_to_symptom, sqf_to_disease)

    # --- Main Loop for Restart ---
    while True:
        final_input_vector = []
        final_output_vector = []
        valid_symptoms_found = [] # Reset for each run

        try:
            print("-" * 70)
            input_str = input("Enter symptom prime numbers (comma-separated, e.g., 2, 5, 11): ")
            raw_inputs = [s.strip() for s in input_str.split(',') if s.strip()]

            if not raw_inputs:
                  print("No input provided.")
                  # Ask to restart or exit here as well
                  if input("\nTry again? (yes/no): ").strip().lower() != 'yes':
                      break
                  else:
                      continue # Go to next iteration of the while loop


            # Validate and convert to primes
            user_symptom_primes = []
            invalid_inputs = []

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
                print("No valid symptom primes provided. Cannot proceed with analysis.")
                if input("\nTry again? (yes/no): ").strip().lower() != 'yes':
                    break
                else:
                    continue

            print(f"\nProcessing symptoms: {', '.join(sorted(valid_symptoms_found))}")
            print(f"Corresponding prime numbers: {user_symptom_primes}")
            final_input_vector = list(user_symptom_primes)

            # Calculate disease matches
            disease_matches = calculate_disease_matches_numeric(user_symptom_primes, disease_to_sqf)

            if not disease_matches:
                print("\nBased on the input symptoms, no matching conditions were found in the dataset.")
                final_output_vector = []
            else:
                # Prioritize results
                prioritized_diseases = sorted(
                    disease_matches.items(),
                    key=lambda item: (-item[1], item[0]) # Sort by count desc, then name asc
                )

                # --- Output Section ---
                print("\n" + "="*70)
                print("                          RESULTS & ACTIONS")
                print("="*70)

                # 1. Sentence Summary
                symptom_names_str = ", ".join(sorted(valid_symptoms_found))
                disease_names_str = ", ".join([d[0] for d in prioritized_diseases])
                print(f"\nBased on the symptoms: {symptom_names_str}")
                print(f"Potential conditions to discuss with a healthcare professional include: {disease_names_str}.\n")
                print("--- Details & Suggested Actions (Not Medical Advice) ---")

                # 2. Prioritized List with Action Plans
                for disease, count in prioritized_diseases:
                    sqf = disease_to_sqf.get(disease, 'N/A')
                    # Fetch action plan, use Default if specific one not found
                    action = disease_action_plan.get(disease, disease_action_plan["Default"])
                    print(f"\n* {disease}")
                    print(f"  Matches {count} symptom(s) (SQF: {sqf})")
                    print(f"  {action}")
                print("---")

                # Prepare for visualization / text graph structure
                matched_disease_sqfs = sorted(list(set(
                    disease_to_sqf[name] for name, count in prioritized_diseases
                )))
                final_output_vector = list(matched_disease_sqfs)

                # 3. Graphical Visualization
                if matplotlib_available:
                    try:
                        print("\nGenerating connections graph...")
                        # Make sure all variables are passed correctly
                        visualize_graph_numeric(user_symptom_primes, matched_disease_sqfs, prime_to_symptom, sqf_to_disease)
                    except Exception as e:
                        print(f"\nError generating visualization: {e}")
                        print("(Check if your display environment supports matplotlib)")
                else:
                    # Fallback text graph if matplotlib is missing (Optional, can be removed)
                    # print_graph_structure_numeric(user_symptom_primes, matched_disease_sqfs, prime_to_symptom, sqf_to_disease)
                    pass # Or just do nothing if visualization is the only goal


            # 4. Output Vectors (Less prominent now)
            # print("\n--- Technical Details ---")
            # print(f"Input Vector (Symptom Primes): {final_input_vector}")
            # print(f"Output Vector (Matched Disease SQFs): {final_output_vector}")
            # print("---")


        except Exception as e:
            print(f"\nAn unexpected error occurred during processing: {e}")
            # import traceback # Keep commented out unless debugging
            # traceback.print_exc()
            print("Please check input format and try again.")

        # --- Restart Prompt ---
        print("-" * 70)
        restart = input("\nAnalyze another set of symptoms? (yes/no): ").strip().lower()
        if restart != 'yes':
            print("\nExiting symptom checker. Remember this is not medical advice.")
            break # Exit the while loop

# --- Run the Demo ---
if __name__ == "__main__":
    symptom_disease_demo_numeric()