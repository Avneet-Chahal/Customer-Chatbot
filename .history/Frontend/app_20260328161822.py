import streamlit as st
import joblib
import datetime
import os
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
    if os.path.exists(os.path.join(BASE_DIR, "chat_history.json")):
        os.remove(os.path.join(BASE_DIR, "chat_history.json"))
    st.success("Chat cleared!")

# ---------------- WELCOME ----------------
if not st.session_state.history:
    st.info("👋 Welcome! Ask me anything about orders, refunds, or issues.")
    st.write("💡 Try:")
    st.write("- Track my order")
    st.write("- Refund my money")
    st.write("- My delivery is late")

# ---------------- DISPLAY CHAT ----------------
for sender, message, time in st.session_state.history:
    if sender == "You":
        with st.chat_message("user"):
            st.write(message)
            st.caption(time)
    else:
        with st.chat_message("assistant"):
            st.write(message)
            st.caption(time)

# ---------------- CHAT INPUT (BOTTOM) ----------------
user_input = st.chat_input("Type your message...")

# ---------------- MAIN LOGIC ----------------
if user_input:
    
    time = datetime.datetime.now().strftime("%H:%M")

    # Show user message
    st.session_state.history.append(("You", user_input, time))

    # Load memory
    history = load_history()

    # Recommendation system
    matched_response, score = get_best_match(user_input, history)

    # Decision logic
    if score > 0.7:
        bot_response = matched_response

    elif score > 0.4:
        bot_response = f"I think this might help: {matched_response}"

    else:
        # 🔥 STOP / EXIT HANDLING (ADD HERE)
        if user_input.lower() in ["stop", "exit", "quit"]:
            bot_response = "👋 Chat ended. Feel free to start a new conversation!"

        # Special cases
        elif user_input.lower() in ["issue", "problem", "help"]:
            bot_response = "👋 Chat ended. Feel free to start a new conversation!"

        elif "refund" in user_input and "late" in user_input:
            bot_response = "🤖 I see your order is delayed and you want a refund. Let me help you with that."

        else:
            with st.spinner("Bot is typing..."):
                intent = predict_intent(user_input)
                bot_response = responses.get(
                    intent,
                    "🤖 I'm not sure I understood. Could you please rephrase?"
                )
                
                
    # Save memory
    save_message(user_input, bot_response)

    # Save bot response
    st.session_state.history.append(("Bot", bot_response, time))

    # Rerun to update UI instantly
    st.rerun()