from transformers import pipeline


classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)


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

    "no significant safety precursor"
]


def analyze_text(text: str):

    result = classifier(
        text,
        candidate_labels=SIF_PRECURSORS,
        multi_label=True
    )

    detected = []

    for label, score in zip(
        result["labels"],
        result["scores"]
    ):

        if score >= 0.50:

            detected.append({
                "precursor": label,
                "confidence": round(
                    float(score),
                    3
                )
            })

    return detected