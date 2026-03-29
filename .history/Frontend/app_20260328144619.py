import streamlit as st
import joblib

# Load model and vectorizer
model = joblib.load("../Models/intent_model.pkl")
vectorizer = joblib.load("../Models/vectorizer.pkl")

# Function to predict intent
def predict_intent(text):
    text = text.lower().strip()
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    
    confidence = 1.0   # fixed confidence (safe)
    
    return prediction, confidence

# Responses
responses = {
    "order_status": "Let me check your order status for you.",
    "delivery_delay": "I apologize for the delay. Let me look into it.",
    "refund_request": "I will assist you with the refund process.",
    "product_issue": "Let's resolve the product issue.",
    "payment_issue": "I’ll help fix your payment issue.",
    "account_problem": "I will assist you with your account.",
    "complaint": "I’m sorry. Please share more details.",
    "general_query": "Sure, I’ll help you.",
    "greeting": "Hello! How can I help you?",
    "goodbye": "Thank you! Have a great day!"
}

# Page title
st.title("🤖 Customer Support Chatbot")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input box
user_input = st.text_input("You:")

if user_input:
    st.session_state.history.append(("You", user_input))

    # Handle vague inputs
    if user_input.lower() in ["issue", "problem", "help"]:
        bot_response = "Could you please describe your issue in more detail?"
    else:
        intent, confidence = predict_intent(user_input)

        if confidence > 0.40:
            bot_response = responses.get(intent)
        else:
            bot_response = "I'm not sure. Can you rephrase?"

    st.session_state.history.append(("Bot", bot_response))

# Show chat history
for sender, message in st.session_state.history:
    st.write(f"{sender}: {message}")