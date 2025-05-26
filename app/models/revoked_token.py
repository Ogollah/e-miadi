from app.extensions import db
from datetime import datetime

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True, nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
