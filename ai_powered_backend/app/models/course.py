from app import db
from datetime import datetime


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignments = db.relationship('Assignment', back_populates='course', lazy='dynamic')
    users = db.relationship('UserCourse', back_populates='course', lazy='dynamic')

    def __repr__(self):
        return f'<Course {self.title}>'


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course = db.relationship('Course', back_populates='assignments')
    submissions = db.relationship('Submission', back_populates='assignment', lazy='dynamic')
    feedbacks = db.relationship('Feedback', back_populates='assignment', lazy='dynamic')

    def __repr__(self):
        return f'<Assignment {self.title}>'


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(200), nullable=False)
    grade = db.Column(db.String(10))

    assignment = db.relationship('Assignment', back_populates='submissions')
    user = db.relationship('User', back_populates='submissions')

    def __repr__(self):
        return f'<Submission {self.id} by User {self.user_id}>'





