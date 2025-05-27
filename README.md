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

## ⚡ Quick Start

1. Clone the repo

```
$ git clone https://github.com/Ogollah/e-miadi.git
$ cd e-miadi
```

2. Initialize and activate a virtualenv:

```
$ python3 -venv venv
$ source env/bin/activate
```

3. Install the dependencies:

```
$ pip install -r requirements.txt
```

5. Run the development server:

```
$ python3 run.py
```

6. Navigate to [http://localhost:5000](http://localhost:5000) OR [http://localhost:5000/apidocs](http://localhost:5000/apidocs)

## 🗄️ DB Schema

```
-- Base persons table (inheritance pattern)
CREATE TABLE persons (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(120) NOT NULL,
    last_name VARCHAR(120) NOT NULL,
    date_of_birth DATE,
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(120) UNIQUE,
    gender VARCHAR(10),
    national_id VARCHAR(30) UNIQUE,
    type VARCHAR(50) NOT NULL
);

-- Patients table (inherits from persons)
CREATE TABLE patients (
    id INTEGER PRIMARY KEY REFERENCES persons(id) ON DELETE CASCADE,
    patient_id VARCHAR(36) UNIQUE NOT NULL DEFAULT gen_random_uuid()::text,
    patient_number VARCHAR(20) UNIQUE
);

-- Providers table (inherits from persons)
CREATE TABLE providers (
    id INTEGER PRIMARY KEY REFERENCES persons(id) ON DELETE CASCADE,
    cadre VARCHAR(100) NOT NULL,
    specialization VARCHAR(100)
);

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(512) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'provider',
    person_id INTEGER REFERENCES persons(id) ON DELETE SET NULL
);

-- Insurance table
CREATE TABLE insurance (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    provider_name VARCHAR(120) NOT NULL,
    policy_number VARCHAR(120) UNIQUE NOT NULL,
    expiry_date DATE NOT NULL
);

-- Appointment types table
CREATE TABLE appointment_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Appointments table
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    appointment_type_id INTEGER REFERENCES appointment_types(id) ON DELETE SET NULL,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    provider_id INTEGER NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(30) DEFAULT 'scheduled',
    rescheduled_start_time TIMESTAMP,
    rescheduled_end_time TIMESTAMP
);

-- Medical records table
CREATE TABLE medical_records (
    id SERIAL PRIMARY KEY,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id) ON DELETE CASCADE,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    provider_id INTEGER NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    diagnosis VARCHAR(255),
    treatment TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Revoked tokens table (for JWT token management)
CREATE TABLE revoked_tokens (
    id SERIAL PRIMARY KEY,
    jti VARCHAR(120) UNIQUE NOT NULL,
    token_type VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX idx_persons_type ON persons(type);
CREATE INDEX idx_persons_email ON persons(email);
CREATE INDEX idx_persons_phone ON persons(phone);
CREATE INDEX idx_persons_national_id ON persons(national_id);

CREATE INDEX idx_patients_patient_id ON patients(patient_id);
CREATE INDEX idx_patients_patient_number ON patients(patient_number);

CREATE INDEX idx_insurance_patient_id ON insurance(patient_id);
CREATE INDEX idx_insurance_policy_number ON insurance(policy_number);

CREATE INDEX idx_appointments_patient_id ON appointments(patient_id);
CREATE INDEX idx_appointments_provider_id ON appointments(provider_id);
CREATE INDEX idx_appointments_start_time ON appointments(start_time);
CREATE INDEX idx_appointments_status ON appointments(status);

CREATE INDEX idx_medical_records_appointment_id ON medical_records(appointment_id);
CREATE INDEX idx_medical_records_patient_id ON medical_records(patient_id);
CREATE INDEX idx_medical_records_provider_id ON medical_records(provider_id);
CREATE INDEX idx_medical_records_created_at ON medical_records(created_at);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_person_id ON users(person_id);

CREATE INDEX idx_revoked_tokens_jti ON revoked_tokens(jti);
```
