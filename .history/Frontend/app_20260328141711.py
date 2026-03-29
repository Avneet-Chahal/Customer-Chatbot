import streamlit as st
import joblib

model = joblib.load("../Models/intent_model.pkl")
vectorizer = joblib.load("../Models/vectorizer.pkl")

def predict_intent(text):
    text = text.lower().strip()
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    confidence = max(model.predict_proba(text_vec)[0])
    return prediction, confidence

responses = {
    "order_status": "Let me check your order status for you.",
    "delivery_delay": "I apologize for the delay.",
    "refund_request": "I will assist you with refund.",
    "product_issue": "Let’s resolve the issue.",
    "payment_issue": "I’ll help fix payment issue.",
    "account_problem": "I will help with your account.",
    "complaint": "Sorry for inconvenience.",
    "general_query": "Sure, I’ll help you.",
    "greeting": "Hello! How can I help?",
    "goodbye": "Thank you! Have a great day!"
}

st.title("🤖 Customer Chatbot")

user_input = st.text_input("You:")

if user_input:
    intent, confidence = predict_intent(user_input)

    if confidence > 0.40:
        response = responses.get(intent)
    else:
        response = "I'm not sure. Can you rephrase?"

    st.write("Bot:", response)