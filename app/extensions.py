from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({"error": "Missing Authorization Header"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({"error": "Invalid token"}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token expired"}), 401
