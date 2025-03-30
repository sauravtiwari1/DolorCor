from flask import Flask, render_template, request, jsonify
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from symptom_checker import (
    prime_to_symptom,
    disease_to_sqf,
    disease_action_plan,
    calculate_disease_matches_numeric,
    visualize_graph_numeric,
    sqf_to_disease
)

app = Flask(__name__)

@app.route('/')
def index():
    # Sort symptoms alphabetically for better UX
    symptoms = sorted(prime_to_symptom.values())
    symptom_primes = {symptom: prime for prime, symptom in prime_to_symptom.items()}
    return render_template('index.html', 
                         symptoms=symptoms, 
                         symptom_primes=symptom_primes)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        selected_primes = [int(prime) for prime in request.form.getlist('symptoms')]
        
        if not selected_primes:
            return jsonify({'error': 'Please select at least one symptom'}), 400

        # Calculate matches
        disease_matches = calculate_disease_matches_numeric(selected_primes, disease_to_sqf)
        prioritized_diseases = sorted(
            disease_matches.items(),
            key=lambda x: (-x[1], x[0])
        )

        # Generate plot
        plot_url = None
        if prioritized_diseases:
            matched_sqfs = [disease_to_sqf[d[0]] for d in prioritized_diseases]
            plt_obj = visualize_graph_numeric(
                selected_primes, 
                matched_sqfs, 
                prime_to_symptom, 
                sqf_to_disease
            )
            
            if plt_obj:
                img = BytesIO()
                plt_obj.savefig(img, format='png', bbox_inches='tight')
                plt_obj.close()
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        # Prepare results
        results = []
        for disease, count in prioritized_diseases:
            results.append({
                'name': disease,
                'count': count,
                'action': disease_action_plan.get(disease, disease_action_plan["Default"])
            })

        return render_template(
            'results.html',
            symptoms=[prime_to_symptom[p] for p in selected_primes],
            results=results,
            plot_url=plot_url
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 