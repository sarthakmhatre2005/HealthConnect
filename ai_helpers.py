"""
HealthConnect AI Helpers
Local Machine Learning Disease Prediction & Healthcare Decision Support
Powered by Random Forest + XGBoost Soft Voting Ensemble.
100% Offline / Local Inference. No external LLM or API keys required.
"""

import logging
from ml_engine.predictor import analyze_patient_symptoms, get_all_symptoms

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_symptoms(symptoms_list, additional_info="", age=None, gender=None, duration=None, severity=None,
                     patient_details=None, problem_description="", symptom_parameters=None, image_metadata=None):
    """
    Analyze patient symptoms using HealthConnect's dual-model local ensemble + 4-qubit Quantum ML pipeline.
    
    Args:
        symptoms_list (list): List of symptoms reported by the patient
        additional_info (str): Additional context or medical notes
        age (int/str, optional): Patient age
        gender (str, optional): Patient gender
        duration (str, optional): Symptom duration
        severity (str, optional): Patient perceived severity
        patient_details (dict, optional): Structured patient details
        problem_description (str, optional): Natural language problem description
        symptom_parameters (dict, optional): Symptom-specific parameter values
        image_metadata (dict, optional): Secure image metadata and visual features
        
    Returns:
        dict: Standardized analysis results including predictions, severity, specialist,
              emergency flags, quantum analysis, and medical disclaimer.
    """
    try:
        result = analyze_patient_symptoms(
            symptoms=symptoms_list,
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
        return result
    except Exception as e:
        logger.error(f"Error in analyze_symptoms: {e}", exc_info=True)
        return {
            "success": False,
            "error": "Failed to analyze symptoms through ML ensemble.",
            "predictions": [],
            "severity": "MODERATE",
            "specialist": "General Physician",
            "specialist_type": "General Physician",
            "immediate_actions": ["Consult with a qualified healthcare professional."],
            "emergency": False,
            "disclaimer": "This tool provides preliminary health information for awareness and decision support. It is not a medical diagnosis. Please consult a qualified healthcare professional for medical advice."
        }
