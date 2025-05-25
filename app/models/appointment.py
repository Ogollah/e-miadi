from app.extensions import db
from datetime import datetime

class AppointmentType(db.Model):
    __tablename__ = 'appointment_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)

    appointment_type_id = db.Column(db.Integer, db.ForeignKey('appointment_types.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)

    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(30), default='scheduled')  # scheduled, completed, cancelled

    appointment_type = db.relationship('AppointmentType')
    medical_record = db.relationship('MedicalRecord', backref='appointment', uselist=False)
