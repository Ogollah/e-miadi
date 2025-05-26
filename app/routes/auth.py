from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.provider import Provider
from app.models.revoked_token import RevokedToken
from app.models.user import User
from app.schemas.provider import ProviderSchema
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register-user', methods=['POST'])
def register_user():
    """
    Register a new user linked to an existing person (provider or patient).
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definations/User'
    responses:
      201:
        description: User created successfully
      400:
        description: Missing required fields
      409:
        description: Username already exists
    """
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

from flask_jwt_extended import create_access_token
from datetime import timedelta

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and return a JWT access token.
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: The username
            password:
              type: string
              description: The password
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not user.check_password(data.get("password")):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user.id), 
        additional_claims={"role": user.role},
        expires_delta=timedelta(hours=1)
    )

    return jsonify(access_token=access_token), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Logout the current user by revoking their JWT token.
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    parameters: []
    responses:
      200:
        description: Successfully logged out
        schema:
          type: object
          properties:
            message:
              type: string
    """
    jwt_data = get_jwt()
    revoked = RevokedToken(
        jti=jwt_data["jti"],
        token_type=jwt_data["type"]
    )
    db.session.add(revoked)
    db.session.commit()
    return jsonify({"message": "Successfully logged out"}), 200
