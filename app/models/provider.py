from app.extensions import db
from .person import Person

class Provider(Person):
    __tablename__ = 'providers'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)

    cadre = db.Column(db.String(100), nullable=False)  # e.g., General Doctor, Nurse
    specialization = db.Column(db.String(100), nullable=True)

    __mapper_args__ = {'polymorphic_identity': 'provider'}

    user = db.relationship('User', backref='provider', uselist=False)
    appointments = db.relationship('Appointment', backref='provider')
