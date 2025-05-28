from app import create_app
from app.extensions import db
from app.models.appointment import AppointmentType
from app.models.user import User


app = create_app('development')

# with app.app_context():
#     types = ['Consultation', 'Follow-up', 'Referral']
#     for name in types:
#         if not AppointmentType.query.filter_by(name=name).first():
#             db.session.add(AppointmentType(name=name))
#     db.session.commit()
#     print("Seeded appointment types.")



with app.app_context():
    if not User.query.filter_by(username='admin3').first():
        admin = User(username='admin3', role='provider')
        admin.set_password('admin3')
        db.session.add(admin)
        db.session.commit()
    # if not User.query.filter_by(username='provider').first():
    #     provider = User(username='provider', password='provider', role='provider')
    #     db.session.add(provider)
        print('Seeded admin user.')

