SIF_CATEGORIES = {
    "Fall from Height": [
        "fall",
        "fell",
        "ladder",
        "scaffold",
        "height",
        "roof",
        "platform",
        "unsecured ladder"
    ],

    "Machine Guarding": [
        "unguarded",
        "guard missing",
        "machine guard",
        "guarding",
        "moving parts",
        "exposed machine"
    ],

    "Electrical Hazard": [
        "electrical",
        "electric shock",
        "exposed wire",
        "live wire",
        "cable",
        "voltage",
        "energized"
    ],

    "Vehicle / Mobile Equipment": [
        "vehicle",
        "truck",
        "forklift",
        "crane",
        "mobile equipment",
        "reversing",
        "backing"
    ],

    "Fire / Explosion": [
        "fire",
        "explosion",
        "flammable",
        "ignition",
        "spark",
        "gas leak"
    ],

    "Confined Space": [
        "confined space",
        "tank",
        "vessel",
        "manhole",
        "oxygen",
        "toxic gas"
    ],

    "Dropped Object": [
        "dropped object",
        "falling object",
        "object fell",
        "overhead",
        "load fell"
    ]
}


def detect_keywords(text):

    text = text.lower()

    detected = []

    for category, keywords in SIF_CATEGORIES.items():

        found_keywords = []

        for keyword in keywords:

            if keyword in text:
                found_keywords.append(keyword)

        if found_keywords:

            detected.append({
                "category": category,
                "keywords": found_keywords
            })

    return detected


def calculate_risk(detected):

    if not detected:
        return "LOW"

    number_of_categories = len(detected)

    if number_of_categories >= 2:
        return "HIGH"

    return "MEDIUM"