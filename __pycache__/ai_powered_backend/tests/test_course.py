import logging
import unittest
from app import create_app, db
from app.models.course import Course
from flask import json

class CourseTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test variables and initialize the app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.course_data = {
            'title': 'Test Course',
            'description': 'This is a test course'
        }

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_list_courses(self):
        """Test listing all courses."""
        try:
            with self.app.app_context():
                course = Course(**self.course_data)
                db.session.add(course)
                db.session.commit()

            response = self.client.get('/courses/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test Course', str(response.data))
        except Exception as e:
            logging.error("Error during test_list_courses: %s", e)
            raise

    def test_get_course_detail(self):
        """Test retrieving a single course by ID."""
        # First, create a course to retrieve
        with self.app.app_context():
            course = Course(**self.course_data)
            db.session.add(course)
            db.session.commit()
            course_id = course.id

        response = self.client.get(f'/courses/{course_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Course', str(response.data))

    def test_create_new_course(self):
        """Test creating a new course."""
        response = self.client.post('/courses/',
                                    data=json.dumps(self.course_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Course', str(response.data))

    def test_update_course_detail(self):
        """Test updating an existing course."""
        # First, create a course to update
        with self.app.app_context():
            course = Course(**self.course_data)
            db.session.add(course)
            db.session.commit()
            course_id = course.id

        update_data = {'title': 'Updated Test Course'}
        response = self.client.put(f'/courses/{course_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Test Course', str(response.data))

    def test_delete_course_detail(self):
        """Test deleting a course."""
        # First, create a course to delete
        with self.app.app_context():
            course = Course(**self.course_data)
            db.session.add(course)
            db.session.commit()
            course_id = course.id

        response = self.client.delete(f'/courses/{course_id}')
        self.assertEqual(response.status_code, 204)

        # Try to retrieve the deleted course
        response = self.client.get(f'/courses/{course_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
