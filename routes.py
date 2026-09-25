import json
import logging
import os
from datetime import datetime, date, time, timedelta
from functools import wraps
from flask import request, redirect, url_for, flash, session, jsonify, abort, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db, login_manager
from models import User, Patient, Doctor, Appointment, Notification, SymptomCheck, Hospital
from ml_engine.predictor import analyze_patient_symptoms, get_all_symptoms
from ml_engine.nlp_extractor import extract_symptoms_from_text
from ml_engine.symptom_parameters import get_parameters_for_symptom, SYMPTOM_PARAMETER_DEFINITIONS
from ml_engine.image_processor import process_uploaded_image, get_image_path
from config import MAPS_API_KEY

logger = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Decorator for API authentication
def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"success": False, "error": "Authentication required. Please log in."}), 401
        return f(*args, **kwargs)
    return decorated_function

# Notification helpers
def create_notification(user_id, title, message, notification_type=None, related_id=None):
    """Create and persist a notification for a user."""
    try:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            related_id=related_id
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    except Exception as e:
        logger.error(f"Error creating notification: {e}")
        db.session.rollback()
        return None

def get_unread_notification_count(user_id):
    """Get count of unread notifications for a user."""
    try:
        return Notification.query.filter_by(user_id=user_id, read=False).count()
    except Exception:
        return 0

# =====================================================================
# REST APIs (for React.js SPA Frontend)
# =====================================================================

