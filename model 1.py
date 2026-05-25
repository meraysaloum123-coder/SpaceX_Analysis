import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score 

df = pd.read_csv("spacex_cleaned_data.csv")
df.head()

le_rocket = LabelEncoder()
le_site = LabelEncoder()

df["rocket_name"] = le_rocket.fit_transform(df["rocket_name"])
df["launch_site"] = le_site.fit_transform(df["launch_site"])


# Features & target
X = df[[
"flight_number",
"payload_mass",
"rocket_name",
"launch_site"
]]

y = df["success"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=42
)
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# 7) Ensemble Model 
# =========================

model1 = LogisticRegression(max_iter=5000)
model2 = DecisionTreeClassifier()
model3 = SVC() 
ensemble = VotingClassifier(
    estimators=[
        ('lr', model1),
        ('dt', model2),
        ('svc', model3)
    ],
    voting='soft'
)
ensemble.fit(X_train, y_train)
y_pred = ensemble.predict(X_test)

# =========================
# 9) Evaluation
# =========================

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
