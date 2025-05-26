import datetime
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.appointment import Appointment
from app.models.user import User
from app.schemas.appointment import AppointmentSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_, or_
from dateutil.parser import parse

appointment_bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@appointment_bp.route('', methods=['POST'])
@jwt_required()
def create_appointment():
    """
    Create a new appointment
    ---
    tags:
      - Appointments
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Appointment'
    responses:
      201:
        description: Appointment created successfully
      401:
        description: Unauthorized
      403:
        description: Access denied
      409:
        description: Conflict due to overlapping appointment
    """
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    data = request.get_json()
    schema = AppointmentSchema()
    appt_data = schema.load(data)

    if user.role == "patient" and user.person_id != appt_data["patient_id"]:
        return jsonify({"message": "Access denied"}), 403

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

@appointment_bp.route("/<int:appointment_id>/status", methods=["PATCH"])
@jwt_required()
def update_appointment_status(appointment_id):
    """
    Update appointment status (e.g., reschedule, cancel, complete)
    ---
    tags:
      - Appointments
    parameters:
      - name: appointment_id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            status:
              type: string
            rescheduled_start_time:
              type: string
            rescheduled_end_time:
              type: string
    responses:
      200:
        description: Status updated
      400:
        description: Invalid input
      401:
        description: Unauthorized
      403:
        description: Forbidden access
      404:
        description: Appointment not found
    """
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    appointment = Appointment.query.get_or_404(appointment_id)

    data = request.get_json()
    new_status = data.get("status")

    valid_statuses = ["scheduled", "completed", "cancelled", "rescheduled"]
    if new_status not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 400

    # Auth checks
    if user.role == "patient" and appointment.patient_id != user.person_id:
        return jsonify({"error": "Access denied"}), 403
    if user.role == "provider" and appointment.provider_id != user.person_id:
        return jsonify({"error": "Access denied"}), 403
    if user.role == "patient" and new_status == "completed":
        return jsonify({"error": "Only providers can mark as completed"}), 403

    if new_status == "rescheduled":
        new_start = data.get("rescheduled_start_time")
        new_end = data.get("rescheduled_end_time")
        if not new_start or not new_end:
            return jsonify({"error": "Provide reschedule times"}), 400
        try:
            appointment.rescheduled_start_time = parse(new_start)
            appointment.rescheduled_end_time = parse(new_end)
        except Exception:
            return jsonify({"error": "Invalid datetime format"}), 400

    appointment.status = new_status
    db.session.commit()

    return jsonify(AppointmentSchema().dump(appointment)), 200

@appointment_bp.route("", methods=["GET"])
@jwt_required()
def list_appointments():
    """
    List all appointments for the authenticated user
    ---
    tags:
      - Appointments
    parameters:
      - name: status
        in: query
        type: string
        required: false
        description: Filter by appointment status
    responses:
      200:
        description: List of appointments
        schema:
          type: array
          items:
            $ref: '#/definitions/Appointment'
      401:
        description: Unauthorized
    """
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    status = request.args.get("status")
    query = Appointment.query

    if user.role == "patient":
        query = query.filter_by(patient_id=user.person_id)
    elif user.role == "provider":
        query = query.filter_by(provider_id=user.person_id)

    if status:
        query = query.filter_by(status=status)

    return jsonify(AppointmentSchema(many=True).dump(query.all())), 200

@appointment_bp.route("/<int:appointment_id>", methods=["GET"])
@jwt_required()
def get_appointment_by_id(appointment_id):
    """
    Get appointment by ID
    ---
    tags:
      - Appointments
    parameters:
      - name: appointment_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Appointment data
        schema:
          $ref: '#/definitions/Appointment'
      401:
        description: Unauthorized
      404:
        description: Appointment not found
    """
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify(AppointmentSchema().dump(appointment)), 200

@appointment_bp.route("/patient/<int:patient_id>", methods=["GET"])
@jwt_required()
def get_appointments_by_patient(patient_id):
    """
    Get all appointments for a specific patient
    ---
    tags:
      - Appointments
    parameters:
      - name: patient_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: List of appointments for the patient
        schema:
          type: array
          items:
            $ref: '#/definitions/Appointment'
      401:
        description: Unauthorized
      404:
        description: No appointments or patient not found
    """
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    if not appointments:
        return jsonify({"error": "No appointments found for this patient"}), 404
    return jsonify(AppointmentSchema(many=True).dump(appointments)), 200


