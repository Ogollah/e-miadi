# e-miadi

**e-miadi** is a secure and scalable healthcare appointment scheduling system built with Flask and PostgreSQL. It enables patient registration, provider management, appointment booking, role-based access control, JWT authentication, and insurance support.

---

## 🚀 Features

- ✅ Person-based modeling (Person → Patient/Provider → User)
- 🔐 JWT authentication with role-based access (`admin`, `provider`, `patient`)
- 📅 Appointment scheduling with conflict prevention
- 🏥 Patient registration with multiple insurance covers
- 📄 Swagger/OpenAPI docs for API
- 🧪 Integrated testing with `unittest`

---

## 📁 Project Structure

```
e-miadi/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── person.py
│   │   ├── patient.py
│   │   ├── provider.py
│   │   ├── appointment.py
│   │   └── insurance.py
│   │   └── record.py
│   │   └── revokeed_token.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── patient.py
│   │   ├── provider.py
│   │   └── appointment.py
│   │   └── insurance.py
│   │   └── medical_record.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── person.py
│   │   ├── patient.py
│   │   ├── provider.py
│   │   ├── appointment.py
│   │   └── insurance.py
│   │   └── swagger_definition.py
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_patient.py
│       ├── test_provider.py
│       └── test_appointment.py
├── migrations/
│   └── ...
├── requirements.txt
├── README.md
├── run.py
└── .env
```
