import os
from typing import Dict, List
from openai import OpenAI
from models.schemas import ChatResponse
from dotenv import load_dotenv

load_dotenv()

# In-memory history for simplicity (session_id -> list of messages)
# In production, use Redis or a Database
chat_history: Dict[str, List[Dict[str, str]]] = {}

SYSTEM_PROMPT = """
You are a highly advanced AI Healthcare Assistant. Your role is to help users understand their symptoms and provide general healthcare advice.
IMPORTANT: You are NOT a doctor. You must append a disclaimer to your responses if giving medical advice: "*Disclaimer: I am an AI, not a medical professional. Please consult a doctor for medical advice.*"

If the user mentions symptoms related to heart disease (like chest pain, high blood pressure, cholesterol, etc.), you should kindly ask them to fill out the Heart Disease Risk Assessment form. To trigger this form, you must include the exact phrase "TRIGGER_SYMPTOM_FORM" in your response.

Be empathetic, concise, and professional.
"""

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        if session_id not in chat_history:
            chat_history[session_id] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
        return chat_history[session_id]

    def add_message(self, session_id: str, role: str, content: str):
        history = self.get_history(session_id)
        history.append({"role": role, "content": content})
        # Keep history bounded memory
        if len(history) > 20:
            chat_history[session_id] = [history[0]] + history[-19:]

    def generate_response(self, session_id: str, user_message: str) -> ChatResponse:
        self.add_message(session_id, "user", user_message)
        
        requires_symptoms = False
        message_content = ""

        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.get_history(session_id)
                )
                message_content = response.choices[0].message.content
            except Exception as e:
                message_content = f"Sorry, I encountered an error communicating with the LLM API: {e}"
        else:
            # Mock fallback if no API key
            lower_msg = user_message.lower()
            if "chest" in lower_msg or "heart" in lower_msg or "pain" in lower_msg:
                message_content = "I noticed you mentioned symptoms that could be related to heart health. To better assist you, could you please provide some specific vitals? TRIGGER_SYMPTOM_FORM\n\n*Disclaimer: I am an AI, not a doctor. Seek immediate medical attention if you are experiencing a heart attack.*"
            else:
                message_content = "I understand. Can you tell me more about how you are feeling? \n\n*Disclaimer: Provide OpenAI API key for full AI capabilities.*"

        if "TRIGGER_SYMPTOM_FORM" in message_content:
            requires_symptoms = True
            message_content = message_content.replace("TRIGGER_SYMPTOM_FORM", "").strip()

        self.add_message(session_id, "assistant", message_content)

        return ChatResponse(
            response=message_content,
            requires_symptoms=requires_symptoms,
            symptoms_context="heart_disease" if requires_symptoms else None
        )

llm_service = LLMService()
