from flask import Blueprint, request, jsonify
from app import db
from flask_cors import CORS
from app.models import course
from app.schema.assignment import AssignmentSchema
from app.services.assignment_service import create_assignment, update_assignment, delete_assignment, get_all_assignments, get_assignment

assignments_bp = Blueprint('assignments', __name__)
assignment_schema = AssignmentSchema()
assignments_schema = AssignmentSchema(many=True)
CORS(assignments_bp)


@assignments_bp.route('/', methods=['GET'])
def list_assignments():
    """
    List all assignments
    ---
    responses:
      200:
        description: A list of assignments
        schema:
          type: array
          items:
            $ref: '#/definitions/Assignment'
    """
    assignments = get_all_assignments()
    return jsonify(assignments_schema.dump(assignments)), 200

@assignments_bp.route('/<int:id>', methods=['GET'])
def get_assignment_detail(id):
    """
    Get assignment detail
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The assignment ID
    responses:
      200:
        description: The assignment detail
        schema:
          $ref: '#/definitions/Assignment'
      404:
        description: Assignment not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: Assignment not found
    """
    assignment = get_assignment(id)
    if assignment is None:
        return jsonify({"error": "Assignment not found"}), 404
    return jsonify(assignment_schema.dump(assignment)), 200

@assignments_bp.route('/', methods=['POST'])
def create_new_assignment():
    """
    Create a new assignment
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            due_date:
              type: string
              format: date-time
    responses:
      201:
        description: Assignment created
        schema:
          $ref: '#/definitions/Assignment'
    """
    data = request.get_json()
    assignment = create_assignment(data)
    return assignment_schema.dump(assignment), 201

@assignments_bp.route('/<int:id>', methods=['PUT'])
def update_assignment_detail(id):
    """
    Update an assignment
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The assignment ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            due_date:
              type: string
              format: date-time
    responses:
      200:
        description: Assignment updated
        schema:
          $ref: '#/definitions/Assignment'
      404:
        description: Assignment not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: Assignment not found
    """
    data = request.get_json()
    assignment = update_assignment(id, data)
    if assignment is None:
        return jsonify({"error": "Assignment not found"}), 404
    return assignment_schema.dump(assignment), 200

@assignments_bp.route('/<int:id>', methods=['DELETE'])
def delete_assignment_detail(id):
    """
    Delete an assignment
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The assignment ID
    responses:
      204:
        description: Assignment deleted successfully
      404:
        description: Assignment not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: Assignment not found
    """
    success = delete_assignment(id)
    if not success:
        return jsonify({"error": "Assignment not found"}), 404
    return jsonify({"message": "Assignment deleted successfully"}), 204
