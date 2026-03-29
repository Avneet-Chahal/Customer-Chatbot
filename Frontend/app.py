import streamlit as st
import joblib
import datetime
import os
import time
from memory import load_history, save_message
from recommender import get_best_match

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "Models", "intent_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "Models", "vectorizer.pkl")

# ---------------- LOAD MODEL ----------------
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
st.set_page_config(page_title="Smart Chatbot", layout="centered")
st.markdown("### 🤖 Smart Customer Support Assistant")

# ---------------- SESSION INIT ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- CLEAR CHAT ----------------
if st.button("🧹 Clear Chat"):
    st.session_state.history = []
    file_path = os.path.join(BASE_DIR, "chat_history.json")
    if os.path.exists(file_path):
        os.remove(file_path)
    st.success("Chat cleared!")

# ---------------- WELCOME ----------------
if not st.session_state.history:
    st.info("👋 Welcome! Ask me anything about orders, refunds, or issues.")
    st.write("💡 Try:")
    st.write("- Track my order")
    st.write("- Refund my money")
    st.write("- My delivery is late")

# ---------------- QUICK ACTION BUTTONS ----------------
st.markdown("### 💡 Quick Actions")

col1, col2, col3 = st.columns(3)

if col1.button("📦 Track Order"):
    st.session_state.quick_input = "track my order"

if col2.button("💰 Refund"):
    st.session_state.quick_input = "refund my money"

if col3.button("🚚 Delivery Issue"):
    st.session_state.quick_input = "my delivery is late"

# ---------------- DISPLAY CHAT ----------------
for sender, message, time_stamp in st.session_state.history:
    if sender == "You":
        with st.chat_message("user"):
            st.write(message)
            st.caption(time_stamp)
    else:
        with st.chat_message("assistant"):
            st.write(message)
            st.caption(time_stamp)

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Type your message...")

# Handle quick buttons
if "quick_input" in st.session_state:
    user_input = st.session_state.quick_input
    del st.session_state.quick_input

# ---------------- MAIN LOGIC ----------------
if user_input:

    time_now = datetime.datetime.now().strftime("%H:%M")
    user_text = user_input.lower().strip()

    # Save user message
    st.session_state.history.append(("You", user_input, time_now))

    # ---------------- STOP / EXIT ----------------
    if user_text in ["stop", "exit", "quit", "bye"]:
        bot_response = "👋 Chat ended. Feel free to start a new conversation!"

    else:
        history = load_history()
        matched_response, score = get_best_match(user_input, history)

        if score > 0.7:
            bot_response = matched_response

        elif score > 0.4:
            bot_response = f"I think this might help: {matched_response}"

        else:
            if user_text in ["issue", "problem", "help"]:
                bot_response = "🤖 Could you please describe your issue in more detail?"

            elif "refund" in user_text and "late" in user_text:
                bot_response = "🤖 I see your order is delayed and you want a refund. Let me help you with that."

            else:
                intent = predict_intent(user_input)
                bot_response = responses.get(
                    intent,
                    "🤖 I'm not sure I understood. Try asking about orders, refunds, or delivery issues."
                )

    # Save to memory (only once)
    save_message(user_input, bot_response)

    # ---------------- TYPING ANIMATION ----------------
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("🤖 Typing...")
        time.sleep(1.2)
        placeholder.markdown(bot_response)
        st.caption(time_now)

    # Save bot response
    st.session_state.history.append(("Bot", bot_response, time_now))

    # Refresh UI
    st.rerun()