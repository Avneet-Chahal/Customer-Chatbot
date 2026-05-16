import pandas as pd

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from backend.ml.preprocessing import preprocess_text
from backend.paths import data_path

# =========================
# LOAD DATASET
# =========================

dataset = pd.read_csv(data_path("conversation_logs.csv"))

# =========================
# CLEAN COLUMNS
# =========================

dataset.columns = [

    col.lower().strip()

    for col in dataset.columns
]

# =========================
# PREPROCESS TEXT
# =========================

dataset["processed"] = (

    dataset["user_message"]

    .apply(preprocess_text)
)

# =========================
# TF-IDF
# =========================

vectorizer = TfidfVectorizer(

    ngram_range=(1, 2),

    max_features=5000
)

X = vectorizer.fit_transform(
    dataset["processed"]
)

# =========================
# PREDICT INTENT
# =========================

def predict_intent(user_text):

    processed = preprocess_text(
        user_text
    )

    if processed.strip() == "":

        return "unknown", 0.0

    user_vector = vectorizer.transform(
        [processed]
    )

    similarities = cosine_similarity(

        user_vector,
        X
    )

    best_index = similarities.argmax()

    best_score = similarities[0][best_index]

    # =========================
    # LOW CONFIDENCE
    # =========================

    if best_score < 0.30:

        return "unknown", best_score

    detected_intent = dataset.iloc[
        best_index
    ]["detected_intent"]

    return (
        detected_intent.lower(),
        best_score
    )