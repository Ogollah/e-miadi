from marshmallow import Schema, fields

class MedicalRecordSchema(Schema):
    appointment_id = fields.Int(required=True)
    diagnosis = fields.Str()
    treatment = fields.Str()
    notes = fields.Str()
