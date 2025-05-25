from app import create_app
from app.extensions import db
from app.models.appointment import AppointmentType

app = create_app()

with app.app_context():
    types = ['Consultation', 'Follow-up', 'Referral']
    for name in types:
        if not AppointmentType.query.filter_by(name=name).first():
            db.session.add(AppointmentType(name=name))
    db.session.commit()
    print("Seeded appointment types.")
