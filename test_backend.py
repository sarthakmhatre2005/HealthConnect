import sys
import json
from app import app, db
import routes

client = app.test_client()

print("==================================================")
print(" RUNNING HEALTHCONNECT BACKEND API TEST SUITE     ")
print("==================================================")

# 1. Test Symptom list
res = client.get('/api/symptoms/list')
assert res.status_code == 200, f'Symptoms list failed: {res.status_code}'
data = res.get_json()
num_syms = len(data['data']['symptoms'])
assert num_syms == 132, f'Expected 132 symptoms, got {num_syms}'
print(f"[PASS] Symptom list API: {num_syms} symptoms verified")

# 2. Test ML Symptom Analysis (Cardiac Emergency)
res = client.post('/api/symptoms/analyze', json={
    'symptoms': ['chest pain', 'shortness of breath', 'sweating'],
    'age': 55,
    'gender': 'Male',
    'duration': '1-2 hours',
    'severity': 'Severe'
})
assert res.status_code == 200, f'Analysis failed: {res.status_code}'
data = res.get_json()
assert data['emergency'] == True, 'Cardiac distress should trigger emergency=True'
assert data['specialist'] == 'Cardiologist', f"Expected Cardiologist, got {data['specialist']}"
assert len(data['predictions']) == 3, 'Expected top 3 predictions'
print(f"[PASS] ML Symptom Analysis: Top Condition = {data['top_condition']} (Prob: {data['confidence_percent']}%), Emergency = {data['emergency']}, Specialist = {data['specialist']}")

# 3. Test Doctors API
res = client.get('/api/doctors')
assert res.status_code == 200
docs = res.get_json()['doctors']
assert len(docs) >= 8, f'Expected at least 8 doctors, got {len(docs)}'
print(f"[PASS] Doctors API: found {len(docs)} specialists across multiple fields")

# 4. Test Doctor Detail API
res = client.get(f'/api/doctors/{docs[0]["id"]}')
assert res.status_code == 200
doc_detail = res.get_json()['doctor']
assert doc_detail['name'] == docs[0]['name']
print(f"[PASS] Doctor Detail API: verified {doc_detail['name']} ({doc_detail['specialization']})")

# 5. Test Hospitals API
res = client.get('/api/hospitals')
assert res.status_code == 200
hosps = res.get_json()['hospitals']
assert len(hosps) >= 6, f'Expected at least 6 hospitals, got {len(hosps)}'
print(f"[PASS] Hospitals API: found {len(hosps)} accredited hospitals")

# 6. Test Auth Login
res = client.post('/api/auth/login', json={
    'email': 'patient@healthconnect.com',
    'password': 'Password123'
})
assert res.status_code == 200, f'Login failed: {res.status_code}'
user = res.get_json()['user']
assert user['email'] == 'patient@healthconnect.com'
print(f"[PASS] Auth Login API: authenticated as {user['name']} ({user['email']})")

# 7. Test Auth Me
res = client.get('/api/auth/me')
assert res.status_code == 200
me = res.get_json()
assert me['authenticated'] == True
print(f"[PASS] Auth Me API: session state verified, user ID {me['user']['id']}")

# 8. Test Patient Dashboard
res = client.get('/api/patient/dashboard')
assert res.status_code == 200
dash = res.get_json()
print(f"[PASS] Patient Dashboard API: upcoming appointments = {len(dash['upcoming_appointments'])}")

# 9. Test Appointment Booking
res = client.post('/api/appointments', json={
    'doctor_id': docs[0]['id'],
    'date': '2026-09-15',
    'time': '11:00',
    'reason': 'Follow-up Consultation'
})
assert res.status_code == 201, f'Appointment booking failed: {res.status_code}'
booked_appt = res.get_json()['appointment']
print(f"[PASS] Appointment Booking API: confirmed appt #{booked_appt['id']} for {booked_appt['date']}")

# 10. Test Notifications
res = client.get('/api/notifications')
assert res.status_code == 200
notifs = res.get_json()['notifications']
assert len(notifs) >= 1
print(f"[PASS] Notifications API: user has {len(notifs)} notification(s)")

# 11. Test Patient Profile Update
res = client.put('/api/patient/profile', json={
    'phone': '+91 99999 88888',
    'city': 'Mumbai',
    'blood_group': 'O+'
})
assert res.status_code == 200
print(f"[PASS] Patient Profile API: profile updated successfully")

# 12. Test Logout
res = client.post('/api/auth/logout')
assert res.status_code == 200
res_me = client.get('/api/auth/me')
assert res_me.get_json()['authenticated'] == False
print(f"[PASS] Auth Logout API: successfully signed out")

print("\n==================================================")
print(" ALL 12 CORE BACKEND & ML APIS PASSED WITH 100%!  ")
print("==================================================")
