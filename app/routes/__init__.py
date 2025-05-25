from .auth import auth_bp
from .provider import provider_bp
def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(provider_bp)
