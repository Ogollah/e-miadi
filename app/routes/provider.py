from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.provider import Provider
from app.schemas.provider import ProviderSchema

provider_bp = Blueprint('provider', __name__, url_prefix='/providers')

@provider_bp.route('', methods=['POST'])
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
