from flask import Blueprint, jsonify
from app.decorators import role_required
from flasgger import swag_from

superuser_bp = Blueprint('superuser_bp', __name__)


@superuser_bp.route('/superuser_protected', methods=['GET'])
@role_required('superuser')
@swag_from({
    'summary': 'Superuser Protected Route',
    'description': 'This endpoint is protected and can only be accessed by superusers.',
    'responses': {
        200: {
            'description': 'Access granted to superuser',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'This is a superuser protected route'
                    }
                }
            }
        },
        403: {
            'description': 'Forbidden - User does not have the required role',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Forbidden'
                    }
                }
            }
        }
    }
})
def superuser_protected():
    return jsonify({"message": "This is a superuser protected route"})
