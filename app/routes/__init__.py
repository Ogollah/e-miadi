from .auth import auth_bp
from .provider import provider_bp
from .appointment import appointment_bp
from .patient import patient_bp
def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(provider_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(patient_bp)
