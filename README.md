# HealthConnect Platform 🏥

> **Smart India Hackathon (SIH) Prototype**
> Intelligent Healthcare, Connected Around You.
> Powered by a 100% Offline Dual-Model Machine Learning Ensemble (Random Forest + XGBoost).

---

## 🌟 Project Overview

HealthConnect is a healthcare technology platform designed to bridge initial symptom awareness with direct clinical care and specialist discovery. The system enables users to perform preliminary symptom checks with explainable AI, find certified medical specialists across multiple fields, locate emergency trauma hospitals with 24/7 care flags, schedule consultations, and maintain clinical histories.

### Key Highlights
- **100% Offline Local Machine Learning Inference**: Zero external AI or cloud LLM dependencies. Operates privately and reliably on edge or local servers.
- **Dual-Model Calibrated Ensemble**: Combines **Random Forest** (120 trees) and **XGBoost** (`multi:softprob`) across 132 standardized clinical symptom dimensions.
- **Dynamic Probabilities & Top-3 Conditions**: Returns ranked potential conditions, calibrated model confidence percentages, and breakdown of contributing symptoms.
- **Safety Triage & Emergency Rules**: Built-in clinical safety rules detect acute myocardial infarction, severe respiratory distress, and stroke symptoms, triggering immediate alerts.
- **Modern Full-Stack Architecture**: React.js SPA (Vite + Tailwind CSS + Lucide) connected via REST APIs and Axios to a Python Flask backend and SQLite database.

---

## 🏗️ Core Architecture

```
                    HEALTHCONNECT
                          │
                          ▼
                  React.js Frontend (Vite)
                          │
                        Axios
                          │
                      REST APIs (JSON)
                          │
                          ▼
                    Flask Backend
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
    Database          ML Engine     Healthcare Logic
  (SQLAlchemy)            │
                   ┌──────┴──────┐
                   ▼             ▼
             Random Forest    XGBoost
                   │             │
                   └──────┬──────┘
                          │
                          ▼
                  Soft Voting Ensemble
                          │
                          ▼
                   Top-3 Predictions
                          │
                          ▼
                    Knowledge Base
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
    Severity         Specialist         Prevention
                          │
                          ▼
                   Doctor Discovery
                          │
                          ▼
                  Appointment Booking
```

---

## 💻 Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React.js 19, Vite, Tailwind CSS, Lucide React, Axios, React Router v7 |
| **Backend** | Python 3.10+, Flask, Flask-SQLAlchemy, Flask-Login, Flask-CORS, Werkzeug |
| **Machine Learning** | Scikit-learn (RandomForestClassifier), XGBoost (XGBClassifier), NumPy, Joblib |
| **Database** | SQLite (development) / PostgreSQL compatible |
| **Knowledge Base** | Curated clinical mapping covering 41 disease categories and 132 clinical symptoms |

---

## 🚀 Getting Started & How to Run

### 1. Prerequisites
- Python 3.10 or higher
- Node.js 18+ and npm

### 2. Backend Setup (Flask)
```bash
# Navigate to project root
cd "c:\Users\DIKSHA CHURI\Downloads\HealthConnectPlatform-1-main\HealthConnectPlatform-1-main"

# Install Python dependencies
pip install -r requirements.txt

# Run backend test suite to verify database and ML models
python test_full_suite.py

# Start Flask Backend API (Runs on port 5000 by default)
python main.py
```
*Backend will be online at `http://localhost:5000` by default. Set `PORT` to use another port. The Vite proxy defaults to this port; set `BACKEND_URL` in `frontend/.env` if Flask runs elsewhere.*

### 3. Frontend Setup (React.js)
```bash
# Open a new terminal and navigate to frontend/
cd "c:\Users\DIKSHA CHURI\Downloads\HealthConnectPlatform-1-main\HealthConnectPlatform-1-main\frontend"

# Install npm dependencies
npm install

# Start Vite development server (Runs on port 5173)
npm run dev
```
*Frontend will be online at `http://localhost:5173`.*

---

## 🔑 Demo Accounts (One-Click Credentials)

The login screen includes quick-fill buttons for immediate hackathon judging:

