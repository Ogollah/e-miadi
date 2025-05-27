from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.person import Person
from app.models.provider import Provider
from app.schemas.provider import ProviderSchema

provider_bp = Blueprint('provider', __name__, url_prefix='/providers')

@provider_bp.route('', methods=['POST'])
@jwt_required()
def create_provider():
    data = request.get_json()
    schema = ProviderSchema()
    provider_data = schema.load(data)

    provider = Provider(**provider_data)
    db.session.add(provider)
    db.session.commit()

    return jsonify({
        "message": "Provider created successfully!",
        "provider_id": provider.id
    }), 201

@provider_bp.route("", methods=["GET"])
@jwt_required()
def list_providers():
    search = request.args.get("search")
    query = Provider.query

    if search:
        search = f"%{search}%"
        query = query.filter(or_(
            *[
                Person.first_name.ilike(search),
                Person.last_name.ilike(search),
                Provider.national_id.ilike(search)
            ]
        ))

    providers = query.all()
    schema = ProviderSchema(many=True)
    return jsonify(schema.dump(providers)), 200

@provider_bp.route("/<int:provider_id>", methods=["GET"])
def get_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    schema = ProviderSchema()
    return jsonify(schema.dump(provider)), 200

