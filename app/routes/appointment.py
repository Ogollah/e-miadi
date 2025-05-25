from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_, or_

appointment_bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@appointment_bp.route('', methods=['POST'])
# @jwt_required()
def create_appointment():
    data = request.get_json()
    schema = AppointmentSchema()
    appt_data = schema.load(data)

    # Check for overlapping appointments
    overlapping = Appointment.query.filter(
        Appointment.provider_id == appt_data["provider_id"],
        Appointment.status == "scheduled",
        or_(
            and_(
                Appointment.start_time <= appt_data["start_time"],
                Appointment.end_time > appt_data["start_time"]
            ),
            and_(
                Appointment.start_time < appt_data["end_time"],
                Appointment.end_time >= appt_data["end_time"]
            ),
            and_(
                Appointment.start_time >= appt_data["start_time"],
                Appointment.end_time <= appt_data["end_time"]
            )
        )
    ).first()

    if overlapping:
        return jsonify({"message": "Provider is not available at the requested time"}), 409

    appointment = Appointment(**appt_data)
    db.session.add(appointment)
    db.session.commit()

    return jsonify({
        "message": "Appointment scheduled successfully",
        "appointment_id": appointment.id
    }), 201
