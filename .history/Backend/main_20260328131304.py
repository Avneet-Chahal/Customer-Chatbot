import joblib

# Load model
model = joblib.load("../Models/intent_model.pkl")
vectorizer = joblib.load("../Models/vectorizer.pkl")

def predict_intent(text):
    text = text.lower()
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

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye", "stop"]:
        break

    intent, confidence = predict_intent(user_input)

    print("Intent:", intent)
    print("Confidence:", round(confidence, 2))

    if confidence > 0.50:
        print("Bot:", responses.get(intent))
    elif confidence > 0.25:
        print("Bot: I think you're asking about", intent.replace("_", " "))
    else:
        print("Bot: I'm not sure. Can you rephrase?")

    print("-" * 40)