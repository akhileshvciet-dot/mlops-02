
import random
import joblib
from sklearn.linear_model import LogisticRegression

random.seed(42)

X = []
y = []

# Generate sample student data
for _ in range(500):
    study_hours = round(random.uniform(0, 10), 1)
    attendance = random.randint(30, 100)
    internal_marks = random.randint(0, 100)

    # Simple sample rule to generate labels
    score = (
        study_hours * 3
        + attendance * 0.25
        + internal_marks * 0.5
    )

    result = 1 if score >= 55 else 0

    X.append([study_hours, attendance, internal_marks])
    y.append(result)

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

joblib.dump(model, "student_model.pkl")

print("Model trained and saved successfully!")
