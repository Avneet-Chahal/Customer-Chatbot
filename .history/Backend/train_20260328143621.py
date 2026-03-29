import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv("../Data/intent_dataset.csv")

X = data["text"]
y = data["intent_label"]

# Vectorization
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=7000)
X_vec = vectorizer.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42, stratify=y
)

# Train
model = LogisticRegression(max_iter=3000, multi_class="ovr")
model.fit(X_train, y_train)

# Save
joblib.dump(model, "../Models/intent_model.pkl")
joblib.dump(vectorizer, "../Models/vectorizer.pkl")

print("✅ Model trained & saved!")