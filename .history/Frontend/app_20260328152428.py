import streamlit as st
import joblib
import datetime

# ---------------- LOAD MODEL ----------------
model = joblib.load("../Models/intent_model.pkl")
vectorizer = joblib.load("../Models/vectorizer.pkl")

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

# ---------------- WELCOME MESSAGE ----------------
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

# ---------------- PROCESS INPUT ----------------
if user_input:
    time = datetime.datetime.now().strftime("%H:%M")

    # Save user message
    st.session_state.history.append(("You", user_input, time))

    # Clear input immediately
    st.session_state.input = ""

    # Handle vague inputs
    if user_input.lower() in ["issue", "problem", "help"]:
        bot_response = "🤖 Could you please describe your issue in more detail?"

    # Smart combined query
    elif "refund" in user_input and "late" in user_input:
        bot_response = "🤖 I see your order is delayed and you want a refund. Let me help you with that."

    else:
        with st.spinner("Bot is typing..."):
            intent = predict_intent(user_input)
            bot_response = responses.get(intent, "🤖 I'm not sure I understood. Could you please rephrase?")

    # Save bot response
    st.session_state.history.append(("Bot", bot_response, time))

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

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("<p style='text-align:center;'>🚀 Built by Avneet | AI Customer Chatbot</p>", unsafe_allow_html=True)