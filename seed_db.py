"""
Database Seeder for HealthConnectPlatform
Seeds verified doctors, accredited hospitals, and demo user accounts.
"""

import os
import sys
from datetime import date, time, datetime

# Ensure root dir is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) 

from app import app, db
from models import User, Patient, Doctor, Hospital, Notification, Appointment

def seed_database():
    with app.app_context():
        print("Synchronizing database schema...")
        db.create_all()
        
        # Check if already seeded
        if User.query.filter_by(email="patient@healthconnect.com").first():
            print("Database already contains seed data. Refreshing...")
        
        # 1. Create Demo Patient
        patient_user = User.query.filter_by(email="patient@healthconnect.com").first()
        if not patient_user:
            patient_user = User(
                email="patient@healthconnect.com",
                name="Rahul Sharma",
                user_type="patient"
            )
            patient_user.set_password("Password123")
            db.session.add(patient_user)
            db.session.commit()
            
            patient_profile = Patient(
                user_id=patient_user.id,
                date_of_birth=date(1998, 5, 15),
                gender="Male",
                blood_group="O+",
                address="102, Green Valley Apartments, Andheri West",
                city="Mumbai",
                state="Maharashtra",
                phone="+91 98765 12345",
                emergency_contact="+91 98765 54321"
            )
            db.session.add(patient_profile)
            
            welcome_notif = Notification(
                user_id=patient_user.id,
                title="Welcome to HealthConnect!",
                message="Welcome to HealthConnect - your AI-assisted, connected healthcare platform. Start by checking your symptoms or exploring verified doctors.",
                notification_type="general",
                read=False
            )
            db.session.add(welcome_notif)
            db.session.commit()
            print("[OK] Created Demo Patient: patient@healthconnect.com (Password123)")

        # 2. Create Specialist Doctors
        doctors_data = [
            {
                "name": "Dr. Ananya Sen",
                "email": "dr.ananya@healthconnect.com",
                "specialization": "Cardiologist",
                "bio": "Senior Consultant Interventional Cardiologist with over 15 years experience in coronary interventions, hypertension, and acute cardiac care.",
                "experience_years": 15,
                "license_number": "MCI-CARD-10293",
                "city": "Mumbai",
                "state": "Maharashtra",
                "address": "Cardiology Wing, Apollo Hospital, Navi Mumbai",
                "phone": "+91 98201 11223",
                "available_days": "Mon,Tue,Wed,Thu,Fri,Sat",
                "available_hours": '{"start": "09:00", "end": "17:00"}'
            },
            {
                "name": "Dr. Vikramaditya Rao",
                "email": "dr.vikram@healthconnect.com",
                "specialization": "Neurologist",
                "bio": "Fellow of Neurological Sciences with clinical expertise in migraine management, stroke rehabilitation, and neuromuscular disorders.",
                "experience_years": 12,
                "license_number": "MCI-NEUR-88371",
                "city": "Bengaluru",
                "state": "Karnataka",
                "address": "Neuro Care Clinic, Indiranagar",
                "phone": "+91 98450 33445",
                "available_days": "Mon,Tue,Wed,Thu,Fri",
                "available_hours": '{"start": "10:00", "end": "18:00"}'
            },
            {
                "name": "Dr. Priya Patel",
                "email": "dr.priya@healthconnect.com",
                "specialization": "Dermatologist",
                "bio": "Dermatologist & Cosmetologist specializing in autoimmune skin disorders, psoriasis, acne management, and fungal infections.",
                "experience_years": 9,
                "license_number": "MCI-DERM-44219",
                "city": "Ahmedabad",
                "state": "Gujarat",
                "address": "Skin & Glow Advanced Clinic, Bodakdev",
                "phone": "+91 98980 55667",
                "available_days": "Mon,Wed,Thu,Fri,Sat",
                "available_hours": '{"start": "11:00", "end": "19:00"}'
            },
            {
                "name": "Dr. Rajesh Kulkarni",
                "email": "dr.rajesh@healthconnect.com",
                "specialization": "General Physician",
                "bio": "Primary Care Physician and Diabetologist focused on preventive family health, viral fevers, seasonal infections, and chronic disease screening.",
                "experience_years": 18,
                "license_number": "MCI-GENP-99124",
                "city": "Pune",
                "state": "Maharashtra",
                "address": "Kulkarni Health Centre, Kothrud",
                "phone": "+91 98220 77889",
                "available_days": "Mon,Tue,Wed,Thu,Fri,Sat",
                "available_hours": '{"start": "08:30", "end": "16:30"}'
            },
            {
                "name": "Dr. Arindam Mukherjee",
                "email": "dr.arindam@healthconnect.com",
                "specialization": "Pulmonologist",
                "bio": "Pulmonary & Critical Care Consultant specializing in bronchial asthma, pneumonia, tuberculosis, and post-viral respiratory rehabilitation.",
                "experience_years": 14,
                "license_number": "MCI-PULM-77182",
                "city": "Kolkata",
                "state": "West Bengal",
                "address": "Chest & Allergy Institute, Salt Lake Sector 2",
                "phone": "+91 98300 99112",
                "available_days": "Tue,Wed,Thu,Fri,Sat",
                "available_hours": '{"start": "09:00", "end": "17:00"}'
            },
            {
                "name": "Dr. Sanjay Verma",
                "email": "dr.sanjay@healthconnect.com",
                "specialization": "Gastroenterologist",
                "bio": "Gastroenterologist and Hepatologist with extensive experience in GERD, peptic ulcers, viral hepatitis, and liver disease management.",
                "experience_years": 16,
                "license_number": "MCI-GAST-66251",
                "city": "New Delhi",
                "state": "Delhi",
                "address": "Digestive Disease Center, Saket",
                "phone": "+91 98110 33221",
                "available_days": "Mon,Tue,Wed,Thu,Fri",
                "available_hours": '{"start": "10:00", "end": "18:00"}'
            },
            {
                "name": "Dr. Meenakshi Sundaram",
                "email": "dr.meenakshi@healthconnect.com",
                "specialization": "Orthopedic Specialist",
                "bio": "Orthopedic Surgeon focusing on osteoarthritis, joint pain, spine care, and sports medicine injury recovery.",
                "experience_years": 11,
                "license_number": "MCI-ORTH-55198",
                "city": "Hyderabad",
                "state": "Telangana",
                "address": "Bones & Joints Specialty Hospital, Banjara Hills",
                "phone": "+91 98490 88776",
                "available_days": "Mon,Tue,Thu,Fri,Sat",
                "available_hours": '{"start": "09:30", "end": "17:30"}'
            },
            {
                "name": "Dr. Sneha Iyer",
                "email": "dr.sneha@healthconnect.com",
                "specialization": "Pediatrician",
                "bio": "Consultant Pediatrician providing newborn care, vaccination, pediatric infectious disease treatment, and adolescent medicine.",
                "experience_years": 10,
                "license_number": "MCI-PEDI-33214",
                "city": "Chennai",
                "state": "Tamil Nadu",
                "address": "Child Health Pavilion, T. Nagar",
                "phone": "+91 98400 44556",
                "available_days": "Mon,Tue,Wed,Thu,Fri,Sat",
                "available_hours": '{"start": "09:00", "end": "16:00"}'
            }
        ]

        for d in doctors_data:
            existing = User.query.filter_by(email=d["email"]).first()
            if not existing:
                u = User(
                    email=d["email"],
                    name=d["name"],
                    user_type="doctor"
                )
                u.set_password("DoctorPass123")
                db.session.add(u)
                db.session.commit()
                
                doc_profile = Doctor(
                    user_id=u.id,
                    specialization=d["specialization"],
                    bio=d["bio"],
                    experience_years=d["experience_years"],
                    license_number=d["license_number"],
                    city=d["city"],
                    state=d["state"],
                    address=d["address"],
                    phone=d["phone"],
                    available_days=d["available_days"],
                    available_hours=d["available_hours"]
                )
                db.session.add(doc_profile)
                db.session.commit()
                print(f"[OK] Created Doctor: {d['name']} ({d['specialization']})")

        # 3. Create Hospitals
        hospitals_data = [
            {
                "name": "Apollo Multispecialty Hospital",
                "address": "Plot No. 13, Off Parsik Hill Road, Sector 23, CBD Belapur",
                "city": "Navi Mumbai",
                "state": "Maharashtra",
                "phone": "+91 22 6280 6280",
                "email": "info_mumbai@apollohospitals.com",
                "website": "https://www.apollohospitals.com",
                "description": "JCI & NABH accredited 500-bed super specialty hospital offering 24/7 advanced emergency cardiac, neuro, and trauma care.",
                "specialties": "Cardiology, Neurology, Oncology, Orthopedics, Critical Care, Gastroenterology",
                "emergency_services": True
            },
            {
                "name": "Fortis Escorts Heart Institute",
                "address": "Okhla Road, New Friends Colony",
                "city": "New Delhi",
                "state": "Delhi",
                "phone": "+91 11 4713 5000",
                "email": "contactus.fehi@fortishealthcare.com",
                "website": "https://www.fortishealthcare.com",
                "description": "Pioneering center for cardiac bypass surgery, interventional cardiology, pediatric heart care, and critical trauma management.",
                "specialties": "Cardiology, Cardiac Surgery, Pulmonology, Vascular Surgery",
                "emergency_services": True
            },
            {
                "name": "Max Super Speciality Hospital",
                "address": "1, 2, Press Enclave Road, Mandir Marg, Saket",
                "city": "New Delhi",
                "state": "Delhi",
                "phone": "+91 11 2651 5050",
                "email": "enquiry@maxhealthcare.com",
                "website": "https://www.maxhealthcare.in",
                "description": "Leading healthcare facility equipped with state-of-the-art diagnostic labs, emergency life support, and multi-organ transplant units.",
                "specialties": "Gastroenterology, Hepatology, Pulmonology, Oncology, Endocrinology, Neurology",
                "emergency_services": True
            },
            {
                "name": "Manipal Hospital",
                "address": "98, HAL Old Airport Road, Kodihalli",
                "city": "Bengaluru",
                "state": "Karnataka",
                "phone": "+91 80 2502 4444",
                "email": "info@manipalhospitals.com",
                "website": "https://www.manipalhospitals.com",
                "description": "Flagship 600-bed tertiary care center known for excellence in robotic surgery, organ transplants, and 24x7 emergency resuscitation.",
                "specialties": "Neurology, Orthopedics, Pediatrics, Nephrology, General Medicine",
                "emergency_services": True
            },
            {
                "name": "Kokilaben Dhirubhai Ambani Hospital",
                "address": "Rao Saheb Achutrao Patwardhan Marg, Four Bungalows, Andheri West",
                "city": "Mumbai",
                "state": "Maharashtra",
                "phone": "+91 22 4269 6969",
                "email": "contact@kokilabenhospital.com",
                "website": "https://www.kokilabenhospital.com",
                "description": "Multi-specialty quaternary care hospital with dedicated stroke units, Level 1 trauma emergency department, and full-spectrum diagnostics.",
                "specialties": "Emergency Medicine, Cardiology, Dermatology, Neurology, Rheumatology",
                "emergency_services": True
            },
            {
                "name": "Medanta - The Medicity",
                "address": "CH Bakhtawar Singh Road, Sector 38",
                "city": "Gurugram",
                "state": "Haryana",
                "phone": "+91 124 414 1414",
                "email": "info@medanta.org",
                "website": "https://www.medanta.org",
                "description": "Sprawling 1250-bed multi-super-specialty institute bringing together world-class doctors and clinical infrastructure.",
                "specialties": "Critical Care, Liver Transplant, Cardiology, Pulmonology, Gastroenterology",
                "emergency_services": True
            }
        ]

        for h in hospitals_data:
            existing = Hospital.query.filter_by(name=h["name"]).first()
            if not existing:
                hosp = Hospital(**h)
                db.session.add(hosp)
                db.session.commit()
                print(f"[OK] Created Hospital: {h['name']}")

        # 4. Create an initial sample appointment for the demo patient with Dr. Ananya
        doc_ananya = Doctor.query.filter_by(specialization="Cardiologist").first()
        if patient_user and doc_ananya and patient_user.patient_data:
            existing_appt = Appointment.query.filter_by(patient_id=patient_user.patient_data.id).first()
            if not existing_appt:
                sample_appt = Appointment(
                    patient_id=patient_user.patient_data.id,
                    doctor_id=doc_ananya.id,
                    date=date.today(),
                    time=time(14, 30),
                    reason="Routine Cardiovascular Checkup and Blood Pressure Follow-up",
                    status="scheduled",
                    notes="Patient has mild hypertension history; regular checkup."
                )
                db.session.add(sample_appt)
                db.session.commit()
                print("[OK] Created Sample Upcoming Appointment for Rahul Sharma")

        print("==================================================")
        print(" Database seeding completed successfully! ")
        print(" Demo Patient Login: patient@healthconnect.com / Password123")
        print(" Demo Doctor Login:  dr.ananya@healthconnect.com / DoctorPass123")
        print("==================================================")

if __name__ == "__main__":
    seed_database()
