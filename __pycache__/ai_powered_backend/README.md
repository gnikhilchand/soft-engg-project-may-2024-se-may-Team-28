# AI-Powered Backend

## Overview

This project is an enterprise-level backend application developed using the Flask framework. It includes migration scripts to manage the database schema, test cases to ensure code reliability, and follows a structured blueprint-based routing system. It also uses multiple AI models that generate text summaries as well as suggestions.

## Features

- **Flask Backend**: RESTful API built using the Flask framework for efficient request handling and response generation.
- **Blueprints**: Modular structure with blueprints for managing different routes and functionalities.
- **Database Migrations**: Integrated with Flask-Migrate for seamless database migration management (upgrades/downgrades).
- **Testing**: Comprehensive test cases implemented using Pytest to validate the application's functionality.
- **Pagination and Search**: APIs support pagination and search functionalities for improved data handling and retrieval.
- **User Authentication**: OAuth2-based authentication system for secure user login and session management.

## Technologies Used

- **Backend**: Flask
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Migrations**: Flask-Migrate
- **Testing**: Pytest
- **Frontend**: Vue.js (for interactive web UI)
- **Cloud**: AWS, Firebase

## Installation

### Prerequisites

- Python 3.x
- Virtual Environment tool (e.g., `venv`)

### Setup

1. Clone the repository:
git clone https://github.com/its-animay/ai_powered_be.git
cd ai_powered_be

2. Create and activate a virtual environment:
python -m venv .venv
source .venv/bin/activate

3. Install the dependencies:
pip install -r requirements.txt

4. Set up the environment variables:
Create a `.env` file with the necessary configurations (e.g., database URL, secret keys).

5. Apply database migrations:
flask db upgrade

6. Run the application:
python run.py
Copy
## Database Migrations

To manage database migrations, use the following commands:

- Create a new migration:
flask db migrate -m "Migration message"

- Apply migrations:
flask db upgrade

- Rollback migrations:
flask db downgrade

## Running Tests

To run the test cases, execute the following command:
pytest
## API Endpoints

Here's a quick overview of the major API endpoints:

### Authentication
- `POST /auth/login`: User login
- `POST /auth/register`: User registration

### Courses
- `GET /courses`: Retrieve all courses (with pagination)
- `POST /courses`: Create a new course

### Users
- `GET /users/<id>`: Get user details
- `POST /user/course/registration`: Register a user to a course

## Contribution Guidelines

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Open a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

Special thanks to all the open-source libraries and contributors who made this project possible.