def detect_failure(

    confidence,

    emotion
):

    if confidence == "LOW":

        return True

    if emotion == "angry":

        return True

    return False