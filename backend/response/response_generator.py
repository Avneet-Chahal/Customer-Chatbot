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
# PREPROCESS
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
# GENERATE RESPONSE
# =========================

def generate_response(

    user_text,

    intent,

    confidence,

    emotion
):

    # =========================
    # UNKNOWN
    # =========================

    if intent == "unknown":

        return (
            "I'm sorry, I could not "
            "understand your request."
        )

    processed = preprocess_text(
        user_text
    )

    user_vector = vectorizer.transform(
        [processed]
    )

    similarities = cosine_similarity(

        user_vector,
        X
    )

    best_index = similarities.argmax()

    response = dataset.iloc[
        best_index
    ]["bot_response"]

    # =========================
    # EMOTION HANDLING
    # =========================

    if emotion == "angry":

        response = (
            "I understand your frustration. "
            + response
        )

    return response