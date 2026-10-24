import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    matthews_corrcoef
)
input_dir = "."
output_dir = "."
os.makedirs(output_dir, exist_ok=True)
classification_tasks = [
    ("NAG", "AG"),
    ("NAG", "IM"),
    ("NAG", "GC"),
    ("AG", "IM"),
    ("AG", "GC"),
    ("IM", "GC")
]
random_seed = 42
rf_parameters = {
    "criterion": "entropy",
    "max_depth": 20,
    "n_estimators": 80,
    "random_state": random_seed
}
def calculate_metrics(
    model,
    X_data,
    y_true,
    dataset_name,
    group1,
    group2
):
    pos_label = group2
    neg_label = group1
    y_pred = model.predict(X_data)
    pos_index = list(model.classes_).index(pos_label)
    y_proba = model.predict_proba(X_data)[:, pos_index]
    y_true_binary = (
        np.asarray(y_true) == pos_label
    ).astype(int)
    y_pred_binary = (
        np.asarray(y_pred) == pos_label
    ).astype(int)
    negative_n = int(np.sum(y_true_binary == 0))
    positive_n = int(np.sum(y_true_binary == 1))
    roc_auc = roc_auc_score(
        y_true_binary,
        y_proba
    )
    accuracy = accuracy_score(
        y_true_binary,
        y_pred_binary
    )
    precision = precision_score(
        y_true_binary,
        y_pred_binary,
        zero_division=0
    )
    recall = recall_score(
        y_true_binary,
        y_pred_binary,
        zero_division=0
    )
    f1 = f1_score(
        y_true_binary,
        y_pred_binary,
        zero_division=0
    )
    mcc = matthews_corrcoef(
        y_true_binary,
        y_pred_binary
    )
    return {
        "Classification task": f"{group1} vs. {group2}",
        "Dataset": dataset_name,
        "Negative class": neg_label,
        "Positive class": pos_label,
        "N": len(y_true_binary),
        "Negative n": negative_n,
        "Positive n": positive_n,
        "ROC-AUC": roc_auc,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-score": f1,
        "MCC": mcc
    }
all_results = []
for group1, group2 in classification_tasks:
    print("\n" + "=" * 60)
    print(f" {group1} vs. {group2}")
    print(f" {group1}")
    print(f" {group2}")
    print("=" * 60)
    filename = os.path.join(
        input_dir,
        f"L6-HOMD-noHP-ML-{group1}&{group2}-SHAP01.csv"
    )
    if not os.path.exists(filename):
        print(f" {filename}")
        continue
    df = pd.read_csv(filename)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    classes = np.unique(y)
    if len(classes) != 2:
        raise ValueError(
            f"Expected two classes for {group1} vs. {group2}: "
            f" {classes}"
        )
    if group1 not in classes:
        raise ValueError(
            f"Missing negative class {group1}: "
            f" {classes}"
        )
    if group2 not in classes:
        raise ValueError(
            f"Missing positive class {group2}: "
            f" {classes}"
        )
    print(" ", classes)
    print(" ", len(y))

    print(y.value_counts())
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=random_seed,
        stratify=y
    )
    clf = RandomForestClassifier(
        **rf_parameters
    )
    clf.fit(
        X_train,
        y_train
    )
    train_metrics = calculate_metrics(
        model=clf,
        X_data=X_train,
        y_true=y_train,
        dataset_name="Train",
        group1=group1,
        group2=group2
    )
    test_metrics = calculate_metrics(
        model=clf,
        X_data=X_test,
        y_true=y_test,
        dataset_name="Test",
        group1=group1,
        group2=group2
    )
    all_results.append(train_metrics)
    all_results.append(test_metrics)
    current_results = pd.DataFrame([
        train_metrics,
        test_metrics
    ])
    metric_columns = [
        "ROC-AUC",
        "Accuracy",
        "Precision",
        "Recall",
        "F1-score",
        "MCC"
    ]
    current_results[metric_columns] = (
        current_results[metric_columns].round(4)
    )

    print(current_results.to_string(index=False))
if len(all_results) == 0:
    raise ValueError(
        "No tasks completed; check input files."
    )
all_results_df = pd.DataFrame(all_results)
metric_columns = [
    "ROC-AUC",
    "Accuracy",
    "Precision",
    "Recall",
    "F1-score",
    "MCC"
]
all_results_df[metric_columns] = (
    all_results_df[metric_columns].round(4)
)
all_output_path = os.path.join(
    output_dir,
    "L6-HOMD-noHP-all_metrics-SHAP01.csv"
)
all_results_df.to_csv(
    all_output_path,
    index=False,
    encoding="utf-8-sig"
)
test_results_df = all_results_df[
    all_results_df["Dataset"] == "Test"
].copy()
test_output_path = os.path.join(
    output_dir,
    "L6-HOMD-noHP-test_metrics-SHAP01.csv"
)
print("\n" + "=" * 60)

print("=" * 60)
print(
    test_results_df.to_string(index=False)
)

print(all_output_path)

test_results_df.to_csv(test_output_path, index=False)
print(test_output_path)
