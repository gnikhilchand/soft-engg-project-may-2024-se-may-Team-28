from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    profile_picture = db.Column(db.String(256))
    bio = db.Column(db.Text)
    role = db.Column(db.String(20), nullable=False, default='user')

    # Relationships
    roles = db.relationship('UserRole', back_populates='user', lazy='dynamic')
    courses = db.relationship('UserCourse', back_populates='user', lazy='dynamic')
    feedbacks = db.relationship('Feedback', back_populates='user', lazy='dynamic')
    problem_solving = db.relationship('ProblemSolving', back_populates='user', lazy='dynamic')
    api_tokens = db.relationship('ApiToken', back_populates='user', lazy='dynamic')
    submissions = db.relationship('Submission', back_populates='user', lazy='dynamic')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', back_populates='roles')


class UserCourse(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='courses')
    course = db.relationship('Course', back_populates='users')


class ApiToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='api_tokens')

