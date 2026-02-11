from marshmallow import Schema, fields

class AssignmentFileSchema(Schema):
    id = fields.Int(dump_only=True)
    assignment_id = fields.Int(required=True, load_only=True)
    file_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
