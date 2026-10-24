import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.family'] = 'Times New Roman'
group1 = "NAG"
group2 = "IR"
filename = f'L6-HOMD-noHP-ML-{group1}&{group2}-SHAP01.csv'
output_path = f'L6-HOMD-noHP-{group1}&{group2}-ROC-SHAP01.png'
df = pd.read_csv(filename)
X = df.values[:, :-1]
y = df.values[:, -1]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=0.8, random_state=0, stratify=y
)
clf = RandomForestClassifier(criterion='entropy', max_depth=20, n_estimators=80, random_state=0)
clf.fit(X_train, y_train)
classes = np.unique(y)
if len(classes) != 2:
    raise ValueError(f'Expected two classes, found {len(classes)}: {classes}')
pos_label = classes[1]
pos_index = list(clf.classes_).index(pos_label)
y_proba_train = clf.predict_proba(X_train)[:, pos_index]
y_proba_test = clf.predict_proba(X_test)[:, pos_index]
fpr_train, tpr_train, _ = roc_curve(y_train, y_proba_train, pos_label=pos_label)
fpr_test, tpr_test, _   = roc_curve(y_test,  y_proba_test,  pos_label=pos_label)
roc_auc_train = auc(fpr_train, tpr_train)
roc_auc_test  = auc(fpr_test, tpr_test)
plt.figure(figsize=(6, 6))
plt.plot(fpr_train, tpr_train, color='#7789B7', lw=3,
         label=f'Train ROC (AUC = {roc_auc_train:.2f})')
plt.plot(fpr_test,  tpr_test,  color='#89AA7B', lw=3,
         label=f'Test ROC (AUC = {roc_auc_test:.2f})')
plt.plot([0, 1], [0, 1], color='grey', lw=1, linestyle='--')
plt.title(f'{group1} vs. {group2} Binarization', fontsize=16)
plt.xlabel('False Positive Rate', fontsize=16)
plt.ylabel('True Positive Rate', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc='lower right', fontsize=14)
os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.1, transparent=True)
plt.show()
print(' ', output_path)
