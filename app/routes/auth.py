from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.provider import Provider
from app.models.user import User
from app.schemas.provider import ProviderSchema
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register-user', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    person_id = data.get("person_id")

    if not all([username, password, role, person_id]):
        return jsonify({"message": "Missing required fields"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409

    # Create User from existing person (provider or patient)
    user = User(username=username, role=role, person_id=person_id if role == "provider" else None)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully."}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not user.check_password(data.get("password")):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity={'id': user.id, 'role': user.role},
        expires_delta=timedelta(hours=1)
    )
    return jsonify(access_token=access_token), 200
