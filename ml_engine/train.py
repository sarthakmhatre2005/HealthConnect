"""
HealthConnect Model Training Script
Trains a dual-model ensemble:
1. Scikit-learn RandomForestClassifier
2. XGBoost XGBClassifier
Saves trained models, encoders, and clinical metadata into ml_engine/models/
"""

import os
import sys

# Ensure parent dir is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import random
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, top_k_accuracy_score
import xgboost as xgb

from ml_engine.dataset import SYMPTOMS, DISEASE_SYMPTOM_MAP, DISEASE_KNOWLEDGE_BASE

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def generate_training_data(samples_per_disease=100, random_seed=42):
    """
    Generates realistic clinical training samples:
    - Full symptom set
    - Subsets (patients don't always exhibit all symptoms)
    - Slight noise (occasional unrelated symptoms)
    """
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    num_symptoms = len(SYMPTOMS)
    symptom_to_idx = {s: i for i, s in enumerate(SYMPTOMS)}
    
    X = []
    y = []
    
    for disease, char_symptoms in DISEASE_SYMPTOM_MAP.items():
        char_indices = [symptom_to_idx[s] for s in char_symptoms if s in symptom_to_idx]
        
        for _ in range(samples_per_disease):
            vec = np.zeros(num_symptoms, dtype=np.float32)
            
            # Select random subset of disease symptoms (at least 2 if available)
            min_k = min(2, len(char_indices))
            max_k = len(char_indices)
            k = random.randint(min_k, max_k)
            chosen_char = random.sample(char_indices, k)
            
            for idx in chosen_char:
                vec[idx] = 1.0
                
            # Slight random noise: 10% chance of 1 unrelated symptom
            if random.random() < 0.10:
                unrelated_pool = [i for i in range(num_symptoms) if i not in char_indices]
                if unrelated_pool:
                    noise_idx = random.choice(unrelated_pool)
                    vec[noise_idx] = 1.0
                    
            X.append(vec)
            y.append(disease)
            
    return np.array(X, dtype=np.float32), np.array(y)

def train_and_save():
    print("==================================================")
    print(" HealthConnect ML Engine Training (RF + XGBoost) ")
    print("==================================================")
    
    X, y = generate_training_data(samples_per_disease=120)
    print(f"Generated {len(X)} clinical training instances across {len(set(y))} diseases.")
    print(f"Feature vector dimensionality: {X.shape[1]} binary symptoms.")
    
    # Label encoding
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    print(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")
    
    # 1. Train Random Forest
    print("\n[1/2] Training RandomForestClassifier (120 trees)...")
    rf_model = RandomForestClassifier(
        n_estimators=120,
        max_depth=18,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    rf_probs = rf_model.predict_proba(X_test)
    rf_acc = accuracy_score(y_test, rf_preds)
    rf_top3 = top_k_accuracy_score(y_test, rf_probs, k=3)
    print(f"  -> Random Forest Test Accuracy: {rf_acc * 100:.2f}%")
    print(f"  -> Random Forest Top-3 Accuracy: {rf_top3 * 100:.2f}%")
    
    # 2. Train XGBoost
    print("\n[2/2] Training XGBoost XGBClassifier...")
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.08,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="multi:softprob",
        eval_metric="mlogloss",
        random_state=42,
        n_jobs=-1
    )
    xgb_model.fit(X_train, y_train)
    xgb_preds = xgb_model.predict(X_test)
    xgb_probs = xgb_model.predict_proba(X_test)
    xgb_acc = accuracy_score(y_test, xgb_preds)
    xgb_top3 = top_k_accuracy_score(y_test, xgb_probs, k=3)
    print(f"  -> XGBoost Test Accuracy: {xgb_acc * 100:.2f}%")
    print(f"  -> XGBoost Top-3 Accuracy: {xgb_top3 * 100:.2f}%")
    
    # 3. Ensemble Evaluation
    ensemble_probs = (rf_probs + xgb_probs) / 2.0
    ensemble_preds = np.argmax(ensemble_probs, axis=1)
    ensemble_acc = accuracy_score(y_test, ensemble_preds)
    ensemble_top3 = top_k_accuracy_score(y_test, ensemble_probs, k=3)
    print("\n[Ensemble Model Combination]")
    print(f"  -> Ensemble Accuracy: {ensemble_acc * 100:.2f}%")
    print(f"  -> Ensemble Top-3 Accuracy: {ensemble_top3 * 100:.2f}%")
    
    # 4. Save Artifacts
    print("\nSaving trained models and encoders to disk...")
    rf_path = os.path.join(MODELS_DIR, "random_forest.joblib")
    xgb_path = os.path.join(MODELS_DIR, "xgboost.joblib")
    symptom_encoder_path = os.path.join(MODELS_DIR, "symptom_encoder.joblib")
    label_encoder_path = os.path.join(MODELS_DIR, "label_encoder.joblib")
    kb_path = os.path.join(MODELS_DIR, "knowledge_base.json")
    
    joblib.dump(rf_model, rf_path)
    joblib.dump(xgb_model, xgb_path)
    joblib.dump(label_encoder, label_encoder_path)
    
    symptom_metadata = {
        "symptoms": SYMPTOMS,
        "symptom_to_idx": {s: i for i, s in enumerate(SYMPTOMS)},
        "num_symptoms": len(SYMPTOMS)
    }
    joblib.dump(symptom_metadata, symptom_encoder_path)
    
    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(DISEASE_KNOWLEDGE_BASE, f, indent=2)
        
    print(f"[OK] Saved Random Forest model: {rf_path}")
    print(f"[OK] Saved XGBoost model: {xgb_path}")
    print(f"[OK] Saved Label Encoder: {label_encoder_path}")
    print(f"[OK] Saved Symptom Encoder: {symptom_encoder_path}")
    print(f"[OK] Saved Knowledge Base: {kb_path}")
    print("==================================================")
    print(" Training completed successfully! ")
    print("==================================================")

if __name__ == "__main__":
    train_and_save()
