import joblib
import os
import numpy as np
from models.schemas import DiseasePredictionRequest, DiseasePredictionResponse

class MLService:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        model_path = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'rf_heart_disease.joblib')
        try:
            self.model = joblib.load(model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def predict(self, data: DiseasePredictionRequest) -> DiseasePredictionResponse:
        if not self.model:
            raise Exception("Model is not loaded.")

        # Prepare features in the exact order as training
        # Features: age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal
        features = np.array([[
            data.age, data.sex, data.cp, data.trestbps, data.chol, 
            data.fbs, data.restecg, data.thalach, data.exang, 
            data.oldpeak, data.slope, data.ca, data.thal
        ]])

        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0][1]

        risk_level = "Low Risk"
        recommendation = "Maintain a healthy lifestyle."

        if probability > 0.7:
            risk_level = "High Risk"
            recommendation = "URGENT: Please consult a cardiologist immediately."
        elif probability > 0.4:
            risk_level = "Moderate Risk"
            recommendation = "Please schedule a checkup with your doctor soon."

        return DiseasePredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            risk_level=risk_level,
            recommendation=recommendation
        )

ml_service = MLService()
