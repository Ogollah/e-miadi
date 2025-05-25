from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from app.models.patient import Patient
from app.schemas.patient import PatientSchema
from app.extensions import db

patient_bp = Blueprint('patients', __name__, url_prefix='/patients')
@patient_bp.route('', methods=['POST'])
def register_patient():
    data = request.get_json()
    schema = PatientSchema()
    patient_data = schema.load(data)

    # Auto-generate next patient number
    last_patient = Patient.query.order_by(Patient.id.desc()).first()
    next_id = last_patient.id + 1 if last_patient else 1
    patient_number = f"PAT-{next_id:03d}" # Format as PAT-001, PAT-002, etc.

    patient = Patient(**patient_data, patient_number=patient_number)

    try:
        db.session.add(patient)
        db.session.commit()
        return jsonify({
            "message": "Patient registered successfully",
            "patient_id": patient.id,
            "patient_number": patient.patient_number
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Duplicate entry"}), 409
