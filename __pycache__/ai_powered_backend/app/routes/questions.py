from flask import Blueprint, request, jsonify
from app.services.questions_service import generate_questions
from flasgger import swag_from

questions_bp = Blueprint('questions_bp', __name__, url_prefix="/api")


@questions_bp.route('/generate_questions', methods=['POST'])
@swag_from({
    'summary': 'Generate Questions from Text',
    'description': 'This endpoint generates questions from the provided text.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'example': 'Enter the text from which questions should be generated.'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Questions generated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'questions': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        }
                    }
                },
                'example': {
                    'questions': ['Question 1?', 'Question 2?', 'Question 3?']
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': 'Text is required'
                    }
                }
            }
        }
    }
})
def generate_questions_route():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    questions = generate_questions(text)
    return jsonify({'questions': questions})
