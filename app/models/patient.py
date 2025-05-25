from app.extensions import db
from .person import Person
from sqlalchemy.orm import validates
import uuid

class Patient(Person):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)

    patient_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True)
    national_id = db.Column(db.String(30), unique=True)
    address = db.Column(db.String(200))

    __mapper_args__ = {'polymorphic_identity': 'patient'}

    insurance = db.relationship('Insurance', backref='patient')
    appointments = db.relationship('Appointment', backref='patient')
