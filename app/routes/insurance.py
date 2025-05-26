from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.insurance import Insurance
from app.schemas.insurance import InsuranceSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

insurance_bp = Blueprint("insurance", __name__, url_prefix="/insurance")

@insurance_bp.route("", methods=["POST"])
@jwt_required()
def add_insurance():
    data = request.get_json()
    schema = InsuranceSchema()
    insurance_data = schema.load(data)

    new_insurance = Insurance(**insurance_data)
    db.session.add(new_insurance)
    db.session.commit()

    return jsonify(schema.dump(new_insurance)), 201

@insurance_bp.route("/patient/<int:patient_id>", methods=["GET"])
@jwt_required()
def get_insurance_by_patient(patient_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Allow patient to see their own insurance
    if user.role == "patient" and user.person_id != patient_id:
        return jsonify({"message": "Access denied"}), 403

    insurances = Insurance.query.filter_by(patient_id=patient_id).all()
    schema = InsuranceSchema(many=True)
    return jsonify(schema.dump(insurances)), 200
