"""
HealthConnect Reusable Symptom Parameter Metadata System
Provides declarative, structured clinical parameter definitions for symptoms
with rich validation rules, allowed options, units, and severity scoring.
Aligned with the 132-symptom clinical vocabulary and triage rules.
"""

from typing import Dict, List, Any, Tuple

# Pre-defined specialized symptom parameter schemas
SYMPTOM_PARAMETER_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "high_fever": {
        "symptom": "high_fever",
        "title": "Fever & Elevated Temperature",
        "category": "General & Systemic",
        "parameters": [
            {
                "name": "temperature",
                "label": "Measured Body Temperature",
                "type": "number",
                "unit": "°F",
                "default": 101.2,
                "validation": {"min": 95.0, "max": 108.0, "step": 0.1},
                "required": False,
                "help": "Normal range: 97.0°F - 99.0°F. High fever is above 101.5°F."
            },
            {
                "name": "temperature_unit",
                "label": "Temperature Unit",
                "type": "select",
                "options": ["°F", "°C"],
                "default": "°F",
                "required": True
            },
            {
                "name": "duration",
                "label": "Fever Duration",
                "type": "select",
                "options": ["Less than 24 hours", "1-2 days", "3-5 days", "1-2 weeks", "More than 2 weeks"],
                "default": "1-2 days",
                "required": True
            },
            {
                "name": "pattern",
                "label": "Fever Pattern",
                "type": "select",
                "options": [
                    "Continuous (stays elevated consistently)",
                    "Intermittent (spikes and returns to normal)",
                    "Evening rises (higher in evenings)",
                    "Fluctuating with sweats and chills"
                ],
                "default": "Intermittent (spikes and returns to normal)",
                "required": False
            },
            {
                "name": "chills",
                "label": "Accompanied by Shivering or Chills?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "sweating",
                "label": "Profuse Sweating or Night Sweats?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "severity",
                "label": "Perceived Severity / Discomfort",
                "type": "slider",
                "validation": {"min": 1, "max": 10, "step": 1},
                "default": 6,
                "required": True
            }
        ]
    },

    "headache": {
        "symptom": "headache",
        "title": "Headache & Head Pain",
        "category": "Head, ENT & Eyes",
        "parameters": [
            {
                "name": "location",
                "label": "Primary Location of Pain",
                "type": "select",
                "options": [
                    "Forehead & brows (Frontal)",
                    "One side / Temple (Unilateral)",
                    "Back of head & neck (Occipital)",
                    "Tight band around entire head",
                    "Behind the eyes"
                ],
                "default": "Forehead & brows (Frontal)",
                "required": True
            },
            {
                "name": "onset",
                "label": "How did the headache start?",
                "type": "select",
                "options": [
                    "Gradual buildup over hours",
                    "Sudden severe 'thunderclap' (within seconds/minutes)",
                    "Woke up with pain",
                    "After reading, screen use, or stress"
                ],
                "default": "Gradual buildup over hours",
                "required": True,
                "help": "Sudden explosive headaches require urgent medical evaluation."
            },
            {
                "name": "pain_character",
                "label": "Character of Pain",
                "type": "select",
                "options": [
                    "Pulsating / Throbbing",
                    "Dull, steady pressure or tightness",
                    "Sharp, stabbing, or shooting",
                    "Burning or electric-like"
                ],
                "default": "Pulsating / Throbbing",
                "required": True
            },
            {
                "name": "light_sensitivity",
                "label": "Sensitivity to Light (Photophobia)?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "sound_sensitivity",
                "label": "Sensitivity to Sound (Phonophobia)?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "nausea",
                "label": "Nausea or Upset Stomach?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "visual_changes",
                "label": "Visual Disturbances (Aura, blurriness, zig-zag lines)?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "severity",
                "label": "Pain Intensity Scale (1-10)",
                "type": "slider",
                "validation": {"min": 1, "max": 10, "step": 1},
                "default": 5,
                "required": True
            }
        ]
    },

    "cough": {
        "symptom": "cough",
        "title": "Cough & Respiratory Reflex",
        "category": "Chest & Cardiovascular",
        "parameters": [
            {
                "name": "cough_type",
                "label": "Type of Cough",
                "type": "select",
                "options": [
                    "Dry & tickly (non-productive)",
                    "Wet & productive (bringing up mucus/phlegm)",
                    "Barking or harsh",
                    "Spasmodic / coughing fits"
                ],
                "default": "Dry & tickly (non-productive)",
                "required": True
            },
            {
                "name": "duration",
                "label": "How long have you been coughing?",
                "type": "select",
                "options": ["Less than 1 week", "1 to 3 weeks", "3 to 8 weeks", "More than 8 weeks (chronic)"],
                "default": "Less than 1 week",
                "required": True
            },
            {
                "name": "sputum_color",
                "label": "Sputum / Phlegm Color",
                "type": "select",
                "options": [
                    "No sputum / Dry",
                    "Clear or white",
                    "Yellow or yellowish-green",
                    "Rust-colored or brownish",
                    "Blood-tinged or pink"
                ],
                "default": "No sputum / Dry",
                "required": False
            },
            {
                "name": "blood_presence",
                "label": "Coughing up visible blood?",
                "type": "boolean",
                "default": False,
                "help": "Coughing up blood is a critical symptom requiring prompt evaluation."
            },
            {
                "name": "breathing_difficulty",
                "label": "Shortness of breath or wheezing with cough?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "chest_pain_with_cough",
                "label": "Sharp chest pain when coughing or taking deep breaths?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "triggers",
                "label": "Common Triggers",
                "type": "multi-select",
                "options": [
                    "Cold dry air",
                    "Lying down flat at night",
                    "Physical exertion or exercise",
                    "Dust, pollen, or chemical fumes",
                    "After eating or lying down after meals"
                ],
                "default": []
            },
            {
                "name": "severity",
                "label": "Cough Frequency & Disturbance (1-10)",
                "type": "slider",
                "validation": {"min": 1, "max": 10, "step": 1},
                "default": 4,
                "required": True
            }
        ]
    },

    "chest_pain": {
        "symptom": "chest_pain",
        "title": "Chest Pain & Discomfort",
        "category": "Chest & Cardiovascular",
        "parameters": [
            {
                "name": "location",
                "label": "Exact Location in Chest",
                "type": "select",
                "options": [
                    "Center of chest behind breastbone (Substernal)",
                    "Left side of chest over the heart",
                    "Right side of chest",
                    "Lower ribs / upper abdomen area",
                    "Diffuse across whole chest"
                ],
                "default": "Center of chest behind breastbone (Substernal)",
                "required": True
            },
            {
                "name": "pain_character",
                "label": "Description of Chest Pain",
                "type": "select",
                "options": [
                    "Heavy pressure, crushing, squeezing or tightness",
                    "Sharp, stabbing, like a needle (worse with deep breath)",
                    "Burning sensation (like severe indigestion/acid)",
                    "Dull, persistent ache",
                    "Tearing or ripping sensation"
                ],
                "default": "Heavy pressure, crushing, squeezing or tightness",
                "required": True
            },
            {
                "name": "radiation",
                "label": "Does the pain radiate to other areas?",
                "type": "multi-select",
                "options": [
                    "Left arm or left shoulder",
                    "Jaw, neck, or lower teeth",
                    "Upper back between shoulder blades",
                    "Upper abdomen",
                    "Right arm",
                    "Does not radiate"
                ],
                "default": ["Does not radiate"]
            },
            {
                "name": "breathlessness",
                "label": "Shortness of breath or difficulty breathing?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "sweating",
                "label": "Cold clammy sweats or unexplained perspiration?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "dizziness",
                "label": "Feeling lightheaded, faint, or dizzy?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "activity_relation",
                "label": "Relation to Physical Activity",
                "type": "select",
                "options": [
                    "Brought on or worsened by exertion (walking, stairs)",
                    "Occurs at rest or during sleep",
                    "Worse when taking deep breaths or coughing",
                    "Worse when pressing on the chest wall",
                    "Better when leaning forward"
                ],
                "default": "Brought on or worsened by exertion (walking, stairs)",
                "required": True
            },
            {
                "name": "severity",
                "label": "Pain Severity Scale (1-10)",
                "type": "slider",
                "validation": {"min": 1, "max": 10, "step": 1},
                "default": 7,
                "required": True
            }
        ]
    },

    "abdominal_pain": {
        "symptom": "abdominal_pain",
        "title": "Abdominal & Stomach Pain",
        "category": "Digestive & Abdomen",
        "parameters": [
            {
                "name": "location",
                "label": "Abdominal Region",
                "type": "select",
                "options": [
                    "Right upper abdomen (beneath right ribs)",
                    "Left upper abdomen (beneath left ribs)",
                    "Right lower abdomen (near groin/hip)",
                    "Left lower abdomen",
                    "Around the belly button (Periumbilical)",
                    "Lower pelvic abdomen (central)",
                    "Generalized throughout whole abdomen"
                ],
                "default": "Around the belly button (Periumbilical)",
                "required": True
            },
            {
                "name": "pain_character",
                "label": "Quality of Pain",
                "type": "select",
                "options": [
                    "Cramping / Waves of colic",
                    "Sharp, knife-like, or stabbing",
                    "Dull, persistent ache",
                    "Burning sensation (like gastritis)",
                    "Bloated and distended fullness"
                ],
                "default": "Cramping / Waves of colic",
                "required": True
            },
            {
                "name": "onset",
                "label": "Pain Onset",
                "type": "select",
                "options": [
                    "Sudden acute onset within minutes",
                    "Gradual increase over 1-2 days",
                    "Recurrent / chronic over weeks"
                ],
                "default": "Gradual increase over 1-2 days",
                "required": True
            },
            {
                "name": "nausea_vomiting",
                "label": "Accompanied by nausea or vomiting?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "diarrhea",
                "label": "Frequent watery stools or diarrhea?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "blood_in_stool",
                "label": "Blood in stool or black tarry stools?",
                "type": "boolean",
                "default": False,
                "help": "GI bleeding requires immediate medical attention."
            },
            {
                "name": "fever",
                "label": "Accompanied by fever or chills?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "severity",
                "label": "Pain Intensity Scale (1-10)",
                "type": "slider",
                "validation": {"min": 1, "max": 10, "step": 1},
                "default": 5,
                "required": True
            }
        ]
    },

    "skin_rash": {
        "symptom": "skin_rash",
        "title": "Skin Rash & Dermatological Change",
        "category": "Skin & Dermatological",
        "parameters": [
            {
                "name": "location",
                "label": "Body Areas Affected",
                "type": "multi-select",
                "options": [
                    "Face / Cheeks / Forehead",
                    "Arms & Forearms",
                    "Hands & Fingers",
                    "Chest, Back & Torso",
                    "Legs & Thighs",
                    "Feet & Ankles",
                    "Skin folds (groin, armpits, under breasts)",
                    "Widespread across most of the body"
                ],
                "default": ["Arms & Forearms"],
                "required": True
            },
            {
                "name": "appearance",
                "label": "Rash Appearance & Texture",
                "type": "select",
                "options": [
                    "Flat red spots or discoloration (Macules)",
                    "Raised red bumps or hives (Papules/Wheals)",
                    "Fluid-filled small blisters (Vesicles)",
                    "Pus-filled pimples (Pustules)",
                    "Dry, scaly, silvery dusting plaques",
                    "Crusted, honey-colored oozing lesions",
                    "Ring-shaped / circular red borders"
                ],
                "default": "Raised red bumps or hives (Papules/Wheals)",
                "required": True
            },
            {
                "name": "itching",
                "label": "Degree of Itching",
                "type": "select",
                "options": [
                    "No itching at all",
                    "Mild occasional itch",
                    "Moderate persistent itching",
                    "Severe, unbearable itching (interrupting sleep)"
                ],
                "default": "Moderate persistent itching",
                "required": True
            },
            {
                "name": "pain",
                "label": "Is the area tender, burning, or painful?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "spread",
                "label": "Has the rash spread over time?",
                "type": "select",
                "options": [
                    "Stationary (stayed in one spot)",
                    "Spreading slowly over several days",
                    "Spreading rapidly within a few hours",
                    "Improving / resolving"
                ],
                "default": "Spreading slowly over several days",
                "required": True
            },
            {
                "name": "discharge",
                "label": "Discharge or Fluid",
                "type": "select",
                "options": ["None / Dry", "Clear watery ooze", "Yellow pus", "Crusting over"],
                "default": "None / Dry"
            },
            {
                "name": "possible_trigger",
                "label": "Possible Trigger or Exposure",
                "type": "select",
                "options": [
                    "New skin product, cosmetic, or soap",
                    "New medication, tablet, or antibiotic",
                    "Outdoor plant, insect bite, or animal contact",
                    "Sunlight or heat exposure",
                    "Unknown / None obvious"
                ],
                "default": "Unknown / None obvious"
            },
            {
                "name": "severity",
                "label": "Rash Discomfort / Severity (1-10)",
                "type": "slider",
                "validation": {"min": 1, "max": 10, "step": 1},
                "default": 4,
                "required": True
            }
        ]
    },

    "breathlessness": {
        "symptom": "breathlessness",
        "title": "Breathlessness & Dyspnea",
        "category": "Chest & Cardiovascular",
        "parameters": [
            {
                "name": "onset",
                "label": "How quickly did breathlessness start?",
                "type": "select",
                "options": [
                    "Sudden acute onset within minutes",
                    "Gradual increase over days",
                    "Progressive worsening over weeks/months",
                    "Episodes that come and go"
                ],
                "default": "Gradual increase over days",
                "required": True
            },
            {
                "name": "worse_lying_down",
                "label": "Harder to breathe when lying flat in bed?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "wheezing",
                "label": "Noticeable wheezing or whistling sound?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "swelling_legs",
                "label": "Noticeable swelling in legs, ankles, or feet?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "severity",
                "label": "Difficulty Breathing Level (1-10)",
                "type": "slider",
                "validation": {"min": 1, "max": 10, "step": 1},
                "default": 6,
                "required": True
            }
        ]
    },

    "joint_pain": {
        "symptom": "joint_pain",
        "title": "Joint Pain & Arthralgia",
        "category": "Musculoskeletal & Mobility",
        "parameters": [
            {
                "name": "joints_affected",
                "label": "Joints Affected",
                "type": "multi-select",
                "options": [
                    "Knees",
                    "Hips",
                    "Hands & Finger joints",
                    "Wrists",
                    "Shoulders",
                    "Ankles & Feet",
                    "Spine & Lower back"
                ],
                "default": ["Knees"],
                "required": True
            },
            {
                "name": "morning_stiffness",
                "label": "Morning stiffness lasting more than 30-45 minutes?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "swelling",
                "label": "Visible swelling or puffiness around joints?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "redness_warmth",
                "label": "Joint is visibly red or warm to touch?",
                "type": "boolean",
                "default": False
            },
            {
                "name": "severity",
                "label": "Joint Pain & Mobility Impact (1-10)",
                "type": "slider",
                "validation": {"min": 1, "max": 10, "step": 1},
                "default": 5,
                "required": True
            }
        ]
    }
}

