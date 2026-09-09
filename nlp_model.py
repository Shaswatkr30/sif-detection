from transformers import pipeline


classifier = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/MiniLM-L6-mnli"
)


import re

SIF_PRECURSORS = [
    "slip or trip hazard",
    "fall from height",
    "machine guarding failure",
    "electrical hazard",
    "vehicle or mobile equipment hazard",
    "fire or explosion hazard",
    "confined space hazard",
    "chemical exposure",
    "dropped object hazard",
    "unsafe lifting operation",
    "lockout tagout failure",
    "personal protective equipment failure",
]

KEYWORDS = {
    "slip or trip hazard": [
        "slip", "trip", "wet floor", "spilled", "spill",
        "uneven floor", "obstruction"
    ],
    "fall from height": [
        "fall from height", "working at height", "ladder",
        "scaffold", "roof", "elevated"
    ],
    "machine guarding failure": [
        "machine guard", "unguarded", "guard missing",
        "machine guarding"
    ],
    "electrical hazard": [
        "electric shock", "electrical", "exposed wire",
        "live wire", "short circuit"
    ],
    "vehicle or mobile equipment hazard": [
        "forklift", "vehicle", "truck", "mobile equipment",
        "reversing vehicle"
    ],
    "fire or explosion hazard": [
        "fire", "explosion", "flammable", "ignition",
        "hot work"
    ],
    "confined space hazard": [
        "confined space", "tank entry", "manhole"
    ],
    "chemical exposure": [
        "chemical", "toxic", "acid", "solvent", "gas leak"
    ],
    "dropped object hazard": [
        "dropped object", "falling object", "falling material"
    ],
    "unsafe lifting operation": [
        "lifting", "crane", "hoist", "suspended load"
    ],
    "lockout tagout failure": [
        "lockout", "tagout", "loto", "isolation failure"
    ],
    "personal protective equipment failure": [
        "no helmet", "no gloves", "no safety shoes",
        "ppe", "without ppe"
    ],
}


def analyze_text(text: str):
    """
    Lightweight safety analysis.
    Does NOT use Hugging Face or any large ML model.
    """

    if not text:
        return {
            "labels": [],
            "scores": [],
            "top_label": "no significant safety precursor",
            "risk_level": "low",
        }

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    matches = []

    for label, keywords in KEYWORDS.items():
        found = []

        for keyword in keywords:
            if keyword in text:
                found.append(keyword)

        if found:
            score = min(0.99, 0.70 + (len(found) - 1) * 0.10)

            matches.append({
                "label": label,
                "score": round(score, 2),
                "keywords": found,
            })

    matches.sort(key=lambda x: x["score"], reverse=True)

    if not matches:
        return {
            "labels": ["no significant safety precursor"],
            "scores": [0.50],
            "top_label": "no significant safety precursor",
            "risk_level": "low",
        }

    return {
        "labels": [x["label"] for x in matches],
        "scores": [x["score"] for x in matches],
        "top_label": matches[0]["label"],
        "risk_level": "high" if matches[0]["score"] >= 0.80 else "medium",
        "matches": matches,
    }