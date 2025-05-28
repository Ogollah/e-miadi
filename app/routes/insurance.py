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
    # Allow provider to see insurance of patients they are linked to
    elif user.role == "provider":
        if not user.patients or patient_id not in [p.id for p in user.patients]:
            return jsonify({"message": "Access denied"}), 403

    insurances = Insurance.query.filter_by(patient_id=patient_id).all()
    schema = InsuranceSchema(many=True)
    return jsonify(schema.dump(insurances)), 200

@insurance_bp.route("/<int:insurance_id>", methods=["GET"])
@jwt_required()
def get_insurance(insurance_id):
    insurance = Insurance.query.get_or_404(insurance_id)
    schema = InsuranceSchema()
    return jsonify(schema.dump(insurance)), 200

@insurance_bp.route("/<int:insurance_id>", methods=["PUT"])
@jwt_required()
def update_insurance(insurance_id):
    data = request.get_json()
    schema = InsuranceSchema()
    insurance_data = schema.load(data)

    insurance = Insurance.query.get_or_404(insurance_id)
    for key, value in insurance_data.items():
        setattr(insurance, key, value)

    db.session.commit()
    return jsonify(schema.dump(insurance)), 200

# get all insurances
@insurance_bp.route("", methods=["GET"])
@jwt_required()
def get_all_insurances():
    # allow only providers and admins to see all insurances
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user.role not in ["provider", "admin"]:
        return jsonify({"message": "Access denied"}), 403
    insurances = Insurance.query.all()
    schema = InsuranceSchema(many=True)
    return jsonify(schema.dump(insurances)), 200
