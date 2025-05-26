from marshmallow import Schema, fields

class InsuranceSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    provider_name = fields.Str(required=True)
    policy_number = fields.Str(required=True)
    expiry_date = fields.Date(required=True)
