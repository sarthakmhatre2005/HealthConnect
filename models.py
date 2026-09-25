from datetime import datetime, date, time
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'patient' or 'doctor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    patient_data = db.relationship('Patient', backref='user', uselist=False, cascade="all, delete-orphan")
    doctor_data = db.relationship('Doctor', backref='user', uselist=False, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        data = {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "user_type": self.user_type,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        if self.user_type == 'patient' and self.patient_data:
            data["profile"] = self.patient_data.to_dict()
        elif self.user_type == 'doctor' and self.doctor_data:
            data["profile"] = self.doctor_data.to_dict()
        return data

    def __repr__(self):
        return f'<User {self.email}>'

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    emergency_contact = db.Column(db.String(15))
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic', 
                                   foreign_keys='Appointment.patient_id')
    symptom_checks = db.relationship('SymptomCheck', backref='patient', lazy='dynamic')
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.user.name if self.user else None,
            "email": self.user.email if self.user else None,
            "date_of_birth": self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            "gender": self.gender,
            "blood_group": self.blood_group,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "emergency_contact": self.emergency_contact
        }

    def __repr__(self):
        return f'<Patient {self.user.name if self.user else self.id}>'

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    license_number = db.Column(db.String(50))
    experience_years = db.Column(db.Integer)
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Availability days (CSV string: "Mon,Tue,Wed")
    available_days = db.Column(db.String(100), default="Mon,Tue,Wed,Thu,Fri")
    # Availability times (JSON string: {"start": "09:00", "end": "17:00"})
    available_hours = db.Column(db.String(100), default='{"start": "09:00", "end": "17:00"}')
    
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic',
                                   foreign_keys='Appointment.doctor_id')
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.user.name if self.user else "Dr. Verified Specialist",
            "email": self.user.email if self.user else None,
            "specialization": self.specialization,
            "bio": self.bio or f"Experienced specialist in {self.specialization} dedicated to evidence-based clinical care.",
            "license_number": self.license_number or "MED-REG-2024",
            "experience_years": self.experience_years or 8,
            "address": self.address or "Healthcare Complex",
            "city": self.city or "Central Medical Hub",
            "state": self.state or "Medical District",
            "phone": self.phone or "+91 98765 43210",
            "latitude": self.latitude,
            "longitude": self.longitude,
            "available_days": self.available_days or "Mon,Tue,Wed,Thu,Fri",
            "available_hours": self.available_hours or '{"start": "09:00", "end": "17:00"}'
        }

    def __repr__(self):
        return f'<Doctor {self.user.name if self.user else self.id} ({self.specialization})>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(15), default='pending')  # pending, scheduled, completed, cancelled, rejected
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "patient_name": self.patient.user.name if self.patient and self.patient.user else "Patient",
            "patient_phone": self.patient.phone if self.patient else "",
            "doctor_name": self.doctor.user.name if self.doctor and self.doctor.user else "Doctor",
            "doctor_specialization": self.doctor.specialization if self.doctor else "Specialist",
            "doctor_city": self.doctor.city if self.doctor else "",
            "date": self.date.strftime('%Y-%m-%d') if self.date else None,
            "time": self.time.strftime('%H:%M') if self.time else None,
            "formatted_time": self.time.strftime('%I:%M %p') if self.time else None,
            "reason": self.reason or "Routine Medical Consultation",
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Appointment {self.id}: {self.patient_id} with Dr {self.doctor_id}>'

class SymptomCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)  # JSON string of symptoms
    problem_description = db.Column(db.Text, nullable=True)  # Natural language problem description
    patient_details = db.Column(db.Text, nullable=True)  # JSON string: age, sex, conditions, meds, allergies
    symptom_parameters = db.Column(db.Text, nullable=True)  # JSON string: per-symptom responses
    image_filename = db.Column(db.String(255), nullable=True)  # Secure stored filename
    image_metadata = db.Column(db.Text, nullable=True)  # JSON string: visual metadata
    analysis = db.Column(db.Text)  # JSON string of analysis result
    recommendations = db.Column(db.Text)  # JSON string of recommendations
    severity = db.Column(db.String(20))  # MILD, MODERATE, SEVERE, CRITICAL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        try:
            parsed_symptoms = json.loads(self.symptoms) if self.symptoms else []
        except:
            parsed_symptoms = [self.symptoms] if self.symptoms else []

        try:
            parsed_patient_details = json.loads(self.patient_details) if self.patient_details else {}
        except:
            parsed_patient_details = {}

        try:
            parsed_symptom_parameters = json.loads(self.symptom_parameters) if self.symptom_parameters else {}
        except:
            parsed_symptom_parameters = {}

        try:
            parsed_image_metadata = json.loads(self.image_metadata) if self.image_metadata else None
        except:
            parsed_image_metadata = None

        try:
            parsed_analysis = json.loads(self.analysis) if self.analysis else {}
        except:
            parsed_analysis = {"raw": self.analysis}

        try:
            parsed_recommendations = json.loads(self.recommendations) if self.recommendations else []
        except:
            parsed_recommendations = []

        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "symptoms": parsed_symptoms,
            "problem_description": self.problem_description or "",
            "patient_details": parsed_patient_details,
            "symptom_parameters": parsed_symptom_parameters,
            "image_filename": self.image_filename,
            "image_metadata": parsed_image_metadata,
            "analysis": parsed_analysis,
            "recommendations": parsed_recommendations,
            "severity": self.severity or "MODERATE",
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "formatted_date": self.created_at.strftime('%b %d, %Y %I:%M %p') if self.created_at else ""
        }

    def __repr__(self):
        return f'<SymptomCheck {self.id} by Patient {self.patient_id}>'

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    notification_type = db.Column(db.String(20))  # appointment, symptom_check, etc.
    related_id = db.Column(db.Integer)  # Related entity ID (e.g., appointment_id)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "read": self.read,
            "notification_type": self.notification_type,
            "related_id": self.related_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "formatted_date": self.created_at.strftime('%b %d, %Y %I:%M %p') if self.created_at else ""
        }

    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120))
    website = db.Column(db.String(120))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.Text)
    specialties = db.Column(db.String(200))  # CSV string of specialties
    emergency_services = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        specialties_list = [s.strip() for s in self.specialties.split(",")] if self.specialties else []
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": self.description,
            "specialties": specialties_list,
            "emergency_services": bool(self.emergency_services)
        }

    def __repr__(self):
        return f'<Hospital {self.name}>'
