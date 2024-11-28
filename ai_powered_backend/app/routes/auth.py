from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from app.services.auth_service import register_user, authenticate_user, generate_token, verify_user, reset_password, update_password
from app import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=['POST'])
def signup():
    """
    User Signup
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: "john_doe"
            email:
              type: string
              example: "john.doe@example.com"
            password:
              type: string
              example: "password123"
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User created successfully. Please verify your email."
      400:
        description: Missing required fields
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Missing required fields"
      500:
        description: Error creating user
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error creating user"
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        user = register_user(username, email, password)
        return jsonify({'message': 'User created successfully. Please verify your email.'}), 201
    except Exception as e:
        current_app.logger.error(f"Error creating user: {e}")
        return jsonify({'message': 'Error creating user'}), 500


@bp.route('/login', methods=['POST'])
def login():
    """
    User Login
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: "john_doe"
            password:
              type: string
              example: "password123"
    responses:
      200:
        description: User authenticated successfully
        schema:
          type: object
          properties:
            token:
              type: string
              example: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
      400:
        description: Missing required fields
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Missing required fields"
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Invalid credentials"
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    user = authenticate_user(username, password)
    if user:
        token = generate_token(user.id)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        response_data = {

            'user': {

                'userid': user.id,

                'username': user.username,

                'email': user.email,

                'role': user.role,

                'last_visit': user.last_login.isoformat() if user.last_login else None

            },

            'token': token,

        }



        return jsonify(response_data), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    """
    Verify User Email
    ---
    parameters:
      - name: token
        in: path
        type: string
        required: true
        description: The verification token
    responses:
      200:
        description: Email verified successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Email verified successfully"
      400:
        description: Invalid or expired token
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Invalid or expired token"
    """
    try:
        verify_user(token)
        return jsonify({'message': 'Email verified successfully'}), 200
    except Exception as e:
        current_app.logger.error(f"Error verifying email: {e}")
        return jsonify({'message': 'Invalid or expired token'}), 400


@bp.route('/reset_password', methods=['POST'])
def reset_password_request():
    """
    Request Password Reset
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "john.doe@example.com"
    responses:
      200:
        description: Password reset instructions sent
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Password reset instructions sent to your email"
      400:
        description: Email is required
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Email is required"
      500:
        description: Error sending password reset email
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error sending password reset email"
    """
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    try:
        reset_password(email)
        return jsonify({'message': 'Password reset instructions sent to your email'}), 200
    except Exception as e:
        current_app.logger.error(f"Error sending password reset email: {e}")
        return jsonify({'message': 'Error sending password reset email'}), 500


@bp.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    """
    Reset Password
    ---
    parameters:
      - name: token
        in: path
        type: string
        required: true
        description: The password reset token
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            new_password:
              type: string
              example: "newpassword123"
    responses:
      200:
        description: Password has been reset successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Password has been reset successfully"
      400:
        description: Invalid or expired token
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Invalid or expired token"
    """
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'message': 'New password is required'}), 400

    try:
        update_password(token, new_password)
        return jsonify({'message': 'Password has been reset successfully'}), 200
    except Exception as e:
        current_app.logger.error(f"Error resetting password: {e}")
        return jsonify({'message': 'Invalid or expired token'}), 400
