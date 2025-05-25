from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from .routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .models import appointment, user, patient, provider, insurance, record, person
    register_blueprints(app)

    return app
