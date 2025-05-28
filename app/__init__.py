from flask import Flask, jsonify

from app.models.revoked_token import RevokedToken
from .config import Config
from .extensions import db, migrate, jwt
from .routes import register_blueprints
from flasgger import Swagger
from .schemas.swagger_definitions import swagger_template
from .config import app_config
from flask_cors import CORS

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    Swagger(app, template=swagger_template)
    from .models import appointment, user, patient, provider, insurance, record, person
    register_blueprints(app)
    CORS(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = RevokedToken.query.filter_by(jti=jti).first()
        return token is not None  # True means token is revoked

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has been revoked"}), 401

    return app
