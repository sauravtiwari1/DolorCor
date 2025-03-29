import matplotlib.pyplot as plt
from collections import defaultdict

# --- Hardcoded Symptom-Disease Matrix ---
# Represents whether a symptom is typically present (1) or absent (0) for a disease.
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
        # Note: Tuberculosis often has other specific symptoms like night sweats, weight loss, not listed here.
        # This matrix is based *only* on the provided table.
    },
    "Pneumonia": {
        "Fever": 1, "Cough": 1, "Fatigue": 1, "Sore throat": 0,
        "Shortness of breath": 1, "Runny nose": 0, "Body aches": 1,
        "Headache": 1, "Chills": 1, "Loss of taste/smell": 0
    }
}

# Extract all unique symptoms from the data
all_symptoms = set()
for symptoms in disease_symptom_data.values():
    all_symptoms.update(symptoms.keys())
all_symptoms = sorted(list(all_symptoms)) # Keep a consistent order

all_diseases = sorted(list(disease_symptom_data.keys()))

# --- Functions Adapted from the First Script ---

def calculate_disease_matches(user_symptoms, disease_data):
    """
    Counts how many user symptoms match each disease in the data.

    Args:
        user_symptoms: A list of validated symptoms provided by the user.
        disease_data: The dictionary holding disease-symptom relationships.

    Returns:
        A dictionary mapping disease names to their match count.
    """
    match_counts = defaultdict(int)
    for disease, symptoms_present in disease_data.items():
        count = 0
        for user_symptom in user_symptoms:
            if symptoms_present.get(user_symptom, 0) == 1: # Check if symptom is present (1)
                count += 1
        if count > 0: # Only include diseases with at least one match
             match_counts[disease] = count
    return dict(match_counts) # Convert back to regular dict

def print_symptom_disease_graph(user_symptoms, matched_diseases):
    """
    Prints the structure of a bipartite graph where edges exist
    if the symptom is associated with the disease in the data.

    Args:
        user_symptoms: List of strings representing the input symptoms (left nodes).
        matched_diseases: List of strings representing potential diseases (right nodes).
    """
    print("\n--- Bipartite Graph Structure (Symptoms vs. Diseases) ---")
    print("Input Symptoms (Left):", user_symptoms)
    print("Matched Diseases (Right):", matched_diseases)
    print("Edges (Symptom -> Disease):")

    # Print the edges based on symptom presence
    for symptom in user_symptoms:
        for disease in matched_diseases:
            # Check if the symptom is listed as present (1) for the disease
            if disease_symptom_data.get(disease, {}).get(symptom, 0) == 1:
                print(f"  ({symptom} -> {disease})")
    print("--- End of Graph Structure ---")


def visualize_symptom_disease_graph(user_symptoms, matched_diseases):
    """
    Visualizes a bipartite graph (using matplotlib) where edges exist
    if the symptom is associated with the disease.

    Args:
        user_symptoms: List of strings for the left column (symptoms).
        matched_diseases: List of strings for the right column (diseases).
    """
    if not user_symptoms or not matched_diseases:
        print("\nCannot visualize graph: No symptoms or matched diseases.")
        return

    plt.figure(figsize=(10, max(len(user_symptoms), len(matched_diseases)) * 0.8)) # Adjust height

    # x-coordinates for each side
    x_left, x_right = 0, 1

    # y-coordinates
    y_coords_left = range(len(user_symptoms))
    y_coords_right = range(len(matched_diseases))

    # Plot the user_symptoms on the left
    for i, symptom in enumerate(user_symptoms):
        plt.scatter(x_left, y_coords_left[i], color='blue', s=150, zorder=2)
        plt.text(x_left - 0.05, y_coords_left[i], symptom,
                 ha='right', va='center', fontsize=9)

    # Plot the matched_diseases on the right
    for j, disease in enumerate(matched_diseases):
        plt.scatter(x_right, y_coords_right[j], color='red', s=150, zorder=2)
        plt.text(x_right + 0.05, y_coords_right[j], disease,
                 ha='left', va='center', fontsize=9)

    # Draw edges based on symptom presence in the disease data
    for i, symptom in enumerate(user_symptoms):
        for j, disease in enumerate(matched_diseases):
             # Check if the symptom is listed as present (1) for the disease
            if disease_symptom_data.get(disease, {}).get(symptom, 0) == 1:
                plt.plot([x_left, x_right],
                         [y_coords_left[i], y_coords_right[j]],
                         color='gray', linewidth=1.0, zorder=1) # zorder=1 puts lines behind nodes

    # Formatting
    plt.xticks([])
    plt.yticks([])
    plt.xlim(-0.8, 1.8) # Adjust limits for text visibility
    plt.ylim(-1, max(len(y_coords_left), len(y_coords_right))) # Adjust y limits
    plt.title("Symptom-Disease Bipartite Graph")
    plt.tight_layout()
    plt.show()

def symptom_disease_demo():
    """Handles user input, calculates matches, prints, and visualizes."""
    print("--- Symptom Checker ---")
    print("Available symptoms:", ", ".join(all_symptoms))
    try:
        input_str = input("Enter your symptoms (comma-separated, case-sensitive): ")
        # Clean input: strip whitespace and handle potential empty strings
        raw_symptoms = [s.strip() for s in input_str.split(',') if s.strip()]

        if not raw_symptoms:
             print("No symptoms entered.")
             return

        # Validate symptoms
        user_symptoms = []
        invalid_symptoms = []
        for symptom in raw_symptoms:
            if symptom in all_symptoms:
                user_symptoms.append(symptom)
            else:
                invalid_symptoms.append(symptom)

        if invalid_symptoms:
            print(f"\nWarning: The following symptoms are not recognized: {', '.join(invalid_symptoms)}")

        if not user_symptoms:
            print("No valid symptoms provided. Cannot proceed.")
            return

        print(f"\nProcessing valid symptoms: {', '.join(user_symptoms)}")

        # Calculate disease matches
        disease_matches = calculate_disease_matches(user_symptoms, disease_symptom_data)

        if not disease_matches:
            print("\nNo diseases found matching the provided symptoms based on the available data.")
            return

        # Create prioritized list (priority queue simulation)
        # Sort by count (descending), then alphabetically by disease name (ascending) for ties
        prioritized_diseases = sorted(
            disease_matches.items(),
            key=lambda item: (-item[1], item[0]) # Sort by count DESC, then name ASC
        )

        print("\n--- Potential Diseases (Prioritized by Symptom Match Count) ---")
        for disease, count in prioritized_diseases:
            print(f"- {disease} (Matches {count} of your symptoms)")
        print("---")

        # Prepare lists for graphing
        matched_disease_names = [disease for disease, count in prioritized_diseases]

        # Print the graph structure to console
        print_symptom_disease_graph(user_symptoms, matched_disease_names)

        # Visualize the bipartite graph
        print("\nGenerating visualization...")
        visualize_symptom_disease_graph(user_symptoms, matched_disease_names)

    except Exception as e: # Catch potential errors during processing/plotting
        print(f"\nAn unexpected error occurred: {e}")
        print("Please ensure symptoms are entered correctly.")

# Run the demo
if __name__ == "__main__":
    symptom_disease_demo()