from marshmallow import Schema, fields

class FileSchema(Schema):
    id = fields.Int(dump_only=True)
    owner_id = fields.Int(required=True, load_only=True)
    filename = fields.Str(required=True)
    mime_type = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)
    size_bytes = fields.Int(dump_default=0)
    purpose = fields.Str(allow_none=True)
    storage_backend = fields.Str(dump_default='local')
    is_public = fields.Bool(dump_default=False)
    reference_count = fields.Int(dump_default=0)
    metadata = fields.Raw(allow_none=True)
    uploaded_at = fields.DateTime(dump_only=True)
