from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_best_match(user_input, history):
    if not history:
        return None, 0

    texts = [item["user"] for item in history]
    texts.append(user_input)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(vectors[-1], vectors[:-1])
    
    best_index = similarity.argmax()
    best_score = similarity[0][best_index]

    if best_score > 0.5:
        return history[best_index]["bot"], best_score
    
    return None, best_score