| Account Type | Email | Password | Role |
| :--- | :--- | :--- | :--- |
| **Patient Demo** | `patient@healthconnect.com` | `Password123` | Patient Portal & Appointments |
| **Doctor Demo** | `dr.ananya@healthconnect.com` | `DoctorPass123` | Doctor Consultation Dashboard |

---

## 📡 API Endpoint Catalog

### Authentication
- `POST /api/auth/register` — Register a new Patient or Doctor account
- `POST /api/auth/login` — Sign in and create persistent session
- `POST /api/auth/logout` — Invalidate session
- `GET /api/auth/me` — Check current user session status

### Clinical AI & Symptom Checker
- `GET /api/symptoms/list` — Returns all 132 symptoms grouped by clinical categories
- `POST /api/symptoms/analyze` — Main local ML inference endpoint (Random Forest + XGBoost soft ensemble)
- `GET /api/symptoms/history` — Patient's previous AI health evaluations

### Doctor Discovery & Scheduling
- `GET /api/doctors` — Search and filter verified doctors by specialty/city/name
- `GET /api/doctors/<id>` — Detailed doctor profile, bio, and license information
- `GET /api/doctors/specializations` — List of all available medical disciplines
- `GET /api/doctor-availability` — Dynamic slot calculation based on date and existing bookings
- `GET /api/doctor/dashboard` — Doctor's schedule, consultations, and stats

### Hospitals & Emergency Care
- `GET /api/hospitals` — Accredited medical centers with emergency filtering
- `GET /api/hospitals/<id>` — Hospital department details, contacts, and trauma status

### Appointments
- `GET /api/appointments` — List consultations for authenticated user
- `POST /api/appointments` — Book new appointment slot
- `PUT /api/appointments/<id>/status` — Update appointment status (`completed`, `cancelled`, `scheduled`)
- `DELETE /api/appointments/<id>` — Cancel appointment

### Notifications
- `GET /api/notifications` — Notification inbox with unread count
- `POST /api/notifications/<id>/read` — Mark single notification as read
- `POST /api/notifications/mark-all-read` — Mark all notifications as read
- `POST /api/notifications/clear-all` — Clear notification feed

### Patient Dashboard & Profile
- `GET /api/patient/dashboard` — Upcoming consultations, recent analyses, and quick stats
- `GET /api/patient/profile` — Clinical demographics and emergency contacts
- `PUT /api/patient/profile` — Update address, blood group, emergency contact, etc.

---

## 🧠 Machine Learning Engine Architecture

HealthConnect's inference pipeline uses local machine learning without external cloud APIs:

1. **Feature Engineering**: Standardizes raw symptom inputs into a 132-element binary feature vector.
2. **Random Forest Classifier**: 120 decision trees trained with depth constraints for high variance reduction.
3. **XGBoost Classifier**: Extreme gradient boosted trees with multi-class soft probability distribution.
4. **Soft Voting Ensemble**: Averages output probability matrices:
   $$\hat{P}(c) = \frac{P_{RF}(c) + P_{XGB}(c)}{2}$$
5. **Dynamic Top-3 Extraction**: Extracts the top 3 ranked conditions with dynamically computed probabilities.
6. **Safety Rules Engine**: Evaluates symptom co-occurrence against acute clinical emergencies (e.g. chest pain + breathlessness + sweating).
7. **Knowledge Base Mapping**: Enriches predictions with specialist doctor recommendations, severity triage, precautions, and red-flag warning signs.

Model artifacts stored in `ml_engine/models/`:
- `random_forest.joblib`
- `xgboost.joblib`
- `label_encoder.joblib`
- `symptom_encoder.joblib`
- `knowledge_base.json`

---

## 🧪 Testing

Run the automated backend test suite:
```bash
python test_full_suite.py
```
*Executes 28 automated integration tests covering ML inference, edge cases, auth, doctor scheduling, and notifications.*

Build frontend production bundle:
```bash
cd frontend
npm run build
```

---

## ⚕️ Medical Disclaimer

> **Important Medical Disclaimer**: HealthConnect provides preliminary health insights for educational awareness and decision support. It does not constitute a certified medical diagnosis. Users should always consult a licensed medical doctor or seek emergency medical care for acute or concerning symptoms.
