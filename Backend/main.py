import joblib

# Load model
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

print("\nChatbot Ready! Type 'exit' to stop.\n")

# Generic vague inputs
generic_words = ["issue", "problem", "help", "error", "something wrong"]

while True:
    user_input = input("You: ").strip()

    # Exit condition
    if user_input.lower() in ["exit", "quit", "bye", "stop"]:
        print("Chatbot stopped.")
        break

    # Handle vague inputs
    if user_input.lower() in generic_words:
        print("Bot: Could you please describe your issue in more detail?")
        print("-" * 40)
        continue

    # Predict intent
    intent, confidence = predict_intent(user_input)

    print("Intent:", intent)
    print("Confidence:", round(confidence, 2))

    # Response logic
    if confidence > 0.35:
        print("Bot:", responses.get(intent, "Let me help you with that."))
    elif confidence > 0.15:
        print("Bot:", responses.get(intent, "Let me help you with that."))
    else:
        print("Bot: I'm not sure I understood. Could you please rephrase?")

    print("-" * 40)