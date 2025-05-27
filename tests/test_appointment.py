import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.models import User, Person, Provider, Patient
from app.extensions import db

class AppointmentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Create a user provider
            provider = User(
                username="john",
                role="provider",
                person_id=1
            )
            provider.set_password("providerpass")
            db.session.add(provider)
            db.session.commit()

    def test_create_appointment_with_auth(self):
        with self.app.app_context():
            # First, login to get the token
            login_resp = self.client.post("/auth/login", json={
                "username": "john",
                "password": "providerpass"
            })
            
            self.assertEqual(login_resp.status_code, 200)
            self.token = login_resp.get_json()["access_token"]
            self.auth_header = {"Authorization": f"Bearer {self.token}"}

            # Now create an appointment with the token
            response = self.client.post("/appointments", json={
                "patient_id": 2,  # Assuming patient with ID 2 exists
                "provider_id": 1,
                "start_time": "2023-10-01T10:00:00Z",
                "end_time": "2023-10-01T11:00:00Z",
                "appointment_type_id": 1,  # Assuming appointment type with ID 1 exists
                "status": "scheduled",
            }, headers=self.auth_header)
            
            self.assertEqual(response.status_code, 201)

    def test_create_appointment_without_auth(self):
        # Attempt to create an appointment without authentication
        response = self.client.post("/appointments", json={
            "patient_id": 2,  # Assuming patient with ID 2 exists
            "provider_id": 1,
            "start_time": "2023-10-01T10:00:00Z",
            "end_time": "2023-10-01T11:00:00Z",
            "appointment_type_id": 1,  # Assuming appointment type with ID 1 exists
            "status": "scheduled",
        })
        
        self.assertEqual(response.status_code, 401)

    def test_create_overlapping_appointment(self):
        with self.app.app_context():
            # First, login to get the token
            login_resp = self.client.post("/auth/login", json={
                "username": "john",
                "password": "providerpass"
            })
            
            self.assertEqual(login_resp.status_code, 200)
            self.token = login_resp.get_json()["access_token"]
            self.auth_header = {"Authorization": f"Bearer {self.token}"}

            # Create an initial appointment
            response = self.client.post("/appointments", json={
                "patient_id": 2,  # Assuming patient with ID 2 exists
                "provider_id": 1,
                "start_time": "2023-10-01T10:00:00Z",
                "end_time": "2023-10-01T11:00:00Z",
                "appointment_type_id": 1,  # Assuming appointment type with ID 1 exists
                "status": "scheduled",
            }, headers=self.auth_header)
            
            self.assertEqual(response.status_code, 201)

            # Attempt to create an overlapping appointment
            overlapping_response = self.client.post("/appointments", json={
                "patient_id": 2,  # Assuming patient with ID 2 exists
                "provider_id": 1,
                "start_time": "2023-10-01T10:30:00Z",
                "end_time": "2023-10-01T11:30:00Z",
                "appointment_type_id": 1,  # Assuming appointment type with ID 1 exists
                "status": "scheduled",
            }, headers=self.auth_header)
            
            self.assertEqual(overlapping_response.status_code, 409)

    def test_get_appointment_with_auth(self):
        with self.app.app_context():
            # First, login to get the token
            login_resp = self.client.post("/auth/login", json={
                "username": "john",
                "password": "providerpass"
            })
            
            self.assertEqual(login_resp.status_code, 200)
            self.token = login_resp.get_json()["access_token"]
            self.auth_header = {"Authorization": f"Bearer {self.token}"}

            # Create an appointment to retrieve
            response = self.client.post("/appointments", json={
                "patient_id": 2,  # Assuming patient with ID 2 exists
                "provider_id": 1,
                "start_time": "2023-10-01T10:00:00Z",
                "end_time": "2023-10-01T11:00:00Z",
                "appointment_type_id": 1,  # Assuming appointment type with ID 1 exists
                "status": "scheduled",
            }, headers=self.auth_header)
            
            self.assertEqual(response.status_code, 201)
            appointment_id = response.get_json()["appointment_id"]

            # Now retrieve the appointment
            get_response = self.client.get(f"/appointments/{appointment_id}", headers=self.auth_header)
            
            self.assertEqual(get_response.status_code, 200)
            data = get_response.get_json()
            self.assertEqual(data["status"], "scheduled")

    def test_reschedule_appointment(self):
        with self.app.app_context():
            # First, login to get the token
            login_resp = self.client.post("/auth/login", json={
                "username": "john",
                "password": "providerpass"
            })
            
            self.assertEqual(login_resp.status_code, 200)
            self.token = login_resp.get_json()["access_token"]
            self.auth_header = {"Authorization": f"Bearer {self.token}"}
    def test_reschedule_appointment(self):
        with self.app.app_context():
            # First, login to get the token
            login_resp = self.client.post("/auth/login", json={
                "username": "john",
                "password": "providerpass"
            })
            
            self.assertEqual(login_resp.status_code, 200)
            self.token = login_resp.get_json()["access_token"]
            self.auth_header = {"Authorization": f"Bearer {self.token}"}

            # Create an appointment to reschedule
            response = self.client.post("/appointments", json={
                "patient_id": 2,  # Assuming patient with ID 2 exists
                "provider_id": 1,
                "start_time": "2023-10-01T10:00:00Z",
                "end_time": "2023-10-01T11:00:00Z",
                "appointment_type_id": 1,  # Assuming appointment type with ID 1 exists
                "status": "scheduled",
            }, headers=self.auth_header)
            
            self.assertEqual(response.status_code, 201)
            appointment_id = response.get_json()["appointment_id"]

            # Now reschedule the appointment
            reschedule_response = self.client.patch(f"/appointments/{appointment_id}/status", json={
                "rescheduled_start_time": "2023-10-01T12:00:00Z",
                "rescheduled_end_time": "2023-10-01T13:00:00Z",
                "status": "rescheduled"
            }, headers=self.auth_header)
            
            self.assertEqual(reschedule_response.status_code, 200)
            data = reschedule_response.get_json()
            self.assertEqual(data["status"], "rescheduled")
            self.assertEqual(data["rescheduled_start_time"], "2023-10-01T12:00:00")
            self.assertEqual(data["rescheduled_end_time"], "2023-10-01T13:00:00")
