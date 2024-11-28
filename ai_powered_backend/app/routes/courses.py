from flask import Blueprint, request, jsonify
from app import db
from app.models import course
from app.schema.course import CourseSchema
from app.services.course_services import create_course, update_course, delete_course, get_all_courses, get_course
from flasgger import Swagger, swag_from

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

@courses_bp.route('/', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'description': 'Page number for pagination',
            'required': False
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'description': 'Number of items per page',
            'required': False
        },
        {
            'name': 'title',
            'in': 'query',
            'type': 'string',
            'description': 'Filter courses by title',
            'required': False
        },
        {
            'name': 'description',
            'in': 'query',
            'type': 'string',
            'description': 'Filter courses by description',
            'required': False
        }
    ],
    'responses': {
        200: {
            'description': 'A list of all courses with pagination and filtering',
            'schema': {
                'type': 'object',
                'properties': {
                    'total': {
                        'type': 'integer',
                        'description': 'Total number of courses'
                    },
                    'courses': {
                        'type': 'array',
                        'items': {
                            '$ref': '#/definitions/Course'
                        }
                    }
                }
            }
        }
    }
})
def list_courses():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    title_filter = request.args.get('title')
    description_filter = request.args.get('description')

    filters = {}
    if title_filter:
        filters['title'] = title_filter
    if description_filter:
        filters['description'] = description_filter

    courses, total = get_all_courses(page=page, per_page=per_page, **filters)
    return jsonify({'total': total, 'courses': courses_schema.dump(courses)}), 200

@courses_bp.route('/<int:id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the course to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'The course details',
            'schema': {
                '$ref': '#/definitions/Course'
            }
        },
        404: {
            'description': 'Course not found'
        }
    }
})
def get_course_detail(id):
    course = get_course(id)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course_schema.dump(course)), 200

@courses_bp.route('/', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                '$ref': '#/definitions/Course'
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Course created successfully',
            'schema': {
                '$ref': '#/definitions/Course'
            }
        }
    }
})
def create_new_course():
    data = request.get_json()
    course = create_course(data)
    return jsonify(course_schema.dump(course)), 201

@courses_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the course to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                '$ref': '#/definitions/Course'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Course updated successfully',
            'schema': {
                '$ref': '#/definitions/Course'
            }
        },
        404: {
            'description': 'Course not found'
        }
    }
})
def update_course_detail(id):
    data = request.get_json()
    course = update_course(id, data)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course_schema.dump(course)), 200

@courses_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the course to delete'
        }
    ],
    'responses': {
        204: {
            'description': 'Course deleted successfully'
        },
        404: {
            'description': 'Course not found'
        }
    }
})
def delete_course_detail(id):
    success = delete_course(id)
    if not success:
        return jsonify({"error": "Course not found"}), 404
    return jsonify({"message": "Course deleted successfully"}), 204


