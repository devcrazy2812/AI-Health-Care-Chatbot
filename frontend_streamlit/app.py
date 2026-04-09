import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000/api"

# Configure the Streamlit page
st.set_page_config(page_title="AI Healthcare Assistant", page_icon="⚕️", layout="centered")

# Custom CSS for a better aesthetic
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(to right, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: sans-serif;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #94a3b8;
        margin-top: -10px;
        margin-bottom: 40px;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(30, 41, 59, 0.8);
        border-left: 5px solid #3b82f6;
        margin-top: 20px;
    }
    .risk-High {
        border-left-color: #ef4444 !important;
        background-color: rgba(239, 68, 68, 0.1) !important;
    }
    .risk-Low {
        border-left-color: #10b981 !important;
        background-color: rgba(16, 185, 129, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>AI Healthcare Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Powered by LLM & Machine Learning<br/><small>Created by: devcrazy AKA Abhay Goyal</small></p>", unsafe_allow_html=True)

# Generate a random session ID if not exists
if "session_id" not in st.session_state:
    import random, string
    st.session_state.session_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Healthcare Assistant. How can I help you today?"}
    ]

if "requires_symptoms" not in st.session_state:
    st.session_state.requires_symptoms = False

# Draw chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input block
prompt = st.chat_input("Describe your symptoms or ask a medical question...")

if prompt:
    # 1. Update UI with user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call FastAPI backend
    with st.spinner("AI is thinking..."):
        try:
            req_data = {
                "session_id": st.session_state.session_id,
                "message": prompt
            }
            res = requests.post(f"{API_BASE}/chat/", json=req_data)
            
            if res.status_code == 200:
                resp_json = res.json()
                bot_reply = resp_json.get("response", "No response from AI")
                
                # Check if symptom form was triggered
                if resp_json.get("requires_symptoms"):
                    st.session_state.requires_symptoms = True
                
                # Append bot message
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                with st.chat_message("assistant"):
                    st.markdown(bot_reply)

            else:
                st.error("Failed to fetch response from API.")
        except Exception as e:
            st.error(f"Error connecting to backend API: {e}. Please make sure backend is running.")

# Render Symptom form if triggered
if st.session_state.requires_symptoms:
    st.markdown("---")
    st.subheader("⚕️ Heart Disease Risk Assessment Form")
    st.markdown("Please provide your clinical metrics below for ML-based evaluation:")

    with st.form("symptoms_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=45)
            trestbps = st.number_input("Resting BP (mm Hg)", value=120)
            restecg = st.selectbox("Resting ECG (0-2)", [0, 1, 2], index=1)
            oldpeak = st.number_input("ST Depression", value=1.0, format="%.2f")
            thal = st.selectbox("Thal (0-3)", [0, 1, 2, 3], index=2)
            
        with col2:
            sex = st.selectbox("Sex", options=[1, 0], format_func=lambda x: "Male" if x==1 else "Female")
            chol = st.number_input("Cholesterol (mg/dl)", value=200)
            thalach = st.number_input("Max Heart Rate", value=150)
            slope = st.selectbox("Slope (0-2)", [0, 1, 2], index=1)
            
        with col3:
            cp = st.selectbox("Chest Pain Type (0-3)", [0, 1, 2, 3], index=1)
            fbs = st.selectbox("Fasting Blood Sugar > 120?", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
            exang = st.selectbox("Exercise Induced Angina?", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
            ca = st.selectbox("Major Vessels (0-3)", [0, 1, 2, 3], index=0)

        submit = st.form_submit_button("Run Prediction Model")

    if submit:
        payload = {
            "age": age, "sex": sex, "cp": cp, "trestbps": trestbps, "chol": chol, "fbs": fbs,
            "restecg": restecg, "thalach": thalach, "exang": exang, "oldpeak": oldpeak,
            "slope": slope, "ca": ca, "thal": thal
        }
        
        with st.spinner("Analyzing your clinical data..."):
            try:
                res = requests.post(f"{API_BASE}/predict/", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    risk = data['risk_level']
                    risk_class = "risk-High" if "High Risk" in risk else ("risk-Low" if "Low Risk" in risk else "")
                    
                    st.markdown(f"""
                    <div class="prediction-box {risk_class}">
                        <h4>Analysis Complete: {risk}</h4>
                        <p style="margin-bottom: 5px;">{data['recommendation']}</p>
                        <p style="font-size: 13px; opacity: 0.8; margin-top:0px;">Confidence: {data['probability']*100:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Prediction failed.")
            except Exception as e:
                st.error(f"Error connecting to backend API: {e}")
