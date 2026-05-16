import streamlit as st

# =========================
# IMPORT ENGINES
# =========================

from backend.ml.intent_engine import (
    predict_intent
)

from backend.ml.emotion_engine import (
    detect_emotion
)

from backend.confidence.confidence_engine import (
    get_confidence_level
)

from backend.response.response_generator import (
    generate_response
)

from backend.failure.failure_detector import (
    detect_failure
)

# =========================
# DATABASE
# =========================

from backend.database.chat_db import (
    save_chat
)

from backend.database.failure_db import (
    save_failure
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(

    page_title=(
        "AI Customer Support Chatbot"
    ),

    page_icon="🤖",

    layout="centered"
)

# =========================
# TITLE
# =========================

st.title(
    "🤖 Self-Improving AI Customer Support Chatbot"
)

st.markdown("""
Welcome to the intelligent customer support assistant.
""")

# =========================
# SESSION STATE
# =========================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# =========================
# USER INPUT
# =========================

user_input = st.text_input(
    "Enter your message"
)

# =========================
# SEND BUTTON
# =========================

if st.button("Send"):

    if user_input.strip() == "":

        st.warning(
            "Please enter a message."
        )

    else:

        # =========================
        # INTENT DETECTION
        # =========================

        intent, probability = (
            predict_intent(user_input)
        )

        # =========================
        # EMOTION DETECTION
        # =========================

        emotion = detect_emotion(
            user_input
        )

        # =========================
        # CONFIDENCE LEVEL
        # =========================

        confidence = (
            get_confidence_level(
                probability
            )
        )

        # =========================
        # RESPONSE GENERATION
        # =========================

        response = generate_response(
            
            user_input,

            intent,

            confidence,

            emotion
        )

        # =========================
        # FAILURE DETECTION
        # =========================

        failed = detect_failure(

            confidence,

            emotion
        )

        # =========================
        # SAVE CHAT
        # =========================

        save_chat(

            username="guest",

            user_message=user_input,

            bot_response=response,

            intent=intent,

            emotion=emotion,

            confidence=confidence
        )

        # =========================
        # SAVE FAILED CHAT
        # =========================

        if failed:

            save_failure(

                username="guest",

                user_message=user_input,

                bot_response=response,

                reason=(
                    "Low confidence or negative emotion"
                )
            )

        # =========================
        # STORE HISTORY
        # =========================

        st.session_state.chat_history.append({

            "user": user_input,

            "bot": response,

            "intent": intent,

            "emotion": emotion,

            "confidence": confidence
        })

# =========================
# CLEAR CHAT BUTTON
# =========================

if st.sidebar.button(
    "🗑 Clear Conversation"
):

    st.session_state.chat_history = []

    st.rerun()

# =========================
# CHAT COUNT
# =========================

st.sidebar.markdown(

    f"### Chats: "

    f"{len(st.session_state.chat_history)}"
)

# =========================
# DISPLAY CHAT
# =========================

st.subheader("💬 Conversation")

for index, chat in enumerate(

    reversed(
        st.session_state.chat_history
    )
):

    # USER MESSAGE

    st.markdown(f"""
    <div style='
        background-color:#DCF8C6;
        padding:10px;
        border-radius:10px;
        margin-bottom:10px;
    '>

    <b>You:</b> {chat['user']}

    </div>
    """, unsafe_allow_html=True)

    # BOT MESSAGE

    st.markdown(f"""
    <div style='
        background-color:#F1F0F0;
        padding:10px;
        border-radius:10px;
        margin-bottom:20px;
    '>

    <b>Bot:</b> {chat['bot']}

    <br><br>

    <b>Intent:</b> {chat['intent']}

    <br>

    <b>Emotion:</b> {chat['emotion']}

    <br>

    <b>Confidence:</b> {chat['confidence']}

    </div>
    """, unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

st.sidebar.title(
    "📊 System Status"
)

st.sidebar.success(
    "Chatbot Running"
)

st.sidebar.markdown("""

### Features

✅ Intent Detection  
✅ Emotion Detection  
✅ Confidence Engine  
✅ Failure Detection  
✅ SQLite Database  
✅ Chat Logging  
✅ Self-Improving Architecture  
""")