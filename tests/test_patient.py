import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models.user import User

class PatientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            admin = User(
                username="admin",
                role="provider"
            )
            admin.set_password("adminpass")
            db.session.add(admin)
            db.session.commit()

    def test_create_patient_with_auth(self):
        with self.app.app_context():
            # First, login to get the token
            login_resp = self.client.post("/auth/login", json={
                "username": "admin",
                "password": "adminpass"
            })
            
            self.assertEqual(login_resp.status_code, 200)
            self.token = login_resp.get_json()["access_token"]
            self.auth_header = {"Authorization": f"Bearer {self.token}"}

            # Now create a patient with the token
            response = self.client.post("/patients", json={
                "first_name": "Jane",
                "last_name": "Doe",
                "gender": "Female",
                "date_of_birth": "1995-05-15",
                "phone": "0712345678",
                "email": "jane@mail.com",
                "national_id": "87654321"
            }, headers=self.auth_header)
            
            self.assertEqual(response.status_code, 201)

    def test_create_patient_without_auth(self):
        # Attempt to create a patient without authentication
        response = self.client.post("/patients", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "gender": "Female",
            "date_of_birth": "1995-05-15",
            "phone": "0712345678",
            "email": "jane@mail.com",
            "national_id": "87654321"
        })

        self.assertEqual(response.status_code, 401)

    def test_list_patients_with_auth(self):
        with self.app.app_context():
            # First, login to get the token
            login_resp = self.client.post("/auth/login", json={
                "username": "admin",
                "password": "adminpass"
            })
            self.assertEqual(login_resp.status_code, 200)
            self.token = login_resp.get_json()["access_token"]
            self.auth_header = {"Authorization": f"Bearer {self.token}"}

            # Now list patients with the token
            response = self.client.get("/patients", headers=self.auth_header)

            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIsInstance(data, list)

    def test_get_patient_with_auth(self):
        with self.app.app_context():
            # First, login to get the token
            login_resp = self.client.post("/auth/login", json={
                "username": "admin",
                "password": "adminpass"
            })
            self.assertEqual(login_resp.status_code, 200)
            self.token = login_resp.get_json()["access_token"]
            self.auth_header = {"Authorization": f"Bearer {self.token}"}

            # Create a patient to retrieve
            create_resp = self.client.post("/patients", json={
                "first_name": "Jane",
                "last_name": "Doe",
                "gender": "Female",
                "date_of_birth": "1995-05-15",
                "phone": "0712345678",
                "email": "jane@mail.com",
                "national_id": "87654321"
            }, headers=self.auth_header)
            self.assertEqual(create_resp.status_code, 201)
            patient_id = create_resp.get_json()["patient_id"]

            # Now get the patient with the token
            response = self.client.get(f"/patients/{patient_id}", headers=self.auth_header)
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main(verbosity=2)