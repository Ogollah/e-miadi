from app.extensions import db

class Insurance(db.Model):
    __tablename__ = 'insurance'
    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(100), nullable=False)
    policy_number = db.Column(db.String(50), nullable=False)
    coverage_details = db.Column(db.Text)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
