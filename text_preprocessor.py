import re


JARGON_MAP = {

    "loto": "lockout tagout",
    "lock out tag out": "lockout tagout",

    "ppe": "personal protective equipment",

    "scaff": "scaffold",
    "scaffolding": "scaffold",

    "elec": "electrical",

    "fork lift": "forklift",

    "energised": "energized",

    "unauthorised": "unauthorized",

    "work at height": "height work",

    "confined-space": "confined space"
}


def normalize_text(text: str):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    for old_word, new_word in JARGON_MAP.items():

        text = text.replace(
            old_word,
            new_word
        )

    return text
