
from flask import Flask, request, render_template_string
import joblib
import os

app = Flask(__name__)

MODEL_VERSION = os.environ.get("MODEL_VERSION", "1.0")
model = joblib.load("student_model.pkl")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Result Predictor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background: #f2f5f9;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
        }
        input, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            box-sizing: border-box;
        }
        button {
            background: #1769e0;
            color: white;
            border: 0;
            border-radius: 6px;
            cursor: pointer;
        }
        .result { font-size: 22px; font-weight: bold; }
    </style>
</head>
<body>
<div class="card">
    <h1>Student Result Predictor</h1>
    <p>Model Version: {{ version }}</p>

    <form method="POST">
        <label>Study Hours (0–10)</label>
        <input type="number" name="hours"
               min="0" max="10" step="0.1" required>

        <label>Attendance (%)</label>
        <input type="number" name="attendance"
               min="0" max="100" required>

        <label>Internal Marks (0–100)</label>
        <input type="number" name="marks"
               min="0" max="100" required>

        <button type="submit">Predict Result</button>
    </form>

    {% if result %}
        <p class="result">Prediction: {{ result }}</p>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        try:
            hours = float(request.form["hours"])
            attendance = float(request.form["attendance"])
            marks = float(request.form["marks"])

            if not (0 <= hours <= 10
                    and 0 <= attendance <= 100
                    and 0 <= marks <= 100):
                raise ValueError("Invalid input")

            prediction = model.predict(
                [[hours, attendance, marks]]
            )[0]

            result = "Pass" if prediction == 1 else "Fail"

        except (ValueError, TypeError):
            result = "Invalid input. Please check your values."

    return render_template_string(
        HTML, version=MODEL_VERSION, result=result
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
