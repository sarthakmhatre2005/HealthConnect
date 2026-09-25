"""
Comprehensive Backend & ML Test Suite for HealthConnectPlatform
Tests all REST APIs, edge cases, error handling, session management, and ML inference.
"""

import sys
import os
import json

# Ensure current directory is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models import User, Patient, Doctor, Appointment, Hospital, Notification, SymptomCheck
import routes

client = app.test_client()

def run_test_suite():
    print("================================================================")
    print(" HEALTHCONNECT FULL-STACK BACKEND & ML TEST SUITE               ")
    print("================================================================")
    
    passed_tests = 0
    total_tests = 0
    
    def test(name, condition, error_msg=""):
        nonlocal passed_tests, total_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f" [PASS] {name}")
            return True
        else:
            print(f" [FAIL] {name}: {error_msg}")
            return False

    # -------------------------------------------------------------
    # 1. ML Symptom List API
    # -------------------------------------------------------------
    res = client.get('/api/symptoms/list')
    data = res.get_json() or {}
    test("1. Symptoms List API returns 200 and 132 symptoms", 
         res.status_code == 200 and len(data.get('data', {}).get('symptoms', [])) == 132,
         f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 2. ML Inference: Standard Medical Condition
    # -------------------------------------------------------------
    res = client.post('/api/symptoms/analyze', json={
        'symptoms': ['itching', 'skin_rash', 'nodal_skin_eruptions'],
        'age': 28,
        'gender': 'Female',
        'duration': '3 days',
        'severity': 'Moderate'
    })
    data = res.get_json() or {}
    test("2. ML Inference (Dermatological): Predicts Fungal Infection with Top-3",
         res.status_code == 200 and len(data.get('predictions', [])) == 3 and data.get('top_condition') == 'Fungal infection',
         f"Got: {data.get('top_condition')}")

    # -------------------------------------------------------------
    # 3. ML Inference: Cardiac Emergency Detection
    # -------------------------------------------------------------
    res = client.post('/api/symptoms/analyze', json={
        'symptoms': ['chest_pain', 'breathlessness', 'sweating'],
        'age': 60,
        'gender': 'Male',
        'duration': '1 hour',
        'severity': 'Severe'
    })
    data = res.get_json() or {}
    test("3. ML Inference (Cardiac Emergency): Triggers emergency=True & Cardiologist",
         res.status_code == 200 and data.get('emergency') is True and data.get('specialist') == 'Cardiologist',
         f"Emergency: {data.get('emergency')}, Specialist: {data.get('specialist')}")

    # -------------------------------------------------------------
    # 4. ML Inference: Edge Case - Empty Symptoms
    # -------------------------------------------------------------
    res = client.post('/api/symptoms/analyze', json={'symptoms': []})
    test("4. ML Inference Edge Case: Empty symptoms returns 400 error",
         res.status_code == 400,
         f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 5. ML Inference: Edge Case - Unknown Symptoms
    # -------------------------------------------------------------
    res = client.post('/api/symptoms/analyze', json={'symptoms': ['completely_fabricated_symptom_xyz']})
    test("5. ML Inference Edge Case: Unknown symptoms returns clean 400 error",
         res.status_code == 400 and res.get_json().get('success') is False,
         f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 6. Auth API: Patient Login with Demo Credentials
    # -------------------------------------------------------------
    res = client.post('/api/auth/login', json={
        'email': 'patient@healthconnect.com',
        'password': 'Password123'
    })
    user_data = res.get_json() or {}
    test("6. Auth Login: Patient demo account logs in successfully",
         res.status_code == 200 and user_data.get('user', {}).get('user_type') == 'patient',
         f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 7. Auth API: Current User Session Check (/api/auth/me)
    # -------------------------------------------------------------
    res = client.get('/api/auth/me')
    me_data = res.get_json() or {}
    test("7. Auth Me: Session persists and returns authenticated user",
         res.status_code == 200 and me_data.get('authenticated') is True,
         f"Authenticated: {me_data.get('authenticated')}")

    # -------------------------------------------------------------
    # 8. Patient Profile API: GET Profile
    # -------------------------------------------------------------
    res = client.get('/api/patient/profile')
    prof_data = res.get_json() or {}
    test("8. Patient Profile: Successfully retrieves profile data",
         res.status_code == 200 and prof_data.get('profile', {}).get('city') is not None,
         f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 9. Patient Profile API: PUT Update
    # -------------------------------------------------------------
    res = client.put('/api/patient/profile', json={
        'phone': '+91 91234 56789',
        'city': 'Bengaluru',
        'state': 'Karnataka',
        'blood_group': 'B+'
    })
    upd_prof = res.get_json() or {}
    test("9. Patient Profile: Successfully updates profile fields",
         res.status_code == 200 and upd_prof.get('profile', {}).get('city') == 'Bengaluru',
         f"City: {upd_prof.get('profile', {}).get('city')}")

    # -------------------------------------------------------------
    # 10. Patient Dashboard API
    # -------------------------------------------------------------
    res = client.get('/api/patient/dashboard')
    dash_data = res.get_json() or {}
    test("10. Patient Dashboard: Returns upcoming appointments and stats",
         res.status_code == 200 and 'upcoming_appointments' in dash_data and 'stats' in dash_data,
         f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 11. Doctors API: List & Filters
    # -------------------------------------------------------------
    res = client.get('/api/doctors')
    doc_data = res.get_json() or {}
    docs = doc_data.get('doctors', [])
    test("11. Doctors API: Returns verified doctors list",
         res.status_code == 200 and len(docs) >= 8,
         f"Count: {len(docs)}")

    # -------------------------------------------------------------
    # 12. Doctor Specializations API
    # -------------------------------------------------------------
    res = client.get('/api/doctors/specializations')
    spec_data = res.get_json() or {}
    specs = spec_data.get('specializations', [])
    test("12. Doctor Specializations API: Returns unique specializations",
         res.status_code == 200 and len(specs) >= 5,
         f"Specs: {specs}")

    # -------------------------------------------------------------
    # 13. Doctor Detail API
    # -------------------------------------------------------------
    first_doc_id = docs[0]['id'] if docs else 1
    res = client.get(f'/api/doctors/{first_doc_id}')
    doc_detail = res.get_json() or {}
    test(f"13. Doctor Detail API: Returns doctor #{first_doc_id} profile",
         res.status_code == 200 and doc_detail.get('doctor', {}).get('id') == first_doc_id,
         f"Doctor ID: {doc_detail.get('doctor', {}).get('id')}")

    # -------------------------------------------------------------
    # 14. Doctor Availability API
    # -------------------------------------------------------------
    res = client.get(f'/api/doctor-availability?doctor_id={first_doc_id}&date=2026-09-14')
    avail_data = res.get_json() or {}
    test("14. Doctor Availability: Generates real appointment time slots",
         res.status_code == 200 and 'available_slots' in avail_data,
         f"Available: {avail_data.get('available')}")

    # -------------------------------------------------------------
    # 15. Hospitals API: List & Emergency Filter
    # -------------------------------------------------------------
    res = client.get('/api/hospitals?emergency=true')
    hosp_data = res.get_json() or {}
    hosps = hosp_data.get('hospitals', [])
    test("15. Hospitals API: Filters for 24/7 Emergency medical centers",
         res.status_code == 200 and len(hosps) >= 3 and all(h.get('emergency_services') for h in hosps),
         f"Count: {len(hosps)}")

    # -------------------------------------------------------------
    # 16. Hospital Detail API
    # -------------------------------------------------------------
    first_hosp_id = hosps[0]['id'] if hosps else 1
    res = client.get(f'/api/hospitals/{first_hosp_id}')
    hosp_detail = res.get_json() or {}
    test(f"16. Hospital Detail API: Returns hospital #{first_hosp_id} data",
         res.status_code == 200 and hosp_detail.get('hospital', {}).get('id') == first_hosp_id,
         f"Hosp: {hosp_detail.get('hospital', {}).get('name')}")

    # -------------------------------------------------------------
    # 17. Appointment Booking API
    # -------------------------------------------------------------
    res = client.post('/api/appointments', json={
        'doctor_id': first_doc_id,
        'date': '2026-09-16',
        'time': '10:30',
        'reason': 'Health checkup and diagnostic follow-up'
    })
    appt_data = res.get_json() or {}
    new_appt_id = appt_data.get('appointment', {}).get('id')
    test("17. Appointment Booking API: Confirms appointment with status 'scheduled'",
         res.status_code == 201 and appt_data.get('appointment', {}).get('status') == 'scheduled',
         f"Status: {res.status_code}, Appt: {appt_data.get('appointment')}")

    # -------------------------------------------------------------
    # 18. Appointments List API
    # -------------------------------------------------------------
    res = client.get('/api/appointments')
    appts_list = res.get_json() or {}
    test("18. Appointments List API: Returns patient appointment list",
         res.status_code == 200 and len(appts_list.get('appointments', [])) >= 1,
         f"Count: {len(appts_list.get('appointments', []))}")

    # -------------------------------------------------------------
    # 19. Appointment Status Update API
    # -------------------------------------------------------------
    if new_appt_id:
        res = client.put(f'/api/appointments/{new_appt_id}/status', json={
            'status': 'completed',
            'notes': 'Consultation completed successfully with diagnosis review.'
        })
        test("19. Appointment Status Update: Marks appointment as completed",
             res.status_code == 200 and res.get_json().get('appointment', {}).get('status') == 'completed',
             f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 20. Notifications API: List
    # -------------------------------------------------------------
    res = client.get('/api/notifications')
    notif_data = res.get_json() or {}
    notifs = notif_data.get('notifications', [])
    test("20. Notifications API: Returns user notification list",
         res.status_code == 200 and len(notifs) >= 1,
         f"Count: {len(notifs)}")

    # -------------------------------------------------------------
    # 21. Notification Mark as Read API
    # -------------------------------------------------------------
    if notifs:
        target_notif_id = notifs[0]['id']
        res = client.post(f'/api/notifications/{target_notif_id}/read')
        test(f"21. Notification Read API: Marks notification #{target_notif_id} as read",
             res.status_code == 200 and res.get_json().get('success') is True,
             f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 22. Notification Mark All Read API
    # -------------------------------------------------------------
    res = client.post('/api/notifications/mark-all-read')
    test("22. Notification Mark All Read: Successfully marks all read",
         res.status_code == 200 and res.get_json().get('success') is True,
         f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 23. Symptom Check History API
    # -------------------------------------------------------------
    res = client.get('/api/symptoms/history')
    hist_data = res.get_json() or {}
    test("23. Symptom History API: Returns history of patient AI checks",
         res.status_code == 200 and 'history' in hist_data,
         f"Count: {len(hist_data.get('history', []))}")

    # -------------------------------------------------------------
    # 24. Auth Logout API
    # -------------------------------------------------------------
    res = client.post('/api/auth/logout')
    test("24. Auth Logout API: Clears session successfully",
         res.status_code == 200,
         f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 25. Protected Route Access when Logged Out
    # -------------------------------------------------------------
    res = client.get('/api/patient/dashboard')
    test("25. Security Check: Accessing protected route logged-out returns 401",
         res.status_code == 401,
         f"Status: {res.status_code}")

    # -------------------------------------------------------------
    # 26. Doctor Login & Doctor Dashboard API
    # -------------------------------------------------------------
    res = client.post('/api/auth/login', json={
        'email': 'dr.ananya@healthconnect.com',
        'password': 'DoctorPass123'
    })
    test("26. Doctor Login: Demo doctor logs in successfully",
         res.status_code == 200 and res.get_json().get('user', {}).get('user_type') == 'doctor',
         f"Status: {res.status_code}")

    res = client.get('/api/doctor/dashboard')
    doc_dash = res.get_json() or {}
    test("27. Doctor Dashboard API: Returns consultations and stats",
         res.status_code == 200 and 'upcoming_appointments' in doc_dash and 'stats' in doc_dash,
         f"Status: {res.status_code}")

    # Logout doctor
    client.post('/api/auth/logout')

    # -------------------------------------------------------------
    # 28. New User Registration Test
    # -------------------------------------------------------------
    import random
    rand_id = random.randint(10000, 99999)
    res = client.post('/api/auth/register', json={
        'name': f'Hackathon Judge {rand_id}',
        'email': f'judge{rand_id}@sih.gov.in',
        'password': 'StrongPassword123',
        'user_type': 'patient',
        'city': 'New Delhi',
        'state': 'Delhi'
    })
    reg_data = res.get_json() or {}
    test("28. New User Registration: Creates account and logs in automatically",
         res.status_code == 201 and reg_data.get('user', {}).get('email') == f'judge{rand_id}@sih.gov.in',
         f"Status: {res.status_code}")

    # Logout newly registered user
    client.post('/api/auth/logout')

    print("================================================================")
    print(f" TEST RESULTS: {passed_tests}/{total_tests} TESTS PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("================================================================")
    
    if passed_tests == total_tests:
        print(" >>> ALL BACKEND, ML, AND SECURITY TESTS PASSED! <<<")
        return 0
    else:
        print(" >>> SOME TESTS FAILED! PLEASE REVIEW OUTPUT ABOVE. <<<")
        return 1

if __name__ == '__main__':
    exit_code = run_test_suite()
    sys.exit(exit_code)
