from services.llm_service import llm_service
from services.ml_service import ml_service
from models.schemas import DiseasePredictionRequest

print("Testing LLM mock fallback endpoint...")
resp1 = llm_service.generate_response("test_session_1", "Hello, I am feeling fine today!")
print(f"Resp1 requires symptoms? {resp1.requires_symptoms}")

resp2 = llm_service.generate_response("test_session_1", "I have severe chest pain and my heart hurts.")
print(f"Resp2 requires symptoms? {resp2.requires_symptoms} - {resp2.response}")

history = llm_service.get_history("test_session_1")
assert len(history) == 5 # 1 system, 2 user, 2 assistant

print("\nTesting ML service prediction...")
req = DiseasePredictionRequest(
    age=63, sex=1, cp=3, trestbps=145, chol=233, fbs=1,
    restecg=0, thalach=150, exang=0, oldpeak=2.3, slope=0, ca=0, thal=1
)
ml_resp = ml_service.predict(req)
print(f"ML Prediction: {ml_resp.prediction}, Risk: {ml_resp.risk_level}")

print("\nAll Tests Passed Successfully!")
