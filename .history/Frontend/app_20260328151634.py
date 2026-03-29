import streamlit as st
import joblib
import datetime

# Load model
model = joblib.load("../Models/intent_model.pkl")
vectorizer = joblib.load("../Models/vectorizer.pkl")

# Predict function
def predict_intent(text):
    text = text.lower().strip()
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    return prediction

# Responses
responses = {
    "order_status": "📦 Let me check your order status for you.",
    "delivery_delay": "⏳ I apologize for the delay. Let me look into it.",
    "refund_request": "💰 I will assist you with the refund process.",
    "product_issue": "🛠️ Let's resolve the product issue.",
    "payment_issue": "💳 I’ll help fix your payment issue.",
    "account_problem": "🔐 I will assist you with your account.",
    "complaint": "😔 I’m sorry. Please share more details.",
    "general_query": "🤝 Sure, I’ll help you.",
    "greeting": "👋 Hello! How can I help you today?",
    "goodbye": "👋 Thank you! Have a great day!"
}

# Page config
st.set_page_config(page_title="Customer Chatbot", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>🤖 Smart Customer Chatbot</h1>", unsafe_allow_html=True)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.history = []

# Input box
user_input = st.text_input("You:", placeholder="Type your message here...")

if user_input:
    time = datetime.datetime.now().strftime("%H:%M")

    # Add user message
    st.session_state.history.append(("You", user_input, time))

    # Handle vague input
    if user_input.lower() in ["issue", "problem", "help"]:
        bot_response = "🤖 Could you please describe your issue in more detail?"

    # Smart combined query
    elif "refund" in user_input and "late" in user_input:
        bot_response = "🤖 I see your order is delayed and you want a refund. Let me help you with that."

    else:
        with st.spinner("Bot is typing..."):
            intent = predict_intent(user_input)
            bot_response = responses.get(intent, "🤖 I'm not sure I understood. Could you rephrase?")

    # Add bot response
    st.session_state.history.append(("Bot", bot_response, time))

# Display chat (bubble style)
for sender, message, time in st.session_state.history:
    if sender == "You":
        st.markdown(
            f"""
            <div style='text-align:right; background:#1f77b4; padding:10px; border-radius:10px; margin:5px; color:white;'>
            🧑 {message}<br><span style='font-size:10px;'>{time}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='text-align:left; background:#2ecc71; padding:10px; border-radius:10px; margin:5px; color:black;'>
            🤖 {message}<br><span style='font-size:10px;'>{time}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

