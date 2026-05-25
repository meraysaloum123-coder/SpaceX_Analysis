from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

y_pred = svm.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()


from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
# نحول القيم لاحتمالات
y_prob = svm.decision_function(X_test)

fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, label="ROC curve (area = %0.2f)" % roc_auc)
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - SpaceX Model")
plt.legend()
plt.show()

from sklearn.model_selection import cross_val_score

scores = cross_val_score(svm, X_train, y_train, cv=5)

print("Cross Validation Scores:", scores)
print("Mean Accuracy:", scores.mean())

import numpy as np
import joblib

model = joblib.load("spacex_final_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_landing(payload_mass):
    data = np.array([[payload_mass]])
    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)
    
    if prediction[0] == 1:
        return "Landing Success 🚀"
    else:
        return "Landing Failure ❌"

# تجربة
print(predict_landing(8000))
print(predict_landing(2000))
