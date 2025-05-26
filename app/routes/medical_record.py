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
    """
    Create a new medical record for a completed appointment.
    Only providers are allowed to create medical records.
    ---
    tags:
      - Medical Records
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/MedicalRecord'
    responses:
      201:
        description: Medical record created
      400:
        description: Validation error
      403:
        description: Only providers can create medical records
      404:
        description: Appointment not found
    """
    current_user_id = int(get_jwt_identity())
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
    """
    Get all medical records for a specific patient
    ---
    tags:
      - Medical Records
    parameters:
      - name: patient_id
        in: path
        required: true
        type: integer
        description: ID of the patient
    responses:
      200:
        description: List of medical records
      403:
        description: Unauthorized access
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role == 'patient' and user.person_id != patient_id:
        return jsonify({"message": "Unauthorized"}), 403

    records = MedicalRecord.query.filter_by(patient_id=patient_id).all()

    schema = MedicalRecordSchema(many=True)
    return jsonify(schema.dump(records)), 200

@medical_record_bp.route('/appointment/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_medical_record_by_appointment(appointment_id):
    """
    Get medical record by appointment ID
    ---
    tags:
      - Medical Records
    parameters:
      - name: appointment_id
        in: path
        required: true
        type: integer
        description: Appointment ID
    responses:
      200:
        description: Medical record
      403:
        description: Access denied
      404:
        description: No medical record found
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    record = MedicalRecord.query.filter_by(appointment_id=appointment_id).first()
    if not record:
        return jsonify({"message": "No medical record found for this appointment"}), 404

    if user.role == 'patient' and user.person_id != record.patient_id:
        return jsonify({"message": "Access denied"}), 403
    if user.role == 'provider' and user.person_id != record.provider_id:
        return jsonify({"message": "Access denied"}), 403

    schema = MedicalRecordSchema()
    return jsonify(schema.dump(record)), 200

@medical_record_bp.route("", methods=["GET"])
@jwt_required()
def list_all_records():
    """
    List all medical records for the authenticated user
    ---
    tags:
      - Medical Records
    parameters:
      - name: diagnosis
        in: query
        type: string
        description: Filter records by diagnosis keyword
    responses:
      200:
        description: List of records
    """
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
    """
    Get a medical record by record ID
    ---
    tags:
      - Medical Records
    parameters:
      - name: record_id
        in: path
        required: true
        type: integer
        description: ID of the medical record
    responses:
      200:
        description: Medical record data
      403:
        description: Access denied
      404:
        description: Record not found
    """
    record = MedicalRecord.query.get_or_404(record_id)
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role == "patient" and record.patient_id != user.person_id:
        return jsonify({"message": "Access denied"}), 403
    if user.role == "provider" and record.provider_id != user.person_id:
        return jsonify({"message": "Access denied"}), 403

    schema = MedicalRecordSchema()
    return jsonify(schema.dump(record)), 200

@medical_record_bp.route("/<int:record_id>", methods=["PATCH"])
@jwt_required()
def update_record(record_id):
    """
    Update an existing medical record (only allowed by the provider who created it).
    ---
    tags:
      - Medical Records
    parameters:
      - name: record_id
        in: path
        required: true
        schema:
          type: integer
        description: ID of the medical record to update
      - in: body
        name: body
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                diagnosis:
                  type: string
                  description: Updated diagnosis
                treatment:
                  type: string
                  description: Updated treatment
                notes:
                  type: string
                  description: Updated notes
    responses:
      200:
        description: Medical record updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                record:
                  $ref: '#/components/schemas/MedicalRecord'
      403:
        description: Access denied (only the provider who created the record can update it)
      404:
        description: Medical record not found
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    record = MedicalRecord.query.get_or_404(record_id)

    if user.role != "provider" or user.person_id != record.provider_id:
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()
    if "diagnosis" in data:
        record.diagnosis = data["diagnosis"]
    if "treatment" in data:
        record.treatment = data["treatment"]
    if "notes" in data:
        record.notes = data["notes"]

    db.session.commit()
    return jsonify({"message": "Record updated", "record": MedicalRecordSchema().dump(record)}), 200

@medical_record_bp.route("/<int:record_id>", methods=["DELETE"])
@jwt_required()
def delete_record(record_id):
    """
    Delete a medical record (only by the provider who created it).
    ---
    tags:
      - Medical Records
    parameters:
      - name: record_id
        in: path
        required: true
        schema:
          type: integer
        description: ID of the medical record to delete
    responses:
      200:
        description: Medical record deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      403:
        description: Access denied (only the provider who created the record can delete it)
      404:
        description: Medical record not found
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    record = MedicalRecord.query.get_or_404(record_id)

    if user.role != "provider" or user.person_id != record.provider_id:
        return jsonify({"message": "Access denied"}), 403

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted successfully"}), 200
