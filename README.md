# 🤖 Self-Improving AI Customer Support Chatbot

An intelligent AI-powered customer support chatbot built using Python, Streamlit, Natural Language Processing (NLP), and SQLite. The chatbot can understand customer queries, detect emotions, generate context-aware responses, log conversations, and support self-improving architecture through failure tracking and analytics.

---

# 📌 Features

✅ Intent Detection  
✅ Emotion Detection  
✅ Dataset-Driven Response Generation  
✅ TF-IDF + Cosine Similarity Matching  
✅ SQLite Database Integration  
✅ Conversation History  
✅ Failed Conversation Logging  
✅ Confidence Engine  
✅ Self-Improving Architecture  
✅ Streamlit Frontend Interface  
✅ Modular Backend Structure  

---

# 🧠 Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Scikit-learn
- NLTK
- TextBlob
- TF-IDF Vectorization
- Cosine Similarity

---

# 📂 Project Structure

```bash
Customer Chatbot/
│
├── app.py
│
├── backend/
│   ├── analytics/
│   ├── confidence/
│   ├── database/
│   ├── failure/
│   ├── ml/
│   ├── response/
│
├── data/
│   ├── chatbot.db
│   ├── conversation_logs.csv
│   ├── emotion_dataset.csv
│   ├── failed_conversations.csv
│   ├── intent_dataset.csv
│
├── Diagrams/
│
├── Docs/
│
├── requirements.txt
│
├── README.md
│
└── screenshot.png
```

---

# ⚙️ System Workflow

```text
User Message
      ↓
Text Preprocessing
      ↓
TF-IDF Similarity Search
      ↓
Intent Detection
      ↓
Emotion Detection
      ↓
Response Generation
      ↓
Confidence Evaluation
      ↓
SQLite Chat Logging
      ↓
Failure Detection
      ↓
Conversation History
```

---

# 📊 Datasets Used

## 1. Intent Dataset
Contains customer queries and their corresponding intents.

Example:
- order_status
- refund_request
- payment_issue
- greeting
- goodbye

---

## 2. Emotion Dataset
Used for emotion analysis and sentiment understanding.

Supported emotions:
- happy
- neutral
- confused
- angry

---

## 3. Conversation Logs Dataset
Contains sample customer support conversations used for response generation.

---

# 🗄️ Database Tables

## chat_history
Stores:
- user messages
- bot responses
- detected intents
- emotions
- confidence scores

## failed_conversations
Stores:
- low-confidence conversations
- unresolved queries
- negative customer interactions

## users
Stores user account information.

---

# 🚀 Installation and Setup

## 1. Clone Repository

```bash
git clone <your-github-repo-link>
```

---

## 2. Open Project Folder

```bash
cd "Customer Chatbot"
```

---

## 3. Create Virtual Environment

```bash
python -m venv .venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
.venv\\Scripts\\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## 5. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 6. Initialize Database

```bash
python -m backend.database.init_db
```

---

## 7. Run Streamlit Application

```bash
streamlit run app.py
```

---

# 🧪 Sample Test Inputs

```text
Where is my order?
```

```text
Track my package
```

```text
I want refund for my order
```

```text
Payment failed during checkout
```

```text
This service is terrible
```

---

# 📈 Future Improvements

- Voice chatbot support
- Real-time analytics dashboard
- Automatic retraining system
- Multi-language support
- User authentication system
- Deep learning NLP models
- API deployment

---

# 📷 Project Screenshot

```
<img width="1917" height="967" alt="image" src="https://github.com/user-attachments/assets/380574b6-604f-4e88-9163-2bd8c57b80f7" />
<img width="1917" height="973" alt="image" src="https://github.com/user-attachments/assets/ae9641a0-7412-45d7-8194-a128e0bd3280" />
<img width="1918" height="963" alt="image" src="https://github.com/user-attachments/assets/0f32a811-509e-469e-902c-d03c7b3021ca" />
<img width="1918" height="965" alt="image" src="https://github.com/user-attachments/assets/deb635ae-654e-4938-83b1-0d3a5afcf5ea" />




```

## 🚀 Live Deployment

You can access the deployed Customer Support Chatbot here:

🔗 [Live Demo](https://customer-chatbot-1-zug4.onrender.com/)

---



# 📚 Learning Outcomes

Through this project, the following concepts were explored:

- Natural Language Processing
- Machine Learning
- Sentiment Analysis
- TF-IDF Similarity
- SQLite Database Management
- Streamlit Frontend Development
- Modular Backend Architecture
- AI-based Customer Support Systems

---

# 👨‍💻 Author

Avneet Chahal

---

# 📄 License

This project is developed for educational and academic purposes.
