from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default=False)

    def __init__(self, name, mail, password, role):
        self.name = name
        self.mail = mail
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role

    def is_active(self):
        return True
    
    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'mail', 'role')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

class CourseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('books', lazy=True))

    def __init__(self, title, author, course_id):
        self.title = title
        self.author = author
        self.course_id = course_id

class AssignmentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'course_id')

Assignment_schema = AssignmentSchema()
Assignments_schema = AssignmentSchema(many=True)

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('borrows', lazy=True))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    assignment = db.relationship('Assignment', backref=db.backref('borrows', lazy=True))
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)

    def __init__(self, user_id, assignment_id, borrow_date, return_date):
        self.user_id = user_id
        self.assignment_id = assignment_id
        self.borrow_date = borrow_date
        self.return_date = return_date

class BorrowSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'assignment_id', 'borrow_date', 'return_date')

borrow_schema = BorrowSchema()
borrows_schema = BorrowSchema(many=True)

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #issued_to = db.Column(db.Integer, db.ForeignKey('borrow.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('issues', lazy=True))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    assignment = db.relationship('Assignment', backref=db.backref('issues', lazy=True))
    issue_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)

    def __init__(self, user_id, assignment_id, issue_date, return_date):
        self.user_id = user_id
        #self.issued_to = issued_to
        self.assignment_id = assignment_id
        self.issue_date = issue_date
        self.return_date = return_date

class IssueSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id','assignment_id', 'issue_date', 'return_date')

issue_schema = IssueSchema()
issues_schema = IssueSchema(many=True)