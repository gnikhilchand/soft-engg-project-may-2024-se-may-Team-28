from flask import Blueprint, request, jsonify
import ast
from transformers import pipeline

# Create a blueprint
code_bp = Blueprint('code_bp', __name__)

# Load a Hugging Face model for code suggestions with GPU support (if available)
code_generation_pipeline = pipeline("text-generation", model="gpt2", device=0)  # Use device=0 for GPU

def evaluate_test_cases(code, test_cases):
    results = []
    for test_case in test_cases:
        input_data = test_case['input']
        expected_output = test_case['expected_output']

        # Prepare the local environment
        local_vars = {}
        exec(code, {'input_data': input_data}, local_vars)
        
        # Capture the result
        result = local_vars.get('result', None)
        results.append({
            'input': input_data,
            'expected_output': expected_output,
            'actual_output': result,
            'pass': result == expected_output
        })
    
    return results

def get_code_suggestions(code):
    # Generate code suggestions using the Hugging Face model
    suggestions = code_generation_pipeline(f"Suggest improvements for this code:\n{code}", max_length=150, truncation=True)
    return suggestions[0]['generated_text']

def analyze_code_complexity(code):
    # Simple heuristic to measure complexity based on the number of AST nodes
    tree = ast.parse(code)
    complexity = len(list(ast.walk(tree)))
    return complexity

@code_bp.route('/evaluate', methods=['POST'])
def evaluate_code():
    try:
        # Get the code and test cases from the request
        data = request.json
        code = data.get('code')
        test_cases = data.get('test_cases', [])

        # Evaluate test cases
        test_results = evaluate_test_cases(code, test_cases)

        # Analyze code complexity
        complexity = analyze_code_complexity(code)

        # Get AI-based code suggestions
        suggestions = get_code_suggestions(code)

        # Return the output as JSON
        return jsonify({
            'test_results': test_results,
            'complexity': complexity,
            'suggestions': suggestions
        }), 200
    except Exception as e:
        # Return error message if code execution fails
        return jsonify({'error': str(e)}), 400
