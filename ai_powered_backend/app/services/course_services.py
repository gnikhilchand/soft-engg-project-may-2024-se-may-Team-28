from app import db
from app.models.course import Course


def get_all_courses(page=1, per_page=10, **filters):
    query = Course.query

    # Apply filters
    for key, value in filters.items():
        if hasattr(Course, key):
            query = query.filter(getattr(Course, key).like(f'%{value}%'))

    # Apply pagination
    courses_paginated = query.paginate(page, per_page, False)
    return courses_paginated.items, courses_paginated.total


def get_course(course_id):
    return Course.query.get(course_id)


def create_course(data):
    course = Course(title=data['title'], description=data.get('description'))
    db.session.add(course)
    db.session.commit()
    return course


def update_course(course_id, data):
    course = Course.query.get(course_id)
    if course is None:
        return None
    course.title = data['title']
    course.description = data.get('description')
    db.session.commit()
    return course


def delete_course(course_id):
    course = Course.query.get(course_id)
    if course is None:
        return False
    db.session.delete(course)
    db.session.commit()
    return True
