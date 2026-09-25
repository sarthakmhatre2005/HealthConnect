"""
Test Suite for HealthConnect Next-Generation Symptom Checker
Validates the 15 required test cases:
1. Fever
2. Headache
3. Cough
4. Chest pain
5. Abdominal pain
6. Skin rash
7. Skin problem with image
8. Skin problem without image
9. Multiple symptoms
10. Missing required information
11. Invalid parameter handling
12. Large image rejection
13. Unsupported image format rejection
14. Emergency combination
15. Normal non-emergency case
"""

import os
import io
import json
from PIL import Image
from app import app
import routes

client = app.test_client()

def run_tests():
    print("==================================================================")
    print(" HEALTHCONNECT NEXT-GEN SYMPTOM CHECKER: 15-CASE TEST SUITE       ")
    print("==================================================================")
    
    passed = 0
    total = 0

    def check(name, condition, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f" [PASS] Case {total}: {name}")
        else:
            print(f" [FAIL] Case {total}: {name} -> {details}")

    # Helper to generate in-memory test image
    def make_test_image(format="JPEG", size=(200, 200), color=(220, 50, 50)):
        buf = io.BytesIO()
        img = Image.new("RGB", size, color)
        img.save(buf, format=format)
        buf.seek(0)
        return buf

    # Case 1: Fever with parameters
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["high_fever", "chills"],
        "patient_details": {"age": 28, "gender": "Male"},
        "symptom_parameters": {
            "high_fever": {
                "temperature": 102.4,
                "temperature_unit": "°F",
                "duration": "1-2 days",
                "chills": True,
                "severity": 7
            }
        }
    })
    d = res.get_json() or {}
    check("Fever with structured parameters", res.status_code == 200 and len(d.get("predictions", [])) > 0 and d.get("quantum_analysis", {}).get("qubits") == 4)

    # Case 2: Headache with parameters
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["headache"],
        "patient_details": {"age": 35, "gender": "Female"},
        "symptom_parameters": {
            "headache": {
                "location": "One side / Temple (Unilateral)",
                "pain_character": "Pulsating / Throbbing",
                "light_sensitivity": True,
                "severity": 8
            }
        }
    })
    d = res.get_json() or {}
    check("Headache with migraine parameters", res.status_code == 200 and "headache" in [s.lower() for s in d.get("input_symptoms", [])])

    # Case 3: Cough with parameters
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["cough", "throat_irritation"],
        "symptom_parameters": {
            "cough": {
                "cough_type": "Dry & tickly (non-productive)",
                "duration": "1 to 3 weeks",
                "severity": 5
            }
        }
    })
    d = res.get_json() or {}
    check("Cough with respiratory parameters", res.status_code == 200 and d.get("specialist") is not None)

    # Case 4: Chest pain with parameters
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["chest_pain"],
        "patient_details": {"age": 52, "gender": "Male"},
        "symptom_parameters": {
            "chest_pain": {
                "location": "Center of chest behind breastbone (Substernal)",
                "pain_character": "Heavy pressure, crushing, squeezing or tightness",
                "radiation": ["Left arm or left shoulder"],
                "breathlessness": True,
                "severity": 9
            }
        }
    })
    d = res.get_json() or {}
    check("Chest pain with radiating pain (Triggers Emergency Alert)", res.status_code == 200 and d.get("emergency") is True and d.get("severity") == "CRITICAL")

    # Case 5: Abdominal pain with parameters
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["abdominal_pain", "vomiting"],
        "symptom_parameters": {
            "abdominal_pain": {
                "location": "Right lower abdomen (near groin/hip)",
                "pain_character": "Sharp, knife-like, or stabbing",
                "nausea_vomiting": True,
                "severity": 8
            }
        }
    })
    d = res.get_json() or {}
    check("Abdominal pain with gastrointestinal parameters", res.status_code == 200 and d.get("specialist") in ["Gastroenterologist", "General Physician", "Hepatologist"])

    # Case 6: Skin rash
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["skin_rash", "itching"],
        "symptom_parameters": {
            "skin_rash": {
                "location": ["Arms & Forearms"],
                "appearance": "Raised red bumps or hives (Papules/Wheals)",
                "itching": "Moderate persistent itching",
                "spread": "Spreading slowly over several days",
                "severity": 6
            }
        }
    })
    d = res.get_json() or {}
    check("Skin rash with dermatological parameters", res.status_code == 200 and d.get("specialist") == "Dermatologist")

    # Case 7: Skin problem with image upload (multipart)
    img_buf = make_test_image("JPEG", (300, 300), color=(230, 80, 80))
    res = client.post('/api/symptoms/analyze', data={
        "symptoms": json.dumps(["skin_rash", "itching"]),
        "problem_description": "Red itchy patch on left forearm for 3 days",
        "patient_details": json.dumps({"age": 30, "gender": "Female"}),
        "symptom_parameters": json.dumps({"skin_rash": {"location": ["Arms & Forearms"], "itching": "Moderate persistent itching"}}),
        "image": (img_buf, "skin_rash.jpg", "image/jpeg")
    }, content_type="multipart/form-data")
    d = res.get_json() or {}
    check("Skin problem with verified image attachment", res.status_code == 200 and d.get("image_analyzed") is True and d.get("image_details", {}).get("visual_features") is not None)

    # Case 8: Skin problem without image
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["skin_rash"],
        "problem_description": "Dry itchy red spot on cheek"
    })
    d = res.get_json() or {}
    check("Skin problem without image", res.status_code == 200 and d.get("image_analyzed") is False)

    # Case 9: Multiple symptoms across categories
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["high_fever", "headache", "cough", "fatigue"],
        "patient_details": {"age": 42, "gender": "Male"}
    })
    d = res.get_json() or {}
    check("Multiple concurrent symptoms", res.status_code == 200 and len(d.get("input_symptoms", [])) == 4)

    # Case 10: Missing required information (empty symptoms and empty text)
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": [],
        "problem_description": ""
    })
    check("Missing required symptoms rejected with 400", res.status_code == 400 and res.get_json().get("success") is False)

    # Case 11: Invalid parameter (out-of-bounds temperature handled gracefully)
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["high_fever"],
        "symptom_parameters": {
            "high_fever": {
                "temperature": 199.9  # Out of valid range
            }
        }
    })
    # Should proceed with safe fallback/warning without server 500 error
    check("Invalid parameter handled gracefully", res.status_code == 200 and res.get_json().get("success") is True)

    # Case 12: Oversized image rejected
    huge_buf = io.BytesIO(b"0" * (6 * 1024 * 1024))  # 6 MB
    res = client.post('/api/symptoms/analyze', data={
        "symptoms": json.dumps(["skin_rash"]),
        "image": (huge_buf, "oversized.jpg", "image/jpeg")
    }, content_type="multipart/form-data")
    check("Oversized image rejected with 400", res.status_code == 400 and "large" in res.get_json().get("error", "").lower())

    # Case 13: Unsupported image format rejected (e.g. text file or exe)
    txt_buf = io.BytesIO(b"Hello this is not an image file")
    res = client.post('/api/symptoms/analyze', data={
        "symptoms": json.dumps(["skin_rash"]),
        "image": (txt_buf, "malicious.exe", "application/octet-stream")
    }, content_type="multipart/form-data")
    check("Unsupported executable/text file rejected", res.status_code == 400)

    # Case 14: Emergency combination (chest pain + breathlessness + sweating)
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["chest_pain", "breathlessness", "sweating"],
        "severity": "Severe"
    })
    d = res.get_json() or {}
    check("Emergency combination triggers emergency=True & Critical severity", res.status_code == 200 and d.get("emergency") is True and d.get("severity") == "CRITICAL" and d.get("specialist") == "Cardiologist")

    # Case 15: Normal non-emergency case (mild acne)
    res = client.post('/api/symptoms/analyze', json={
        "symptoms": ["pus_filled_pimples", "blackheads"],
        "severity": "Mild"
    })
    d = res.get_json() or {}
    check("Normal non-emergency case (Mild)", res.status_code == 200 and d.get("emergency") is False and d.get("severity") == "MILD" and d.get("specialist") == "Dermatologist")

    print("==================================================================")
    print(f" TEST RESULTS: {passed}/{total} CASES PASSED ({(passed/total)*100:.1f}%)")
    print("==================================================================")
    assert passed == total, f"Expected {total} passed tests, but got {passed}"

if __name__ == "__main__":
    run_tests()
