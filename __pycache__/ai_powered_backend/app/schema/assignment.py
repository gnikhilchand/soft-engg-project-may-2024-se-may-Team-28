from marshmallow import Schema, fields
from app.schema.submission import SubmissionSchema  


class AssignmentSchema(Schema):
    id = fields.Int(dump_only=True)
    course_id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    due_date = fields.DateTime(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    submissions = fields.Nested(SubmissionSchema, many=True, dump_only=True)



