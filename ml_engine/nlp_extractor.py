"""
HealthConnect Local Deterministic NLP Extractor
Extracts clinical signals (symptom mentions, duration, severity, anatomical location, visual cues)
from patient free-text descriptions using a local, deterministic rule-based medical vocabulary parser.
100% Offline / Local Execution. No external LLMs, no Gemini, no API keys required.
"""

import re
from typing import Dict, List, Any

# Clinical symptom alias mapping to standard dataset feature keys
CLINICAL_ALIASES = {
    # Systemic & General
    "fever": "high_fever",
    "high fever": "high_fever",
    "mild fever": "mild_fever",
    "low grade fever": "mild_fever",
    "temperature": "high_fever",
    "chills": "chills",
    "shivering": "shivering",
    "sweating": "sweating",
    "night sweats": "sweating",
    "fatigue": "fatigue",
    "exhaustion": "fatigue",
    "tired": "fatigue",
    "tiredness": "fatigue",
    "lethargy": "lethargy",
    "weakness": "fatigue",
    "malaise": "malaise",
    "weight loss": "weight_loss",
    "weight gain": "weight_gain",
    "dehydration": "dehydration",
    "anxiety": "anxiety",
    "restlessness": "restlessness",
    "mood swings": "mood_swings",
    "depression": "depression",
    "irritability": "irritability",

    # Head, Eyes & ENT
    "headache": "headache",
    "head ache": "headache",
    "migraine": "headache",
    "splitting headache": "headache",
    "dizziness": "dizziness",
    "dizzy": "dizziness",
    "lightheaded": "dizziness",
    "vertigo": "spinning_movements",
    "spinning": "spinning_movements",
    "runny nose": "runny_nose",
    "running nose": "runny_nose",
    "sneezing": "continuous_sneezing",
    "continuous sneezing": "continuous_sneezing",
    "congestion": "congestion",
    "blocked nose": "congestion",
    "stuffy nose": "congestion",
    "sinus pressure": "sinus_pressure",
    "sinus pain": "sinus_pressure",
    "sore throat": "throat_irritation",
    "throat irritation": "throat_irritation",
    "scratchy throat": "throat_irritation",
    "patches in throat": "patches_in_throat",
    "loss of smell": "loss_of_smell",
    "anosmia": "loss_of_smell",
    "red eyes": "redness_of_eyes",
    "redness in eyes": "redness_of_eyes",
    "watery eyes": "watering_from_eyes",
    "watering eyes": "watering_from_eyes",
    "sunken eyes": "sunken_eyes",
    "eye pain": "pain_behind_the_eyes",
    "pain behind eyes": "pain_behind_the_eyes",
    "blurred vision": "blurred_and_distorted_vision",
    "distorted vision": "blurred_and_distorted_vision",
    "mouth ulcers": "ulcers_on_tongue",
    "ulcers on tongue": "ulcers_on_tongue",

    # Chest & Respiratory
    "cough": "cough",
    "coughing": "cough",
    "dry cough": "cough",
    "wet cough": "cough",
    "chest pain": "chest_pain",
    "chest tightness": "chest_pain",
    "chest pressure": "chest_pain",
    "shortness of breath": "breathlessness",
    "difficulty breathing": "breathlessness",
    "breathlessness": "breathlessness",
    "dyspnea": "breathlessness",
    "rapid heartbeat": "fast_heart_rate",
    "fast heart rate": "fast_heart_rate",
    "tachycardia": "fast_heart_rate",
    "palpitations": "palpitations",
    "racing heart": "palpitations",
    "phlegm": "phlegm",
    "mucus": "phlegm",
    "sputum": "phlegm",
    "blood in sputum": "blood_in_sputum",
    "coughing blood": "blood_in_sputum",
    "rusty sputum": "rusty_sputum",

    # Digestive & Abdomen
    "stomach pain": "stomach_pain",
    "stomach ache": "stomach_pain",
    "abdominal pain": "abdominal_pain",
    "belly pain": "belly_pain",
    "stomach cramps": "abdominal_pain",
    "acidity": "acidity",
    "heartburn": "acidity",
    "acid reflux": "acidity",
    "vomiting": "vomiting",
    "threw up": "vomiting",
    "throwing up": "vomiting",
    "nausea": "nausea",
    "queasy": "nausea",
    "indigestion": "indigestion",
    "loss of appetite": "loss_of_appetite",
    "poor appetite": "loss_of_appetite",
    "not hungry": "loss_of_appetite",
    "increased appetite": "increased_appetite",
    "excessive hunger": "excessive_hunger",
    "diarrhea": "diarrhoea",
    "diarrhoea": "diarrhoea",
    "loose motion": "diarrhoea",
    "loose stools": "diarrhoea",
    "constipation": "constipation",
    "gas": "passage_of_gases",
    "bloating": "distention_of_abdomen",
    "stomach swelling": "swelling_of_stomach",
    "bloody stool": "bloody_stool",
    "blood in stool": "bloody_stool",
    "stomach bleeding": "stomach_bleeding",

    # Skin & Visual Complaints
    "rash": "skin_rash",
    "skin rash": "skin_rash",
    "red rash": "skin_rash",
    "red patch": "skin_rash",
    "red patches": "skin_rash",
    "itching": "itching",
    "itchy": "itching",
    "itch": "itching",
    "internal itching": "internal_itching",
    "skin eruptions": "nodal_skin_eruptions",
    "nodal skin eruptions": "nodal_skin_eruptions",
    "bumps": "nodal_skin_eruptions",
    "red spots": "red_spots_over_body",
    "spots on skin": "red_spots_over_body",
    "yellow skin": "yellowish_skin",
    "yellowing skin": "yellowish_skin",
    "yellow eyes": "yellowing_of_eyes",
    "jaundice": "yellowish_skin",
    "pimples": "pus_filled_pimples",
    "pus filled pimples": "pus_filled_pimples",
    "acne": "pus_filled_pimples",
    "blackheads": "blackheads",
    "skin peeling": "skin_peeling",
    "peeling skin": "skin_peeling",
    "blister": "blister",
    "blisters": "blister",
    "crusts": "yellow_crust_ooze",
    "oozing sores": "yellow_crust_ooze",
    "red sore": "red_sore_around_nose",
    "discolored patches": "dischromic_patches",
    "bruising": "bruising",
    "bruise": "bruising",

    # Musculoskeletal & Mobility
    "joint pain": "joint_pain",
    "joints hurt": "joint_pain",
    "muscle pain": "muscle_pain",
    "body ache": "muscle_pain",
    "body pain": "muscle_pain",
    "muscle ache": "muscle_pain",
    "back pain": "back_pain",
    "lower back pain": "back_pain",
    "neck pain": "neck_pain",
    "stiff neck": "stiff_neck",
    "knee pain": "knee_pain",
    "hip pain": "hip_joint_pain",
    "swollen joints": "swelling_joints",
    "joint swelling": "swelling_joints",
    "movement stiffness": "movement_stiffness",
    "painful walking": "painful_walking",
    "trouble walking": "painful_walking",
    "muscle weakness": "muscle_weakness",
    "cramps": "cramps",
    "swollen legs": "swollen_legs",
    "swollen extremities": "swollen_extremeties",

    # Neurological & Critical
    "slurred speech": "slurred_speech",
    "loss of balance": "loss_of_balance",
    "unsteady": "unsteadiness",
    "unsteadiness": "unsteadiness",
    "one sided weakness": "weakness_of_one_body_side",
    "numbness on one side": "weakness_of_one_body_side",
    "confusion": "altered_sensorium",
    "altered mental state": "altered_sensorium",
    "coma": "coma",
    "unconscious": "coma",

    # Urinary & Pelvic
    "burning urination": "burning_micturition",
    "burning sensation while urinating": "burning_micturition",
    "painful urination": "burning_micturition",
    "spotting urination": "spotting_urination",
    "dark urine": "dark_urine",
    "foul smelling urine": "foul_smell_of_urine",
    "frequent urination": "polyuria",
    "bladder discomfort": "bladder_discomfort",
}