# Aliases for symptoms that map to parameter schemas
SCHEMA_ALIASES = {
    "mild_fever": "high_fever",
    "fever": "high_fever",
    "stomach_pain": "abdominal_pain",
    "belly_pain": "abdominal_pain",
    "nodal_skin_eruptions": "skin_rash",
    "pus_filled_pimples": "skin_rash",
    "dischromic_patches": "skin_rash",
    "red_spots_over_body": "skin_rash",
    "knee_pain": "joint_pain",
    "hip_joint_pain": "joint_pain",
    "swelling_joints": "joint_pain"
}

def get_default_symptom_parameters(symptom_key: str, display_name: str, category: str = "General") -> Dict[str, Any]:
    """Generates an adaptive structured parameter schema for any symptom without a custom schema."""
    return {
        "symptom": symptom_key,
        "title": display_name,
        "category": category,
        "parameters": [
            {
                "name": "duration",
                "label": f"How long have you had {display_name.lower()}?",
                "type": "select",
                "options": ["Less than 24 hours", "1-2 days", "3-7 days", "1-2 weeks", "More than 2 weeks"],
                "default": "1-2 days",
                "required": True
            },
            {
                "name": "onset",
                "label": "Onset Pattern",
                "type": "select",
                "options": ["Sudden onset", "Gradual development", "Comes and goes (intermittent)"],
                "default": "Gradual development",
                "required": False
            },
            {
                "name": "impact",
                "label": "Impact on Daily Activities",
                "type": "select",
                "options": [
                    "Mild (noticeable but no disruption)",
                    "Moderate (disrupts some daily tasks)",
                    "Severe (unable to perform routine activities)"
                ],
                "default": "Moderate (disrupts some daily tasks)",
                "required": True
            },
            {
                "name": "severity",
                "label": f"Severity Level for {display_name} (1-10)",
                "type": "slider",
                "validation": {"min": 1, "max": 10, "step": 1},
                "default": 5,
                "required": True
            },
            {
                "name": "notes",
                "label": "Specific Observations or Triggers (Optional)",
                "type": "text",
                "default": "",
                "required": False
            }
        ]
    }

