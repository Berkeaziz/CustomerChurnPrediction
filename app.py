from fastapi import FastAPI
import joblib
import pandas as pd
import json

app = FastAPI()

model = joblib.load("models/xgb_model.pkl")

with open("models/feature_columns.json", "r") as f:
    FEATURE_COLS = json.load(f)

THRESHOLD = 0.24

@app.get("/")
def home():
    return {"message": "Churn Prediction API is running"}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])

    for col in FEATURE_COLS:
        if col not in df.columns:
            df[col] = 0

    df = df[FEATURE_COLS]

    proba = model.predict_proba(df)[0][1]
    pred = int(proba >= THRESHOLD)

    return {
        "churn_probability": float(proba),
        "prediction": pred,
        "threshold": THRESHOLD
    }