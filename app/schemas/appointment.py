from marshmallow import Schema, fields, validate

from marshmallow import Schema, fields, validate

class AppointmentSchema(Schema):
    patient_id = fields.Int(required=True)
    provider_id = fields.Int(required=True)
    appointment_type_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    status = fields.Str(
        validate=validate.OneOf(["scheduled", "completed", "cancelled", "rescheduled"]),
        load_default="scheduled"
    )
    rescheduled_start_time = fields.DateTime(dump_only=True)
    rescheduled_end_time = fields.DateTime(dump_only=True)