# Visual complaint keywords that indicate a photo may be relevant
VISUAL_KEYWORDS = [
    "rash", "skin", "patch", "lesion", "bump", "blister", "spot", "spots",
    "acne", "pimple", "pimples", "swelling", "swollen", "redness", "red patch",
    "discoloration", "peeling", "crust", "ooze", "wound", "bruise", "irritation",
    "mole", "sore", "eruption", "hives", "eczema", "boil"
]

# Anatomical body locations
BODY_LOCATIONS = [
    "arm", "arms", "forearm", "wrist", "hand", "hands", "finger", "fingers",
    "leg", "legs", "thigh", "knee", "knees", "calf", "ankle", "foot", "feet", "toe",
    "head", "forehead", "temple", "scalp", "face", "eye", "eyes", "nose", "throat", "neck",
    "chest", "breast", "ribs", "back", "upper back", "lower back", "spine",
    "stomach", "abdomen", "belly", "flank", "groin", "hip", "hips",
    "shoulder", "shoulders", "skin", "whole body"
]

def extract_duration_signals(text: str) -> str:
    """Detects duration phrasing in user text."""
    lowered = text.lower()
    
    # Patterns like "for 3 days", "3-4 days", "past 2 days", "since 3 days"
    day_match = re.search(r'(\d+)\s*(?:to|-)\s*(\d+)\s*days?', lowered)
    if day_match:
        return f"{day_match.group(1)}-{day_match.group(2)} days"
    
    day_single = re.search(r'(?:for|since|past|last)?\s*(\d+)\s*days?', lowered)
    if day_single:
        d = int(day_single.group(1))
        if d <= 1:
            return "Less than 24 hours"
        elif d <= 2:
            return "1-2 days"
        elif d <= 7:
            return "3-7 days"
        elif d <= 14:
            return "1-2 weeks"
        else:
            return "More than 2 weeks"
            
    # Week patterns
    week_match = re.search(r'(?:for|since|past|last)?\s*(\d+)\s*weeks?', lowered)
    if week_match:
        w = int(week_match.group(1))
        return "1-2 weeks" if w <= 2 else "More than 2 weeks"
        
    # Month patterns
    if re.search(r'\b(?:month|months|year|years)\b', lowered):
        return "More than 2 weeks"
        
    # Recent hours
    if re.search(r'\b(?:today|since morning|few hours|couple of hours|yesterday)\b', lowered):
        return "Less than 24 hours"
        
    return "1-2 days"

