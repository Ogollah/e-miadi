swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "e-miadi Healthcare appoinment management API",
        "description": "API for managing patients, providers, appointments, and medical records",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "definitions": {
    "Appointment": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "patient_id": {"type": "integer"},
            "provider_id": {"type": "integer"},
            "appointment_type_id": {"type": "integer"},
            "start_time": {"type": "string", "format": "date-time"},
            "end_time": {"type": "string", "format": "date-time"},
            "status": {"type": "string"},
            "rescheduled_start_time": {"type": "string", "format": "date-time"},
            "rescheduled_end_time": {"type": "string", "format": "date-time"}
        }
    }
},
    "security": [
        {
            "Bearer": []
        }
    ]
}
