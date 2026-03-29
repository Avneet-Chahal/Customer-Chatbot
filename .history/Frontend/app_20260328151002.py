import streamlit as st
import joblib

# Load model and vectorizer
model = joblib.load("../Models/intent_model.pkl")
vectorizer = joblib.load("../Models/vectorizer.pkl")

# Predict function (safe version)
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

# Page config
st.set_page_config(page_title="Customer Chatbot", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>🤖 Customer Support Chatbot</h1>", unsafe_allow_html=True)

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.history = []

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input
user_input = st.text_input("You:")

if user_input:
    st.session_state.history.append(("You", user_input))

    # Handle vague input
    if user_input.lower() in ["issue", "problem", "help"]:
        bot_response = "Could you please describe your issue in more detail?"

    # Smart combined query handling
    elif "refund" in user_input and "late" in user_input:
        bot_response = "I see your order is delayed and you want a refund. Let me help you with that."

    else:
        with st.spinner("Bot is typing..."):
            intent, confidence = predict_intent(user_input)

            if confidence > 0.40:
                bot_response = responses.get(intent, "Let me help you with that.")
            else:
                bot_response = "I'm not sure I understood. Could you please rephrase?"

        # Show intent (for demo)
        st.caption(f"Intent: {intent}")

    st.session_state.history.append(("Bot", bot_response))

# Chat display (bubble style)
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(
            f"<div style='text-align:right; background:#1f77b4; padding:10px; border-radius:10px; margin:5px; color:white;'>🧑 {message}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align:left; background:#2ecc71; padding:10px; border-radius:10px; margin:5px; color:black;'>🤖 {message}</div>",
            unsafe_allow_html=True
        )