def extract_severity_signals(text: str) -> str:
    """Detects severity phrasing in user text."""
    lowered = text.lower()
    
    critical_words = ["unbearable", "excruciating", "can't breathe", "cannot breathe", "passed out", "blacked out", "severe chest pain"]
    for w in critical_words:
        if w in lowered:
            return "Severe"
            
    severe_words = ["severe", "extremely", "terrible", "horrible", "intense", "sharp", "very bad", "agony", "high fever"]
    for w in severe_words:
        if w in lowered:
            return "Severe"
            
    mild_words = ["mild", "slight", "little bit", "minor", "not too bad", "subtle", "low grade"]
    for w in mild_words:
        if w in lowered:
            return "Mild"
            
    return "Moderate"

def extract_body_locations(text: str) -> List[str]:
    """Extracts mentioned anatomical body locations."""
    lowered = text.lower()
    found = []
    for loc in BODY_LOCATIONS:
        # Match as whole word
        pattern = r'\b' + re.escape(loc) + r'\b'
        if re.search(pattern, lowered):
            # Normalize singular/plural
            norm_loc = loc.rstrip('s') if loc.endswith('s') and loc not in ["gas", "hives"] else loc
            if norm_loc not in found:
                found.append(norm_loc)
    return found

def extract_symptoms_from_text(text: str) -> Dict[str, Any]:
    """
    Parses patient natural language description and extracts:
    - Standardized symptom keys
    - Human-readable symptom names
    - Duration cues
    - Severity level
    - Mentioned body locations
    - Visual complaint presence flag
    """
    if not text or not isinstance(text, str):
        return {
            "success": True,
            "extracted_symptoms": [],
            "extracted_symptoms_display": [],
            "duration": "1-2 days",
            "severity": "Moderate",
            "locations": [],
            "has_visual_mention": False,
            "confidence": "none"
        }
        
    lowered = text.lower().strip()
    matched_symptoms = []
    
    # Sort aliases by phrase length descending (greedy multi-word match first)
    sorted_aliases = sorted(CLINICAL_ALIASES.items(), key=lambda x: len(x[0]), reverse=True)
    
    for phrase, feature_key in sorted_aliases:
        pattern = r'\b' + re.escape(phrase) + r'\b'
        if re.search(pattern, lowered):
            if feature_key not in matched_symptoms:
                matched_symptoms.append(feature_key)
                
    # Detect visual cues
    has_visual = False
    for kw in VISUAL_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', lowered):
            has_visual = True
            break
            
    # If any matched symptom is dermatological, set visual flag true
    skin_symptoms = [
        "skin_rash", "nodal_skin_eruptions", "yellowish_skin", "red_spots_over_body",
        "pus_filled_pimples", "blackheads", "skin_peeling", "blister", "yellow_crust_ooze",
        "dischromic_patches", "bruising", "itching"
    ]
    if any(s in skin_symptoms for s in matched_symptoms):
        has_visual = True
        
    duration = extract_duration_signals(lowered)
    severity = extract_severity_signals(lowered)
    locations = extract_body_locations(lowered)
    
    display_names = [s.replace("_", " ").title() for s in matched_symptoms]
    
    confidence = "high" if len(matched_symptoms) >= 2 else ("moderate" if len(matched_symptoms) == 1 else "low")
    
    return {
        "success": True,
        "extracted_symptoms": matched_symptoms,
        "extracted_symptoms_display": display_names,
        "duration": duration,
        "severity": severity,
        "locations": locations,
        "has_visual_mention": has_visual,
        "confidence": confidence,
        "summary": f"Detected {len(matched_symptoms)} symptom(s): {', '.join(display_names) if display_names else 'None directly identified'}."
    }
