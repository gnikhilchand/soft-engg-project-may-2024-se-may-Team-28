from marshmallow import Schema, fields

class SubmissionSchema(Schema):
    id = fields.Int(dump_only=True)
    assignment_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)