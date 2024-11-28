from flask import Blueprint, request, jsonify
from app.services.summarization_services import summarize_transcript
from flasgger import swag_from

summary_bp = Blueprint('summary_bp', __name__, url_prefix="/api")


@summary_bp.route('/summarize', methods=['POST'])
@swag_from({
    'summary': 'Summarize Transcript',
    'description': 'This endpoint summarizes the provided transcript.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'transcript': {
                        'type': 'string',
                        'example': 'Enter the transcript text to be summarized.'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Transcript summarized successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'summary': {
                        'type': 'string',
                        'example': 'This is the summarized text of the transcript.'
                    }
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
                        'example': 'Transcript is required'
                    }
                }
            }
        }
    }
})
def summarize():
    data = request.get_json()
    transcript = data.get('transcript')
    if not transcript:
        return jsonify({'error': 'Transcript is required'}), 400

    summary = summarize_transcript(transcript)
    return jsonify({'summary': summary})
