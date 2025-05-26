from app.extensions import db
from datetime import date

class Insurance(db.Model):
    __tablename__ = "insurance"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    provider_name = db.Column(db.String(120), nullable=False)
    policy_number = db.Column(db.String(120), nullable=False, unique=True)
    expiry_date = db.Column(db.Date, nullable=False)

    patient = db.relationship("Patient", back_populates="insurances")

