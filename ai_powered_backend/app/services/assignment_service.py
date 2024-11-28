from app import db
from app.models.course import Assignment


def get_all_assignments():
    return Assignment.query.all()


def get_assignment(assignment_id):
    return Assignment.query.get(assignment_id)


def create_assignment(data):
    assignment = Assignment(
        course_id=data['course_id'],
        title=data['title'],
        description=data.get('description'),
    )
    db.session.add(assignment)
    db.session.commit()
    return assignment


def update_assignment(assignment_id, data):
    assignment = Assignment.query.get(assignment_id)
    if assignment is None:
        return None
    assignment.title = data['title']
    assignment.description = data.get('description')
    db.session.commit()
    return assignment


def delete_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if assignment is None:
        return False
    db.session.delete(assignment)
    db.session.commit()
    return True
