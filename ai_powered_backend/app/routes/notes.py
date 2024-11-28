# from flask import Blueprint, request, jsonify
# from app.services.notes_service import generate_notes
#
# notes_bp = Blueprint('notes_bp', __name__)
#
#
# @notes_bp.route('/generate_notes', methods=['POST'])
# def generate_notes_route():
#     data = request.get_json()
#     topic = data.get('topic')
#     if not topic:
#         return jsonify({'error': 'Topic is required'}), 400
#
#     notes = generate_notes(topic)
#     return jsonify({'notes': notes})
