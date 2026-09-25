# benchmark_models.py

import os
import time
import json
import warnings

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = "data/dataset.csv"
RESULTS_PATH = "models/benchmark_results.json"

RANDOM_STATE = 42
TEST_SIZE = 0.20


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    print("\nDataset shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    return df


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(df):

    # Change this only if your actual target column has
    # a different name.
    possible_targets = [
        "prognosis",
        "disease",
        "target",
        "label",
        "Disease"
    ]

    target_column = None

    for column in possible_targets:
        if column in df.columns:
            target_column = column
            break

    if target_column is None:
        raise ValueError(
            "Could not find target column. "
            "Expected one of: "
            + ", ".join(possible_targets)
        )

    print("\nTarget column:", target_column)

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Convert categorical feature columns to numeric
    X = pd.get_dummies(X)

    # Handle missing values
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)

    # Encode target labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y.astype(str))

    print("Number of features:", X.shape[1])
    print("Number of classes:", len(label_encoder.classes_))

    return (
        X.astype(np.float32),
        y_encoded,
        label_encoder
    )


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

def split_data(X, y):

    return train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )


# ============================================================
# EVALUATION
# ============================================================

def evaluate_model(name, model, X_train, X_test, y_train, y_test):

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    start = time.perf_counter()

    model.fit(X_train, y_train)

    training_time = time.perf_counter() - start

    start = time.perf_counter()

    predictions = model.predict(X_test)

    inference_time = time.perf_counter() - start

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    result = {
        "model": name,
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "training_time_seconds": float(training_time),
        "inference_time_seconds": float(inference_time),
        "test_samples": int(len(y_test))
    }

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    print(
        f"Training time  : "
        f"{training_time:.4f} sec"
    )

    print(
        f"Inference time : "
        f"{inference_time:.4f} sec"
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    return result, model


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("HEALTHCONNECT MODEL BENCHMARK")
    print("=" * 60)

    # Load
    df = load_dataset()

    # Prepare
    X, y, label_encoder = prepare_data(df)

    # Split
    X_train, X_test, y_train, y_test = split_data(X, y)

    print("\nTraining samples:", len(X_train))
    print("Testing samples :", len(X_test))

    # --------------------------------------------------------
    # RANDOM FOREST
    # --------------------------------------------------------

    rf = RandomForestClassifier(
        n_estimators=100,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced"
    )

    # --------------------------------------------------------
    # XGBOOST
    # --------------------------------------------------------

    num_classes = len(np.unique(y))

    if num_classes > 2:

        xgb = XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="multi:softprob",
            num_class=num_classes,
            eval_metric="mlogloss",
            random_state=RANDOM_STATE,
            n_jobs=-1
        )

    else:

        xgb = XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_jobs=-1
        )

    # --------------------------------------------------------
    # SVM BASELINE
    # --------------------------------------------------------

    svm = SVC(
        kernel="rbf",
        probability=True,
        random_state=RANDOM_STATE
    )

    # --------------------------------------------------------
    # RUN BENCHMARKS
    # --------------------------------------------------------

    results = []

    models = [
        ("Random Forest", rf),
        ("XGBoost", xgb),
        ("SVM", svm)
    ]

    trained_models = {}

    for name, model in models:

        result, trained_model = evaluate_model(
            name,
            model,
            X_train,
            X_test,
            y_train,
            y_test
        )

        results.append(result)
        trained_models[name] = trained_model

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    results_df = pd.DataFrame(results)

    print("\n")
    print("=" * 80)
    print("BENCHMARK SUMMARY")
    print("=" * 80)

    print(
        results_df[
            [
                "model",
                "accuracy",
                "precision",
                "recall",
                "f1_score",
                "inference_time_seconds"
            ]
        ].to_string(index=False)
    )

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    os.makedirs(
        os.path.dirname(RESULTS_PATH),
        exist_ok=True
    )

    with open(
        RESULTS_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "dataset": DATASET_PATH,
                "test_size": TEST_SIZE,
                "random_state": RANDOM_STATE,
                "results": results
            },
            f,
            indent=4
        )

    print(
        f"\nBenchmark results saved to: "
        f"{RESULTS_PATH}"
    )

    # --------------------------------------------------------
    # BEST MODEL
    # --------------------------------------------------------

    best = max(
        results,
        key=lambda x: x["f1_score"]
    )

    print("\nBest model based on weighted F1:")
    print(best["model"])

    print(
        f"F1 Score: "
        f"{best['f1_score']:.4f}"
    )


if __name__ == "__main__":
    main()