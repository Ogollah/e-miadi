from marshmallow import Schema, fields

class ProviderSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    date_of_birth = fields.Date(required=False)
    phone = fields.Str()
    email = fields.Email()
    gender = fields.Str()

    cadre = fields.Str(required=True)
    specialization = fields.Str(required=False)

