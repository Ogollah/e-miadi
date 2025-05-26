from app.extensions import db
from .person import Person
from sqlalchemy.orm import validates
import uuid

class Patient(Person):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)

    patient_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True)
    patient_number = db.Column(db.String(20), unique=True)

    __mapper_args__ = {'polymorphic_identity': 'patient'}

    insurances = db.relationship("Insurance", back_populates="patient", cascade="all, delete-orphan")

    appointments = db.relationship('Appointment', backref='patient')
