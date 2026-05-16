import pandas as pd
import pickle

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.linear_model import (
    LogisticRegression
)

from backend.ml.preprocessing import preprocess_text
from backend.paths import data_path

# =========================
# LOAD DATASET
# =========================

intent_df = pd.read_csv(data_path("intent_dataset.csv"))

# =========================
# CLEAN COLUMN NAMES
# =========================

intent_df.columns = [

    col.lower().strip()

    for col in intent_df.columns
]

# =========================
# CLEAN LABELS
# =========================

intent_df["intent_label"] = (

    intent_df["intent_label"]

    .astype(str)

    .str.lower()

    .str.strip()
)

# =========================
# PREPROCESS TEXT
# =========================

intent_df["processed"] = (

    intent_df["text"]

    .apply(preprocess_text)
)

# =========================
# FEATURES
# =========================

X = intent_df["processed"]

# =========================
# LABELS
# =========================

y = intent_df["intent_label"]

# =========================
# TF-IDF
# =========================

vectorizer = TfidfVectorizer(

    ngram_range=(1, 2),

    max_features=5000
)

X_vectorized = (
    vectorizer.fit_transform(X)
)

# =========================
# MODEL
# =========================

model = LogisticRegression(
    max_iter=1000
)

model.fit(X_vectorized, y)

# =========================
# SAVE MODEL
# =========================

pickle.dump(

    model,

    open(
        "models/intent_model.pkl",
        "wb"
    )
)

pickle.dump(

    vectorizer,

    open(
        "models/vectorizer.pkl",
        "wb"
    )
)

print(
    "Intent model trained successfully"
)