# 1. AUTHENTICATION APIs
@app.route('/api/auth/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        user_type = data.get('user_type', 'patient').strip().lower()
        specialization = data.get('specialization', 'General Physician')
        
        if not email or not password or not name:
            return jsonify({"success": False, "error": "Name, email, and password are required."}), 400
        
        if len(password) < 6:
            return jsonify({"success": False, "error": "Password must be at least 6 characters long."}), 400
            
        if user_type not in ['patient', 'doctor']:
            user_type = 'patient'
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"success": False, "error": "An account with this email already exists."}), 409
            
        new_user = User(email=email, name=name, user_type=user_type)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        if user_type == 'patient':
            patient = Patient(
                user_id=new_user.id,
                gender=data.get('gender', ''),
                phone=data.get('phone', ''),
                city=data.get('city', ''),
                state=data.get('state', '')
            )
            db.session.add(patient)
        else:
            doctor = Doctor(
                user_id=new_user.id,
                specialization=specialization,
                experience_years=int(data.get('experience_years', 5)) if data.get('experience_years') else 5,
                city=data.get('city', ''),
                state=data.get('state', ''),
                phone=data.get('phone', '')
            )
            db.session.add(doctor)
            
        db.session.commit()
        
        # Welcome notification
        create_notification(
            new_user.id,
            "Welcome to HealthConnect!",
            f"Hi {name}, welcome to HealthConnect! You can check symptoms, discover specialist doctors, and book appointments anytime.",
            "general"
        )
        
        # Log the user in
        login_user(new_user, remember=True)
        session['user_id'] = new_user.id
        session['user_type'] = new_user.user_type
        
        return jsonify({
            "success": True,
            "message": "Registration successful!",
            "user": new_user.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error in api_register: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"success": False, "error": "Registration failed due to server error."}), 500

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"success": False, "error": "Email and password are required."}), 400
            
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"success": False, "error": "Invalid email or password."}), 401
            
        login_user(user, remember=True)
        session['user_id'] = user.id
        session['user_type'] = user.user_type
        
        return jsonify({
            "success": True,
            "message": "Login successful!",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in api_login: {e}", exc_info=True)
        return jsonify({"success": False, "error": "Login failed due to server error."}), 500

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    try:
        logout_user()
        session.pop('user_id', None)
        session.pop('user_type', None)
        return jsonify({"success": True, "message": "Logged out successfully."}), 200
    except Exception as e:
        logger.error(f"Error in api_logout: {e}")
        return jsonify({"success": True, "message": "Logged out."}), 200

@app.route('/api/auth/me', methods=['GET'])
def api_current_user():
    if not current_user.is_authenticated:
        return jsonify({"authenticated": False}), 401
    
    unread_count = get_unread_notification_count(current_user.id)
    user_dict = current_user.to_dict()
    user_dict["unread_notifications"] = unread_count
    
    return jsonify({
        "authenticated": True,
        "user": user_dict
    }), 200

# 2. PATIENT PROFILE APIs
@app.route('/api/patient/profile', methods=['GET', 'PUT'])
@api_login_required
def api_patient_profile():
    if current_user.user_type != 'patient':
        return jsonify({"success": False, "error": "Only patients have a patient profile."}), 403
        
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    if not patient:
        patient = Patient(user_id=current_user.id)
        db.session.add(patient)
        db.session.commit()
        
    if request.method == 'GET':
        return jsonify({"success": True, "profile": patient.to_dict()}), 200
        
    # PUT: update profile
    try:
        data = request.get_json() or {}
        if 'name' in data and data['name'].strip():
            current_user.name = data['name'].strip()
            
        if 'gender' in data:
            patient.gender = data['gender']
        if 'blood_group' in data:
            patient.blood_group = data['blood_group']
        if 'address' in data:
            patient.address = data['address']
        if 'city' in data:
            patient.city = data['city']
        if 'state' in data:
            patient.state = data['state']
        if 'phone' in data:
            patient.phone = data['phone']
        if 'emergency_contact' in data:
            patient.emergency_contact = data['emergency_contact']
        if 'date_of_birth' in data and data['date_of_birth']:
            try:
                patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                pass
                
        db.session.commit()
        return jsonify({"success": True, "message": "Profile updated successfully!", "profile": patient.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error updating patient profile: {e}")
        db.session.rollback()
        return jsonify({"success": False, "error": "Failed to update profile."}), 500

# 3. SYMPTOM ANALYSIS & ML APIs
@app.route('/api/symptoms/list', methods=['GET'])
def api_symptoms_list():
    """Returns all 132 symptoms grouped by clinical category."""
    try:
        data = get_all_symptoms()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        logger.error(f"Error fetching symptoms list: {e}")
        return jsonify({"success": False, "error": "Could not load symptoms list."}), 500

@app.route('/api/symptoms/extract-nlp', methods=['POST'])
def api_extract_nlp():
    """
    Extracts structured clinical signals (symptoms, duration, severity, location, visual flag)
    from patient natural language description using deterministic local parser.
    """
    try:
        data = request.get_json() or {}
        text = data.get('text', '').strip()
        result = extract_symptoms_from_text(text)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in api_extract_nlp: {e}", exc_info=True)
        return jsonify({"success": False, "error": "Failed to parse natural problem description."}), 500

@app.route('/api/symptoms/parameters/metadata', methods=['GET'])
def api_symptom_parameters_metadata():
    """
    Returns parameter schemas and validation rules for symptoms.
    Optional query parameter: ?symptom=fever
    """
    try:
        sym_query = request.args.get('symptom')
        if sym_query:
            schema = get_parameters_for_symptom(sym_query)
            return jsonify({"success": True, "data": schema}), 200
        else:
            # Return specialized schemas catalog
            return jsonify({
                "success": True,
                "data": {
                    "definitions": SYMPTOM_PARAMETER_DEFINITIONS
                }
            }), 200
    except Exception as e:
        logger.error(f"Error in api_symptom_parameters_metadata: {e}")
        return jsonify({"success": False, "error": "Could not retrieve parameter metadata."}), 500

@app.route('/api/symptoms/image/<filename>', methods=['GET'])
def api_get_secure_image(filename):
    """
    Serves medical intake images from secure protected storage.
    Enforces cache privacy and prevents directory traversal.
    """
    try:
        path = get_image_path(filename)
        if not path or not os.path.exists(path):
            return jsonify({"success": False, "error": "Image not found."}), 404
            
        response = send_file(path, mimetype="image/jpeg")
        response.headers["Cache-Control"] = "private, no-store, max-age=0"
        return response
    except Exception as e:
        logger.error(f"Error serving secure image: {e}")
        return jsonify({"success": False, "error": "Failed to load image."}), 500

@app.route('/api/symptoms/analyze', methods=['POST'])
def api_analyze_symptoms():
    """
    Next-Generation AI & QML Multimodal Symptom Analysis Endpoint.
    Combines:
    - Patient Details & Context
    - Natural Language Problem Description (Local NLP Extraction)
    - Structured Symptom Selection & Parameter Definitions
    - Optional Secure Medical Visual Image Attachment
    - Dual Classical ML Ensemble (Random Forest + XGBoost)
    - 4-Qubit Quantum Machine Learning Simulator (PennyLane QNN, VQC, QSVM)
    - Emergency Triage Safety System
    """
    try:
        image_metadata = None
        symptoms = []
        patient_details = {}
        symptom_parameters = {}
        problem_description = ""
        age = None
        gender = None
        duration = None
        severity = None
        additional_info = ""

        # Handle multipart/form-data (when image is uploaded) or application/json
        if request.content_type and 'multipart/form-data' in request.content_type:
            form = request.form
            
            # Parse symptoms
            raw_symptoms = form.get('symptoms', '[]')
            try:
                symptoms = json.loads(raw_symptoms) if isinstance(raw_symptoms, str) else list(raw_symptoms)
            except:
                symptoms = [s.strip() for s in raw_symptoms.split(',') if s.strip()]

            # Parse patient details
            raw_pd = form.get('patient_details')
            if raw_pd:
                try:
                    patient_details = json.loads(raw_pd)
                except:
                    patient_details = {}

            # Parse symptom parameters
            raw_sp = form.get('symptom_parameters')
            if raw_sp:
                try:
                    symptom_parameters = json.loads(raw_sp)
                except:
                    symptom_parameters = {}

            problem_description = form.get('problem_description', '')
            age = form.get('age') or patient_details.get('age')
            gender = form.get('gender') or patient_details.get('gender')
            duration = form.get('duration') or patient_details.get('duration')
            severity = form.get('severity') or patient_details.get('severity')
            additional_info = form.get('additional_info', '')

            # Process uploaded image if present
            if 'image' in request.files and request.files['image'].filename:
                img_file = request.files['image']
                img_ok, img_meta, img_err = process_uploaded_image(img_file)
                if not img_ok:
                    return jsonify({"success": False, "error": img_err}), 400
                image_metadata = img_meta

        else:
            # Standard JSON payload
            data = request.get_json() or {}
            symptoms = data.get('symptoms', [])
            patient_details = data.get('patient_details', {})
            symptom_parameters = data.get('symptom_parameters', {})
            problem_description = data.get('problem_description', '')
            age = data.get('age') or patient_details.get('age')
            gender = data.get('gender') or patient_details.get('gender')
            duration = data.get('duration') or patient_details.get('duration')
            severity = data.get('severity') or patient_details.get('severity')
            additional_info = data.get('additional_info', '')

        # If user entered free text problem description but symptoms array is empty, run NLP extraction
        if (not symptoms or len(symptoms) == 0) and problem_description:
            nlp_result = extract_symptoms_from_text(problem_description)
            symptoms = nlp_result.get("extracted_symptoms", [])

        if not symptoms or not isinstance(symptoms, list) or len(symptoms) == 0:
            return jsonify({
                "success": False,
                "error": "Please select at least one symptom or describe your symptoms clearly."
            }), 400

        # Execute hybrid multimodal ML/QML prediction pipeline
        analysis_result = analyze_patient_symptoms(
            symptoms=symptoms,
            age=age,
            gender=gender,
            duration=duration,
            severity=severity,
            additional_info=additional_info,
            patient_details=patient_details,
            problem_description=problem_description,
            symptom_parameters=symptom_parameters,
            image_metadata=image_metadata
        )

        if not analysis_result.get("success", False):
            return jsonify(analysis_result), 400

        # Persist assessment in database for authenticated patient
        symptom_check_id = None
        if current_user.is_authenticated and current_user.user_type == 'patient':
            patient = Patient.query.filter_by(user_id=current_user.id).first()
            if patient:
                sc = SymptomCheck(
                    patient_id=patient.id,
                    symptoms=json.dumps(symptoms),
                    problem_description=problem_description,
                    patient_details=json.dumps(patient_details) if patient_details else None,
                    symptom_parameters=json.dumps(symptom_parameters) if symptom_parameters else None,
                    image_filename=image_metadata.get('filename') if image_metadata else None,
                    image_metadata=json.dumps(image_metadata) if image_metadata else None,
                    analysis=json.dumps(analysis_result),
                    recommendations=json.dumps(analysis_result.get('prevention', [])),
                    severity=analysis_result.get('severity', 'MODERATE')
                )
                db.session.add(sc)
                db.session.commit()
                symptom_check_id = sc.id

                # Create notification
                top_disease = analysis_result.get('top_condition', 'Condition')
                spec = analysis_result.get('specialist', 'General Physician')
                create_notification(
                    current_user.id,
                    f"Health Intake Analysis: {top_disease}",
                    f"Your health check analysis indicated {top_disease} ({analysis_result.get('confidence_percent')}% confidence). Recommended Specialist: {spec}.",
                    "symptom_check",
                    sc.id
                )

        analysis_result["symptom_check_id"] = symptom_check_id
        return jsonify(analysis_result), 200

    except Exception as e:
        logger.error(f"Error in api_analyze_symptoms: {e}", exc_info=True)
        return jsonify({"success": False, "error": "An error occurred during symptom analysis."}), 500

@app.route('/api/symptoms/history', methods=['GET'])
@api_login_required
def api_symptoms_history():
    if current_user.user_type != 'patient':
        return jsonify({"success": False, "error": "Only patients have symptom check history."}), 403
        
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    if not patient:
        return jsonify({"success": True, "history": []}), 200
        
    checks = SymptomCheck.query.filter_by(patient_id=patient.id).order_by(SymptomCheck.created_at.desc()).limit(20).all()
    return jsonify({
        "success": True,
        "history": [c.to_dict() for c in checks]
    }), 200

# 4. DOCTOR DISCOVERY & AVAILABILITY APIs
@app.route('/api/doctors', methods=['GET'])
def api_get_doctors():
    try:
        specialization = request.args.get('specialization', '').strip()
        search = request.args.get('search', '').strip().lower()
        city = request.args.get('city', '').strip().lower()
        
        query = Doctor.query
        
        if specialization:
            query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
            
        doctors = query.all()
        
        result = []
        for doc in doctors:
            doc_dict = doc.to_dict()
            # Search filter on name, specialty, bio, or city
            if search:
                combined_text = f"{doc_dict['name']} {doc_dict['specialization']} {doc_dict['city']} {doc_dict['bio']}".lower()
                if search not in combined_text:
                    continue
            if city and city not in doc_dict['city'].lower():
                continue
            result.append(doc_dict)
            
        return jsonify({"success": True, "doctors": result, "count": len(result)}), 200
    except Exception as e:
        logger.error(f"Error fetching doctors: {e}")
        return jsonify({"success": False, "error": "Failed to load doctors."}), 500

@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def api_get_doctor_detail(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"success": False, "error": "Doctor not found."}), 404
    return jsonify({"success": True, "doctor": doctor.to_dict()}), 200

@app.route('/api/doctors/specializations', methods=['GET'])
def api_doctor_specializations():
    specs = db.session.query(Doctor.specialization).distinct().all()
    spec_list = sorted([s[0] for s in specs if s[0]])
    return jsonify({"success": True, "specializations": spec_list}), 200

@app.route('/api/doctor-availability', methods=['GET'])
def api_doctor_availability():
    doctor_id = request.args.get('doctor_id')
    selected_date = request.args.get('date')
    
    if not doctor_id or not selected_date:
        return jsonify({'error': 'Doctor ID and Date are required.'}), 400
        
    try:
        parsed_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
        
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found.'}), 404
        
    day_abbr = parsed_date.strftime('%a')
    working_days = [d.strip() for d in (doctor.available_days or "Mon,Tue,Wed,Thu,Fri").split(',')]
    
    if day_abbr not in working_days:
        return jsonify({
            'available': False,
            'message': f'Dr. {doctor.user.name if doctor.user else ""} is not available on {parsed_date.strftime("%A")}s.',
            'available_slots': []
        }), 200
        
    # Available hours
    try:
        hours = json.loads(doctor.available_hours) if doctor.available_hours else {"start": "09:00", "end": "17:00"}
    except:
        hours = {"start": "09:00", "end": "17:00"}
        
    existing_appts = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.date == parsed_date,
        Appointment.status.in_(['pending', 'scheduled'])
    ).all()
    booked_times = {a.time.strftime('%H:%M') for a in existing_appts if a.time}
    
    try:
        start_dt = datetime.strptime(hours.get("start", "09:00"), '%H:%M')
        end_dt = datetime.strptime(hours.get("end", "17:00"), '%H:%M')
    except:
        start_dt = datetime.strptime("09:00", '%H:%M')
        end_dt = datetime.strptime("17:00", '%H:%M')
        
    slots = []
    curr = start_dt
    while curr < end_dt:
        time_str = curr.strftime('%H:%M')
        if time_str not in booked_times:
            slots.append({
                "value": time_str,
                "display": curr.strftime('%I:%M %p')
            })
        curr += timedelta(minutes=30)
        
    return jsonify({
        'available': len(slots) > 0,
        'message': f"{len(slots)} consultation slot(s) available" if slots else "No slots remaining for this date.",
        'available_slots': slots
    }), 200

# 5. HOSPITAL DISCOVERY APIs
@app.route('/api/hospitals', methods=['GET'])
def api_get_hospitals():
    try:
        search = request.args.get('search', '').strip().lower()
        emergency_only = request.args.get('emergency', '').strip().lower() in ['true', '1']
        
        query = Hospital.query
        if emergency_only:
            query = query.filter_by(emergency_services=True)
            
        hospitals = query.all()
        result = []
        for h in hospitals:
            h_dict = h.to_dict()
            if search:
                combined_text = f"{h_dict['name']} {h_dict['city']} {h_dict['description']} {' '.join(h_dict['specialties'])}".lower()
                if search not in combined_text:
                    continue
            result.append(h_dict)
            
        return jsonify({"success": True, "hospitals": result, "count": len(result)}), 200
    except Exception as e:
        logger.error(f"Error fetching hospitals: {e}")
        return jsonify({"success": False, "error": "Failed to load hospitals."}), 500

@app.route('/api/hospitals/<int:hospital_id>', methods=['GET'])
def api_get_hospital_detail(hospital_id):
    h = Hospital.query.get(hospital_id)
    if not h:
        return jsonify({"success": False, "error": "Hospital not found."}), 404
    return jsonify({"success": True, "hospital": h.to_dict()}), 200

# 6. APPOINTMENT APIs
@app.route('/api/appointments', methods=['GET', 'POST'])
@api_login_required
def api_appointments():
    if request.method == 'GET':
        if current_user.user_type == 'patient':
            patient = Patient.query.filter_by(user_id=current_user.id).first()
            if not patient:
                return jsonify({"success": True, "appointments": []}), 200
            appts = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
        else:
            doctor = Doctor.query.filter_by(user_id=current_user.id).first()
            if not doctor:
                return jsonify({"success": True, "appointments": []}), 200
            appts = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
            
        return jsonify({
            "success": True,
            "appointments": [a.to_dict() for a in appts]
        }), 200

    # POST: Book new appointment
    try:
        if current_user.user_type != 'patient':
            return jsonify({"success": False, "error": "Only registered patients can book appointments."}), 403
            
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            patient = Patient(user_id=current_user.id)
            db.session.add(patient)
            db.session.commit()
            
        data = request.get_json() or {}
        doctor_id = data.get('doctor_id')
        appt_date_str = data.get('date')
        appt_time_str = data.get('time')
        reason = data.get('reason', 'General Health Consultation')
        
        if not doctor_id or not appt_date_str or not appt_time_str:
            return jsonify({"success": False, "error": "Doctor, date, and time slot are required."}), 400
            
        try:
            parsed_date = datetime.strptime(appt_date_str, '%Y-%m-%d').date()
            parsed_time = datetime.strptime(appt_time_str, '%H:%M').time()
        except ValueError:
            return jsonify({"success": False, "error": "Invalid date or time format."}), 400
            
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({"success": False, "error": "Specified doctor not found."}), 404
            
        new_appt = Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            date=parsed_date,
            time=parsed_time,
            reason=reason,
            status="scheduled"
        )
        db.session.add(new_appt)
        db.session.commit()
        
        # Notifications for both parties
        create_notification(
            doctor.user_id,
            "New Appointment Confirmed",
            f"You have a new consultation confirmed with {current_user.name} on {parsed_date.strftime('%B %d, %Y')} at {parsed_time.strftime('%I:%M %p')}.",
            "appointment",
            new_appt.id
        )
        
        create_notification(
            current_user.id,
            "Appointment Booked Successfully",
            f"Your appointment with Dr. {doctor.user.name if doctor.user else 'Specialist'} ({doctor.specialization}) is confirmed for {parsed_date.strftime('%B %d, %Y')} at {parsed_time.strftime('%I:%M %p')}.",
            "appointment",
            new_appt.id
        )
        
        return jsonify({
            "success": True,
            "message": "Appointment confirmed successfully!",
            "appointment": new_appt.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error booking appointment: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"success": False, "error": "Failed to book appointment."}), 500

@app.route('/api/appointments/<int:appointment_id>/status', methods=['PUT', 'POST'])
@api_login_required
def api_update_appointment_status(appointment_id):
    try:
        appt = Appointment.query.get(appointment_id)
        if not appt:
            return jsonify({"success": False, "error": "Appointment not found."}), 404
            
        # Verify ownership
        is_patient = (current_user.user_type == 'patient' and appt.patient.user_id == current_user.id)
        is_doctor = (current_user.user_type == 'doctor' and appt.doctor.user_id == current_user.id)
        if not is_patient and not is_doctor:
            return jsonify({"success": False, "error": "Unauthorized to modify this appointment."}), 403
            
        data = request.get_json() or {}
        new_status = data.get('status')
        notes = data.get('notes')
        
        allowed_statuses = ['scheduled', 'completed', 'cancelled', 'rejected']
        if new_status not in allowed_statuses:
            return jsonify({"success": False, "error": f"Status must be one of: {allowed_statuses}"}), 400
            
        appt.status = new_status
        if notes:
            appt.notes = notes
            
        db.session.commit()
        
        # Notify the other party
        recipient_id = appt.doctor.user_id if is_patient else appt.patient.user_id
        create_notification(
            recipient_id,
            f"Appointment Status Updated: {new_status.capitalize()}",
            f"The appointment on {appt.date.strftime('%B %d, %Y')} has been updated to status: {new_status}.",
            "appointment",
            appt.id
        )
        
        return jsonify({
            "success": True,
            "message": f"Appointment status updated to {new_status}.",
            "appointment": appt.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating appointment status: {e}")
        db.session.rollback()
        return jsonify({"success": False, "error": "Failed to update appointment status."}), 500

@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
@api_login_required
def api_cancel_appointment(appointment_id):
    try:
        appt = Appointment.query.get(appointment_id)
        if not appt:
            return jsonify({"success": False, "error": "Appointment not found."}), 404
            
        is_patient = (current_user.user_type == 'patient' and appt.patient.user_id == current_user.id)
        is_doctor = (current_user.user_type == 'doctor' and appt.doctor.user_id == current_user.id)
        if not is_patient and not is_doctor:
            return jsonify({"success": False, "error": "Unauthorized to cancel this appointment."}), 403
            
        appt.status = "cancelled"
        db.session.commit()
        
        return jsonify({"success": True, "message": "Appointment cancelled successfully."}), 200
    except Exception as e:
        logger.error(f"Error cancelling appointment: {e}")
        db.session.rollback()
        return jsonify({"success": False, "error": "Failed to cancel appointment."}), 500

# 7. NOTIFICATION APIs
@app.route('/api/notifications', methods=['GET'])
@api_login_required
def api_get_notifications():
    try:
        notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(50).all()
        unread_count = get_unread_notification_count(current_user.id)
        return jsonify({
            "success": True,
            "notifications": [n.to_dict() for n in notifs],
            "unread_count": unread_count
        }), 200
    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
        return jsonify({"success": False, "error": "Failed to fetch notifications."}), 500

@app.route('/api/notifications/<int:notification_id>/read', methods=['POST', 'PUT'])
@api_login_required
def api_mark_single_notification_read(notification_id):
    try:
        notif = Notification.query.get(notification_id)
        if not notif or notif.user_id != current_user.id:
            return jsonify({"success": False, "error": "Notification not found."}), 404
            
        notif.read = True
        db.session.commit()
        return jsonify({"success": True, "message": "Notification marked as read."}), 200
    except Exception as e:
        logger.error(f"Error marking notification read: {e}")
        db.session.rollback()
        return jsonify({"success": False, "error": "Could not mark notification as read."}), 500

@app.route('/api/notifications/mark-all-read', methods=['POST'])
@api_login_required
def api_mark_all_read():
    try:
        Notification.query.filter_by(user_id=current_user.id, read=False).update({"read": True})
        db.session.commit()
        return jsonify({"success": True, "message": "All notifications marked as read."}), 200
    except Exception as e:
        logger.error(f"Error marking all notifications read: {e}")
        db.session.rollback()
        return jsonify({"success": False, "error": "Failed to mark all as read."}), 500

@app.route('/api/notifications/clear-all', methods=['POST', 'DELETE'])
@api_login_required
def api_clear_all_notifications():
    try:
        Notification.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return jsonify({"success": True, "message": "All notifications cleared."}), 200
    except Exception as e:
        logger.error(f"Error clearing notifications: {e}")
        db.session.rollback()
        return jsonify({"success": False, "error": "Failed to clear notifications."}), 500

# 8. PATIENT DASHBOARD METRICS API
@app.route('/api/patient/dashboard', methods=['GET'])
@api_login_required
def api_patient_dashboard():
    if current_user.user_type != 'patient':
        return jsonify({"success": False, "error": "Only patients have patient dashboard."}), 403
        
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    if not patient:
        patient = Patient(user_id=current_user.id)
        db.session.add(patient)
        db.session.commit()
        
    # Upcoming appointments
    upcoming_appts = Appointment.query.filter_by(patient_id=patient.id).filter(
        Appointment.status.in_(['scheduled', 'pending']),
        Appointment.date >= date.today()
    ).order_by(Appointment.date, Appointment.time).all()
    
    # Recent symptom analyses
    recent_checks = SymptomCheck.query.filter_by(patient_id=patient.id).order_by(
        SymptomCheck.created_at.desc()
    ).limit(3).all()
    
    unread_notifs = get_unread_notification_count(current_user.id)
    
    return jsonify({
        "success": True,
        "patient": patient.to_dict(),
        "upcoming_appointments": [a.to_dict() for a in upcoming_appts],
        "recent_symptom_checks": [c.to_dict() for c in recent_checks],
        "unread_notifications": unread_notifs,
        "stats": {
            "total_appointments": Appointment.query.filter_by(patient_id=patient.id).count(),
            "completed_appointments": Appointment.query.filter_by(patient_id=patient.id, status='completed').count(),
            "total_health_checks": SymptomCheck.query.filter_by(patient_id=patient.id).count()
        }
    }), 200

# 9. DOCTOR DASHBOARD METRICS API
@app.route('/api/doctor/dashboard', methods=['GET'])
@api_login_required
def api_doctor_dashboard():
    if current_user.user_type != 'doctor':
        return jsonify({"success": False, "error": "Only doctors have doctor dashboard."}), 403
        
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if not doctor:
        return jsonify({"success": False, "error": "Doctor profile not found."}), 404
        
    upcoming_appts = Appointment.query.filter_by(doctor_id=doctor.id).filter(
        Appointment.status.in_(['scheduled', 'pending']),
        Appointment.date >= date.today()
    ).order_by(Appointment.date, Appointment.time).all()
    
    today_appts = Appointment.query.filter_by(doctor_id=doctor.id, date=date.today()).all()
    
    return jsonify({
        "success": True,
        "doctor": doctor.to_dict(),
        "today_appointments": [a.to_dict() for a in today_appts],
        "upcoming_appointments": [a.to_dict() for a in upcoming_appts],
        "stats": {
            "total_consultations": Appointment.query.filter_by(doctor_id=doctor.id).count(),
            "completed_consultations": Appointment.query.filter_by(doctor_id=doctor.id, status='completed').count(),
            "today_count": len(today_appts)
        }
    }), 200

# =====================================================================
# API Root Health Route
# =====================================================================

@app.route('/')
def home():
    return jsonify({
        "name": "HealthConnect API",
        "status": "online",
        "version": "2.0.0",
        "documentation": "/api/*",
        "frontend_url": "http://localhost:5173"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')), debug=True)
