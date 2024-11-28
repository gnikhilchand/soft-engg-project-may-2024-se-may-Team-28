from flask import Blueprint, jsonify
from app.decorators import role_required
from flasgger import swag_from

mid_user_bp = Blueprint('mid_user_bp', __name__)


@mid_user_bp.route('/mid_user_protected', methods=['GET'])
@swag_from({
    'summary': 'Mid User Protected Route',
    'description': 'This route is protected and only accessible to users with the role of "mid_user".',
    'responses': {
        200: {
            'description': 'Success',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'This is a mid_user protected route'
                    }
                }
            }
        },
        401: {
            'description': 'Unauthorized'
        }
    }
})
@role_required('mid_user')
def mid_user_protected():
    return jsonify({"message": "This is a mid_user protected route"})
