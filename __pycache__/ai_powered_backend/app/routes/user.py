from datetime import datetime
import json
import logging
from app.models.course import Assignment, Course
from flask import request
import requests
from app.models.user import User, UserCourse
from flask import Blueprint, jsonify
from app.decorators import role_required
from flasgger import swag_from
from app import db
from sqlalchemy.orm import class_mapper

user_bp = Blueprint('user_bp', __name__)

logging.basicConfig(level=logging.DEBUG)

@user_bp.route('/user_protected', methods=['GET'])
@role_required('user')
@swag_from({
    'summary': 'User Protected Route',
    'description': 'This endpoint is protected and can only be accessed by users with the user role.',
    'responses': {
        200: {
            'description': 'Access granted to user',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'This is a user protected route'
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
def user_protected():
    return jsonify({"message": "This is a user protected route"})

@user_bp.route('/api/users', methods=['GET'])
def get_users():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Filters
    username_filter = request.args.get('username')
    email_filter = request.args.get('email')
    role_filter = request.args.get('role')

    # Query active users based on filters
    query = User.query.filter_by(is_active=True)  # Only active users

    if username_filter:
        query = query.filter(User.username.ilike(f'%{username_filter}%'))
    if email_filter:
        query = query.filter(User.email.ilike(f'%{email_filter}%'))
    if role_filter:
        query = query.filter(User.role == role_filter)

    # Pagination
    users = query.paginate(page=page, per_page=per_page)

    # Preparing the response data
    users_data = []
    for user in users.items:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'last_login': user.last_login.isoformat() if user.last_login else None, 
            'created_at': user.created_at.isoformat(),
            'profile_picture': user.profile_picture,
            'bio': user.bio
        })

    return jsonify({
        'users': users_data,
        'total_users': users.total,
        'current_page': users.page,
        'per_page': users.per_page,
        'total_pages': users.pages
    }), 200

# Get user by id
@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'bio': user.bio,
        'role': user.role,
        'is_active': user.is_active,
        'last_login': user.last_login,
        'created_at': user.created_at,
        'profile_picture': user.profile_picture
    }
    return jsonify(user_data), 200

# Update user
@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'bio' in data:
        user.bio = data['bio']
    if 'profile_picture' in data:
        user.profile_picture = data['profile_picture']
    if 'role' in data:
        user.role = data['role']
    if 'is_active' in data:
        user.is_active = data['is_active']

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200

# Delete user
@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def soft_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = False  # Mark user as inactive                                     
    db.session.commit()

    return jsonify({'message': 'User marked as inactive'}), 200



def serialize_datetime(dt):
    return dt.isoformat() if dt else None

@user_bp.route('/dashboard/<int:user_id>/details', methods=['GET'])
def get_user_details(user_id):
    user = User.query.get_or_404(user_id)
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': serialize_datetime(user.created_at),
        'is_active': user.is_active,
        'last_login': serialize_datetime(user.last_login),
        'profile_picture': user.profile_picture,
        'bio': user.bio,
        'role': user.role,
        'courses': []
    }
    
    for user_course in user.courses:
        course = user_course.course
        course_data = {
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'created_at': serialize_datetime(course.created_at),
            'updated_at': serialize_datetime(course.updated_at),
            'assignments': []
        }
        
        for assignment in course.assignments:
            assignment_data = {
                'id': assignment.id,
                'title': assignment.title,
                'description': assignment.description,
                'due_date': serialize_datetime(assignment.due_date),
                'created_at': serialize_datetime(assignment.created_at),
                'updated_at': serialize_datetime(assignment.updated_at)
            }
            course_data['assignments'].append(assignment_data)
        
        user_data['courses'].append(course_data)
    
    return jsonify(user_data), 200


@user_bp.route('/user/course/registration', methods=['POST'])
def create_user_course():
    data = request.get_json()

    user_id = data.get('user_id')
    course_id = data.get('course_id')

    # Check if the user and course exist
    if not User.query.get(user_id):
        return jsonify({"error": "User not found"}), 404
    if not Course.query.get(course_id):
        return jsonify({"error": "Course not found"}), 404

    # Create and save the user-course association
    user_course = UserCourse(user_id=user_id, course_id=course_id, joined_at=datetime.utcnow())
    db.session.add(user_course)
    db.session.commit()

    return jsonify({
        "user_id": user_course.user_id,
        "course_id": user_course.course_id,
        "joined_at": user_course.joined_at.isoformat()
    }), 201