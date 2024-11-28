import unittest
import json
from app import create_app, db
from app.models.course import Assignment

class AssignmentsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test client and database."""
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Tear down database and app context."""
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Set up test data."""
        self.assignment_data = {
            'course_id': 1,
            'title': 'Test Assignment',
            'description': 'This is a test assignment'
        }

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()

    def test_create_new_assignment(self):
        """Test creating a new assignment."""
        response = self.client.post('/assignments/',
                                    data=json.dumps(self.assignment_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['title'], self.assignment_data['title'])
        self.assertEqual(response.json['description'], self.assignment_data['description'])

    def test_delete_assignment_detail(self):
        """Test deleting an assignment."""
        # Create an assignment to delete
        with self.app.app_context():
            assignment = Assignment(
                course_id=1,
                title='Test Assignment',
                description='This is a test assignment'
            )
            db.session.add(assignment)
            db.session.commit()
            assignment_id = assignment.id

        response = self.client.delete(f'/assignments/{assignment_id}')
        self.assertEqual(response.status_code, 204)

        # Verify the assignment has been deleted
        response = self.client.get(f'/assignments/{assignment_id}')
        self.assertEqual(response.status_code, 404)

    def test_get_assignment_detail(self):
        """Test retrieving a single assignment by ID."""
        # Create an assignment to retrieve
        with self.app.app_context():
            assignment = Assignment(
                course_id=1,
                title='Test Assignment',
                description='This is a test assignment'
            )
            db.session.add(assignment)
            db.session.commit()
            assignment_id = assignment.id

        response = self.client.get(f'/assignments/{assignment_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Test Assignment')
        self.assertEqual(response.json['description'], 'This is a test assignment')

    def test_list_assignments(self):
        """Test listing all assignments."""
        # Create an assignment first to ensure the list is not empty
        with self.app.app_context():
            assignment = Assignment(
                course_id=1,
                title='Test Assignment',
                description='This is a test assignment'
            )
            db.session.add(assignment)
            db.session.commit()

        response = self.client.get('/assignments/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)

    def test_update_assignment_detail(self):
        """Test updating an existing assignment."""
        # Create an assignment to update
        with self.app.app_context():
            assignment = Assignment(
                course_id=1,
                title='Old Title',
                description='Old Description'
            )
            db.session.add(assignment)
            db.session.commit()
            assignment_id = assignment.id

        updated_data = {
            'title': 'Updated Title',
            'description': 'Updated Description'
        }
        response = self.client.put(f'/assignments/{assignment_id}',
                                  data=json.dumps(updated_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Updated Title')
        self.assertEqual(response.json['description'], 'Updated Description')

if __name__ == '__main__':
    unittest.main()
