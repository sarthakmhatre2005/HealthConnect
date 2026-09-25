"""
HealthConnect ML Predictor Module
Provides high-performance, in-memory local inference combining:
- RandomForestClassifier
- XGBoost XGBClassifier
- Clinical Knowledge Base
- Emergency Triage & Severity Rules
"""

import os
import sys
import json
import logging
import numpy as np
import joblib

# Ensure parent directory is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml_engine.dataset import SYMPTOMS, SYMPTOM_CATEGORIES, DISEASE_KNOWLEDGE_BASE, EMERGENCY_RULES, DISEASE_SYMPTOM_MAP
from ml_engine.quantum_pipeline import run_quantum_pipeline
from ml_engine.symptom_parameters import validate_all_symptom_parameters

logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

class HealthPredictor:
    """
    Singleton ML Inference Engine
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HealthPredictor, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance

    def _load_models(self):
        logger.info("Loading HealthConnect ML models and encoders into memory...")
        rf_path = os.path.join(MODELS_DIR, "random_forest.joblib")
        xgb_path = os.path.join(MODELS_DIR, "xgboost.joblib")
        label_enc_path = os.path.join(MODELS_DIR, "label_encoder.joblib")
        symptom_enc_path = os.path.join(MODELS_DIR, "symptom_encoder.joblib")
        kb_path = os.path.join(MODELS_DIR, "knowledge_base.json")

        if not all(os.path.exists(p) for p in [rf_path, xgb_path, label_enc_path, symptom_enc_path, kb_path]):
            from ml_engine.train import train_and_save
            train_and_save()

        self.rf_model = joblib.load(rf_path)
        try:
            self.xgb_model = joblib.load(xgb_path)
        except Exception as exc:
            # On macOS, XGBoost may be installed without its OpenMP runtime
            # (libomp). Keep the API usable with the bundled Random Forest in
            # that case; symptom prediction below reports the active model.
            self.xgb_model = None
            logger.warning(
                "Could not load the XGBoost model; using Random Forest only. "
                "On macOS, install the OpenMP runtime with `brew install libomp`. "
                "Details: %s",
                exc,
            )
        self.label_encoder = joblib.load(label_enc_path)
        self.symptom_metadata = joblib.load(symptom_enc_path)

        with open(kb_path, "r", encoding="utf-8") as f:
            self.knowledge_base = json.load(f)

        self.symptoms_list = self.symptom_metadata["symptoms"]
        self.symptom_to_idx = self.symptom_metadata["symptom_to_idx"]
        self.num_symptoms = self.symptom_metadata["num_symptoms"]

        # Alias lookup for user symptom strings
        self.alias_map = {}
        for s in self.symptoms_list:
            clean = s.lower().replace("_", " ").strip()
            self.alias_map[clean] = s
            self.alias_map[s] = s

        # Common clinical aliases
        common_aliases = {
            "fever": "high_fever",
            "temperature": "high_fever",
            "chills": "chills",
            "body pain": "muscle_pain",
            "body ache": "muscle_pain",
            "shortness of breath": "breathlessness",
            "difficulty breathing": "breathlessness",
            "dyspnea": "breathlessness",
            "loose motion": "diarrhoea",
            "loose stools": "diarrhoea",
            "runny nose": "runny_nose",
            "sneezing": "continuous_sneezing",
            "headache": "headache",
            "migraine": "headache",
            "vomiting": "vomiting",
            "nausea": "nausea",
            "fatigue": "fatigue",
            "tiredness": "fatigue",
            "rash": "skin_rash",
            "itching": "itching",
            "chest pain": "chest_pain",
            "palpitations": "palpitations",
            "fast heart rate": "fast_heart_rate",
            "tachycardia": "fast_heart_rate",
            "stomach ache": "stomach_pain",
            "stomach pain": "stomach_pain",
            "abdominal pain": "abdominal_pain",
            "joint pain": "joint_pain",
            "knee pain": "knee_pain",
            "back pain": "back_pain",
            "yellow eyes": "yellowing_of_eyes",
            "yellow skin": "yellowish_skin",
            "acidity": "acidity",
            "heartburn": "acidity"
        }
        for alias, target in common_aliases.items():
            if target in self.symptom_to_idx:
                self.alias_map[alias] = target

        logger.info("HealthConnect ML Predictor initialized successfully.")

    def normalize_symptom(self, symptom_str):
        """Maps user symptom string to exact training feature key."""
        if not symptom_str or not isinstance(symptom_str, str):
            return None
        cleaned = symptom_str.lower().replace("-", " ").replace("_", " ").strip()
        if cleaned in self.alias_map:
            return self.alias_map[cleaned]
        if symptom_str in self.symptom_to_idx:
            return symptom_str
        # Substring match
        for known in self.symptoms_list:
            known_clean = known.replace("_", " ")
            if cleaned in known_clean or known_clean in cleaned:
                return known
        return None

    def check_emergency(self, normalized_symptoms):
        """Evaluates emergency triage rules against patient symptoms."""
        symptom_set = set(normalized_symptoms)
        for rule in EMERGENCY_RULES:
            req_match = all(r in symptom_set for r in rule["required_symptoms"])
            if req_match:
                if rule["min_co_symptoms"] == 0:
                    return True, rule["name"], rule["message"]
                co_matches = sum(1 for c in rule["co_symptoms"] if c in symptom_set)
                if co_matches >= rule["min_co_symptoms"]:
                    return True, rule["name"], rule["message"]
        return False, None, None

    def check_parameter_red_flags(self, symptom_parameters):
        """Evaluates clinical red flags from detailed symptom parameters."""
        if not symptom_parameters or not isinstance(symptom_parameters, dict):
            return False, None, None

        # Cough red flags
        cough_params = symptom_parameters.get("cough", {})
        if cough_params.get("blood_presence") is True:
            return True, "Hemoptysis / Acute Respiratory Bleed", "Critical Warning: Coughing up blood requires immediate urgent medical evaluation."

        # Headache red flags
        headache_params = symptom_parameters.get("headache", {})
        if "thunderclap" in str(headache_params.get("onset", "")).lower():
            return True, "Acute Thunderclap Headache / Vascular Event", "Emergency Alert: Sudden explosive thunderclap headache may indicate vascular distress. Seek emergency medical attention immediately."

        # Chest pain red flags
        chest_params = symptom_parameters.get("chest_pain", {})
        if chest_params:
            rad = chest_params.get("radiation", [])
            has_arm_jaw_radiation = any("arm" in str(r).lower() or "jaw" in str(r).lower() for r in rad)
            if has_arm_jaw_radiation or chest_params.get("breathlessness") is True or chest_params.get("sweating") is True:
                return True, "Acute Coronary Distress", "Emergency Alert: Severe chest pain with radiating pain and distress signs. Seek emergency medical care (ER/Ambulance) immediately."

        # Abdominal pain red flags
        abd_params = symptom_parameters.get("abdominal_pain", {}) or symptom_parameters.get("stomach_pain", {})
        if abd_params.get("blood_in_stool") is True:
            return True, "Acute Gastrointestinal Hemorrhage", "Urgent Emergency: Blood in stool or gastrointestinal bleeding detected. Immediate hospitalization required."

        return False, None, None

    def predict(self, symptoms, age=None, gender=None, duration=None, severity=None, additional_info="",
                patient_details=None, problem_description="", symptom_parameters=None, image_metadata=None):
        """
        Performs multimodal clinical inference combining:
        - Dual Classical Ensemble: RandomForestClassifier + XGBoost XGBClassifier
        - 4-Qubit Quantum ML Pipeline: PennyLane Simulator (AngleEmbedding, VQC/QNN, QSVM)
        - Dynamic Clinical Parameter Evaluation & Red-Flag Safety Rules
        """
        if not symptoms or not isinstance(symptoms, list):
            return {
                "success": False,
                "error": "Please provide a list of symptoms.",
                "predictions": [],
                "severity": "MILD",
                "emergency": False,
                "specialist": "General Physician"
            }

        # Resolve demographics from patient_details if provided
        if patient_details and isinstance(patient_details, dict):
            if age is None and patient_details.get("age"):
                try:
                    age = int(patient_details["age"])
                except (ValueError, TypeError):
                    pass
            if gender is None and patient_details.get("gender"):
                gender = patient_details["gender"]

        normalized_symptoms = []
        for s in symptoms:
            norm = self.normalize_symptom(s)
            if norm and norm not in normalized_symptoms:
                normalized_symptoms.append(norm)

        if not normalized_symptoms:
            return {
                "success": False,
                "error": "None of the provided symptoms could be recognized. Please select from known clinical symptoms.",
                "predictions": [],
                "severity": "MILD",
                "emergency": False,
                "specialist": "General Physician"
            }

        # Validate symptom parameters if supplied
        if symptom_parameters and isinstance(symptom_parameters, dict):
            _, param_errors = validate_all_symptom_parameters(symptom_parameters)
            if param_errors:
                logger.warning(f"Symptom parameter validation notices: {param_errors}")

        # Build feature vector for classical ML models
        vector = np.zeros(self.num_symptoms, dtype=np.float32)
        for s in normalized_symptoms:
            idx = self.symptom_to_idx[s]
            vector[idx] = 1.0

        feature_matrix = vector.reshape(1, -1)

        # 1. Random Forest inference
        rf_probs = self.rf_model.predict_proba(feature_matrix)[0]

        # 2. XGBoost inference, when its native runtime is available.
        if self.xgb_model is not None:
            xgb_probs = self.xgb_model.predict_proba(feature_matrix)[0]
        else:
            xgb_probs = rf_probs.copy()

        # 3. Dual-model ensemble (equal weighting)
        ensemble_probs = (rf_probs + xgb_probs) / 2.0

        # Extract Top 3 predictions
        top3_indices = np.argsort(ensemble_probs)[::-1][:3]
        top3_classes = self.label_encoder.inverse_transform(top3_indices)
        top3_probs = ensemble_probs[top3_indices]

        # Normalize top 3 probabilities for user presentation
        total_top3_prob = float(np.sum(top3_probs))
        if total_top3_prob > 0:
            norm_top3_probs = top3_probs / total_top3_prob
        else:
            norm_top3_probs = top3_probs

        predictions = []
        for i in range(len(top3_classes)):
            disease_name = str(top3_classes[i])
            raw_prob = float(top3_probs[i])
            calibrated_pct = round(raw_prob * 100, 1)
            predictions.append({
                "disease": disease_name,
                "probability": round(raw_prob, 3),
                "confidence_percent": calibrated_pct,
                "rf_probability": round(float(rf_probs[top3_indices[i]]), 3),
                "xgb_probability": (
                    round(float(xgb_probs[top3_indices[i]]), 3)
                    if self.xgb_model is not None
                    else None
                )
            })

        top_disease = predictions[0]["disease"]
        kb_info = self.knowledge_base.get(top_disease, {
            "specialist": "General Physician",
            "base_severity": "MODERATE",
            "description": "Consult a healthcare provider for personalized medical evaluation.",
            "precautions": ["Rest adequately", "Stay hydrated", "Monitor symptoms", "Consult a doctor"],
            "warning_signs": ["Persistent high fever", "Severe pain", "Difficulty breathing"]
        })

        # Emergency rule triage: Check both symptom set and parameter red flags
        is_emergency, emergency_event, emergency_message = self.check_emergency(normalized_symptoms)
        if not is_emergency and symptom_parameters:
            param_emerg, param_event, param_msg = self.check_parameter_red_flags(symptom_parameters)
            if param_emerg:
                is_emergency = True
                emergency_event = param_event
                emergency_message = param_msg

        # Dynamic severity calculation incorporating parameters
        base_sev = kb_info.get("base_severity", "MODERATE")
        if is_emergency:
            computed_severity = "CRITICAL"
        elif severity and str(severity).lower() in ["severe", "very severe"]:
            computed_severity = "SEVERE" if base_sev != "CRITICAL" else "CRITICAL"
        else:
            # Check high fever temperature parameter (> 103°F)
            fever_params = (symptom_parameters or {}).get("high_fever", {}) or (symptom_parameters or {}).get("mild_fever", {})
            if fever_params.get("temperature") and float(fever_params["temperature"]) >= 103.0:
                computed_severity = "SEVERE"
            else:
                computed_severity = base_sev

        # 4-Qubit Quantum Machine Learning Pipeline
        visual_features = image_metadata.get("visual_features") if image_metadata else None
        quantum_analysis = run_quantum_pipeline(
            symptom_vector=vector,
            severity=computed_severity,
            duration=duration or "1-2 days",
            age=age,
            visual_features=visual_features
        )

        # Explainable AI: Identify contributing symptoms from patient input
        disease_char_symptoms = DISEASE_SYMPTOM_MAP.get(top_disease, [])
        contributing_symptoms = [
            s.replace("_", " ").title() for s in normalized_symptoms if s in disease_char_symptoms
        ]
        if not contributing_symptoms:
            contributing_symptoms = [s.replace("_", " ").title() for s in normalized_symptoms[:3]]

        # Human-readable symptoms
        formatted_symptoms = [s.replace("_", " ").title() for s in normalized_symptoms]

        return {
            "success": True,
            "predictions": predictions,
            "top_condition": top_disease,
            "confidence_percent": predictions[0]["confidence_percent"],
            "severity": computed_severity,
            "emergency": is_emergency,
            "emergency_event": emergency_event,
            "emergency_message": emergency_message or "",
            "specialist": kb_info.get("specialist", "General Physician"),
            "specialist_type": kb_info.get("specialist", "General Physician"),
            "description": kb_info.get("description", ""),
            "important_symptoms": contributing_symptoms,
            "input_symptoms": formatted_symptoms,
            "problem_description": problem_description,
            "patient_details": patient_details or {
                "age": age,
                "gender": gender,
                "duration": duration,
                "severity": severity
            },
            "symptom_parameters": symptom_parameters or {},
            "image_analyzed": bool(image_metadata and image_metadata.get("image_analyzed")),
            "image_details": image_metadata if image_metadata else None,
            "quantum_analysis": quantum_analysis,
            "prevention": kb_info.get("precautions", []),
            "immediate_actions": kb_info.get("precautions", []),
            "warning_signs": kb_info.get("warning_signs", []),
            "emergency_warning_signs": kb_info.get("warning_signs", []),
            "ensemble_architecture": {
                "classical_models": (
                    ["RandomForestClassifier (120 trees)", "XGBoost (multi:softprob)"]
                    if self.xgb_model is not None
                    else ["RandomForestClassifier (120 trees)"]
                ),
                "quantum_models": ["4-Qubit Variational Quantum Circuit (VQC/QNN)", "Quantum Support Vector Machine (QSVM Kernel)"],
                "quantum_simulator": quantum_analysis.get("simulator", "4-Qubit Simulator"),
                "strategy": (
                    "Hybrid Classical-Quantum Soft Voting & Fidelity Alignment"
                    if self.xgb_model is not None
                    else "Random Forest with Quantum Analysis (XGBoost unavailable)"
                ),
                "feature_space_dim": self.num_symptoms,
                "quantum_features_dim": 4
            },
            "disclaimer": "This tool provides preliminary health information for awareness and decision support. It is not a medical diagnosis. Please consult a qualified healthcare professional for medical advice."
        }

# Global instance
predictor_instance = HealthPredictor()

def analyze_patient_symptoms(symptoms, age=None, gender=None, duration=None, severity=None, additional_info="",
                             patient_details=None, problem_description="", symptom_parameters=None, image_metadata=None):
    return predictor_instance.predict(
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

def get_all_symptoms():
    """Returns all available clinical symptoms with categories for UI autocomplete"""
    return {
        "symptoms": [s.replace("_", " ").title() for s in SYMPTOMS],
        "symptom_keys": SYMPTOMS,
        "categories": {
            cat: [s.replace("_", " ").title() for s in sym_list]
            for cat, sym_list in SYMPTOM_CATEGORIES.items()
        }
    }
