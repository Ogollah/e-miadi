from app.extensions import db

class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    gender = db.Column(db.String(10))
    national_id = db.Column(db.String(30), unique=True)

    type = db.Column(db.String(50))  # Discriminator for joined-table inheritance
    __mapper_args__ = {'polymorphic_identity': 'person', 'polymorphic_on': type}