def get_parameters_for_symptom(symptom_key: str, category: str = "General") -> Dict[str, Any]:
    """Returns the parameter metadata definition for a specific symptom."""
    clean_key = symptom_key.lower().replace(" ", "_").strip()
    
    # Check direct schema
    if clean_key in SYMPTOM_PARAMETER_DEFINITIONS:
        return SYMPTOM_PARAMETER_DEFINITIONS[clean_key]
        
    # Check alias
    if clean_key in SCHEMA_ALIASES:
        target_schema = SYMPTOM_PARAMETER_DEFINITIONS[SCHEMA_ALIASES[clean_key]].copy()
        target_schema["symptom"] = clean_key
        target_schema["title"] = clean_key.replace("_", " ").title()
        return target_schema
        
    # Return adaptive fallback schema
    display = clean_key.replace("_", " ").title()
    return get_default_symptom_parameters(clean_key, display, category)

def validate_parameter_value(param_def: Dict[str, Any], value: Any) -> Tuple[bool, str]:
    """Validates a single parameter value against its definition."""
    ptype = param_def.get("type")
    is_required = param_def.get("required", False)
    
    if value is None or value == "":
        if is_required:
            return False, f"'{param_def.get('label')}' is required."
        return True, ""
        
    validation = param_def.get("validation", {})
    
    if ptype == "number":
        try:
            num = float(value)
            if "min" in validation and num < validation["min"]:
                return False, f"Value must be at least {validation['min']} {param_def.get('unit', '')}."
            if "max" in validation and num > validation["max"]:
                return False, f"Value must not exceed {validation['max']} {param_def.get('unit', '')}."
        except (ValueError, TypeError):
            return False, "Please enter a valid numeric value."
            
    elif ptype == "slider":
        try:
            num = int(value)
            if "min" in validation and num < validation["min"]:
                return False, f"Scale minimum is {validation['min']}."
            if "max" in validation and num > validation["max"]:
                return False, f"Scale maximum is {validation['max']}."
        except (ValueError, TypeError):
            return False, "Scale must be an integer."
            
    elif ptype == "select":
        allowed = param_def.get("options", [])
        if value not in allowed:
            return False, f"Invalid selection. Please choose from allowed options."
            
    elif ptype == "multi-select":
        allowed = set(param_def.get("options", []))
        if not isinstance(value, (list, tuple)):
            return False, "Selection must be a list."
        for item in value:
            if item not in allowed:
                return False, f"Invalid selection item '{item}'."
                
    elif ptype == "boolean":
        if not isinstance(value, bool):
            if str(value).lower() not in ["true", "false", "1", "0"]:
                return False, "Must be true or false."
                
    return True, ""

def validate_all_symptom_parameters(symptom_parameters: Dict[str, Dict[str, Any]]) -> Tuple[bool, Dict[str, str]]:
    """
    Validates a complete dictionary of user-entered symptom parameters.
    Returns: (is_valid, errors_dict)
    """
    errors = {}
    if not isinstance(symptom_parameters, dict):
        return True, {}
        
    for symptom_key, user_params in symptom_parameters.items():
        schema = get_parameters_for_symptom(symptom_key)
        for pdef in schema.get("parameters", []):
            pname = pdef.get("name")
            val = user_params.get(pname, pdef.get("default"))
            is_valid, err_msg = validate_parameter_value(pdef, val)
            if not is_valid:
                errors[f"{symptom_key}.{pname}"] = err_msg
                
    return len(errors) == 0, errors
