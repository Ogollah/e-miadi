from marshmallow import Schema, fields, validate
class PatientSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    date_of_birth = fields.Date(required=False)
    phone = fields.Str(validate=validate.Length(min=10, max=15, error="Phone number must be between 10 and 15 characters long."))
    email = fields.Email()
    gender = fields.Str()
    national_id = fields.Str(validate=validate.Length(min = 8, error="National ID must be exactly 8 characters long."))
