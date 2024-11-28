import jwt
from datetime import datetime, timedelta
from flask import current_app, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import db, mail
from app.models.user import User

SECRET_KEY = 'your_secret_key'
SECURITY_PASSWORD_SALT = 'your_security_password_salt'


def generate_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )


def register_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    # Generate and send verification email
    send_verification_email(user)
    return user


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


def send_verification_email(user):
    token = generate_verification_token(user.email)
    verify_url = url_for('auth.verify_email', token=token, _external=True)
    msg = Message('Verify Your Email', recipients=[user.email])
    msg.body = f'Please click the link to verify your email: {verify_url}'
    mail.send(msg)

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)


def verify_user(token):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt=SECURITY_PASSWORD_SALT, max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_active = True
            db.session.commit()
    except Exception:
        raise Exception('Invalid or expired token')


def reset_password(email):
    user = User.query.filter_by(email=email).first()
    if user:
        token = generate_reset_token(user.email)
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        msg = Message('Reset Your Password', recipients=[user.email])
        msg.body = f'Please click the link to reset your password: {reset_url}'
        mail.send(msg)


# app/services/auth_service.py
def update_password(token, new_password):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt=SECURITY_PASSWORD_SALT, max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
    except Exception:
        raise Exception('Invalid or expired token')

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)