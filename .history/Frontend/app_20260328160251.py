import streamlit as st
import joblib
import datetime
import os
from memory import load_history, save_message
from recommender import get_best_match

# ---------------- LOAD MODEL ----------------
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "Models", "intent_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "Models", "vectorizer.pkl")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)


# ---------------- PREDICT FUNCTION ----------------
def predict_intent(text):
    text = text.lower().strip()
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    return prediction

# ---------------- RESPONSES ----------------
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

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Customer Chatbot", layout="centered")

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align: center;'>🤖 Smart Customer Chatbot</h1>", unsafe_allow_html=True)

# ---------------- INIT SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "input" not in st.session_state:
    st.session_state.input = ""

# ---------------- CLEAR BUTTON ----------------
if st.button("🧹 Clear Chat"):
    st.session_state.history = []
    st.session_state.input = ""
    if os.path.exists("chat_history.json"):
        os.remove("chat_history.json")

# ---------------- WELCOME ----------------
if not st.session_state.history:
    st.info("👋 Welcome! Ask me anything about orders, refunds, or issues.")
    st.write("💡 Try:")
    st.write("- Track my order")
    st.write("- Refund my money")
    st.write("- My delivery is late")

# ---------------- INPUT ----------------
user_input = st.text_input(
    "",
    value=st.session_state.input,
    placeholder="Type your message here..."
)

# ---------------- MAIN LOGIC (ONLY ONE BLOCK) ----------------
if st.button("Send") and user_input:

    time = datetime.datetime.now().strftime("%H:%M")

    # Save user message
    st.session_state.history.append(("You", user_input, time))

    # Load memory
    history = load_history()

    # Step 1: Try recommendation system
    matched_response, score = get_best_match(user_input, history)

    # Step 2: Decision flow
    if score > 0.7:
        bot_response = matched_response

    elif score > 0.4:
        bot_response = f"I think this might help: {matched_response}"

    else:
        # Step 3: fallback to ML model
        if user_input.lower() in ["issue", "problem", "help"]:
            bot_response = "🤖 Could you please describe your issue in more detail?"

        elif "refund" in user_input and "late" in user_input:
            bot_response = "🤖 I see your order is delayed and you want a refund. Let me help you with that."

        else:
            with st.spinner("Bot is typing..."):
                intent = predict_intent(user_input)
                bot_response = responses.get(
                    intent,
                    "🤖 I'm not sure I understood. Could you please rephrase?"
                )

    # Save to memory
    save_message(user_input, bot_response)

    # Save bot response to UI
    st.session_state.history.append(("Bot", bot_response, time))

    # Clear input
    st.session_state.input = ""

# ---------------- DISPLAY CHAT ----------------
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