def get_confidence_level(score):
    
    if score >= 0.80:

        return "HIGH"

    elif score >= 0.50:

        return "MEDIUM"

    return "LOW"