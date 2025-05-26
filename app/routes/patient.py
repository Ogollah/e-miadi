from operator import or_
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from app.models.patient import Patient
from app.models.person import Person
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
    
@patient_bp.route("", methods=["GET"])
def list_patients():
    search = request.args.get("search")
    query = Patient.query

    if search:
        search = f"%{search}%"
        query = query.filter(or_(
            Person.first_name.ilike(search),
            Person.last_name.ilike(search),
            Person.national_id.ilike(search),
            Patient.patient_number.ilike(search)
        ))

    patients = query.all()
    schema = PatientSchema(many=True)
    return jsonify(schema.dump(patients)), 200

@patient_bp.route("/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    schema = PatientSchema()
    return jsonify(schema.dump(patient)), 200
