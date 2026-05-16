from textblob import TextBlob

def detect_emotion(text):

    polarity = (

        TextBlob(text)

        .sentiment

        .polarity
    )

    if polarity < -0.3:

        return "angry"

    elif polarity < 0:

        return "confused"

    elif polarity > 0.3:

        return "happy"

    return "neutral"