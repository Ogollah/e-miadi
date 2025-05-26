from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.extensions import db
from app.models.record import MedicalRecord
from app.models.appointment import Appointment
from app.models.user import User
from app.schemas.medical_record import MedicalRecordSchema

medical_record_bp = Blueprint('medical_records', __name__, url_prefix='/medical-records')

@medical_record_bp.route('', methods=['POST'])
@jwt_required()
def create_medical_record():
    current_user_id = int(get_jwt_identity())  # ✅ Fix here
    user = User.query.get(current_user_id)

    if user.role != 'provider':
        return jsonify({"message": "Only providers can create medical records"}), 403

    data = request.get_json()
    schema = MedicalRecordSchema()
    try:
        record_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    appointment = Appointment.query.get(record_data['appointment_id'])
    if not appointment:
        return jsonify({"message": "Appointment not found"}), 404

    record = MedicalRecord(
        appointment_id=appointment.id,
        patient_id=appointment.patient_id,
        provider_id=appointment.provider_id,
        diagnosis=record_data.get('diagnosis'),
        treatment=record_data.get('treatment'),
        notes=record_data.get('notes'),
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Medical record created", "record_id": record.id}), 201

@medical_record_bp.route('/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_medical_records_by_patient(patient_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Patients can only view their own records
    if user.role == 'patient' and user.person_id != patient_id:
        return jsonify({"message": "Unauthorized"}), 403

    # Providers can view any patient records (or restrict further)
    records = MedicalRecord.query.filter_by(patient_id=patient_id).all()

    schema = MedicalRecordSchema(many=True)
    return jsonify(schema.dump(records)), 200


@medical_record_bp.route('/appointment/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_medical_record_by_appointment(appointment_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    record = MedicalRecord.query.filter_by(appointment_id=appointment_id).first()
    if not record:
        return jsonify({"message": "No medical record found for this appointment"}), 404

    # Authorization check
    if user.role == 'patient' and user.person_id != record.patient_id:
        return jsonify({"message": "Access denied"}), 403
    if user.role == 'provider' and user.person_id != record.provider_id:
        return jsonify({"message": "Access denied"}), 403

    schema = MedicalRecordSchema()
    return jsonify(schema.dump(record)), 200

@medical_record_bp.route("", methods=["GET"])
@jwt_required()
def list_all_records():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    query = MedicalRecord.query

    if user.role == "patient":
        query = query.filter_by(patient_id=user.person_id)
    elif user.role == "provider":
        query = query.filter_by(provider_id=user.person_id)

    search = request.args.get("diagnosis")
    if search:
        query = query.filter(MedicalRecord.diagnosis.ilike(f"%{search}%"))

    schema = MedicalRecordSchema(many=True)
    return jsonify(schema.dump(query.all())), 200

@medical_record_bp.route("/<int:record_id>", methods=["GET"])
@jwt_required()
def get_record_by_id(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role == "patient" and record.patient_id != user.person_id:
        return jsonify({"message": "Access denied"}), 403
    if user.role == "provider" and record.provider_id != user.person_id:
        return jsonify({"message": "Access denied"}), 403

    schema = MedicalRecordSchema()
    return jsonify(schema.dump(record)), 200

