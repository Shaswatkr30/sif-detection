RECOMMENDATIONS = {

    "Fall from Height":
        "Stop the activity and secure the ladder, scaffold, "
        "or working platform before work resumes.",

    "Electrical Hazard":
        "Stop the work, isolate the electrical source, "
        "and have the equipment checked by a qualified person.",

    "Machine Guarding":
        "Stop the machine and restore the required guarding "
        "before operation continues.",

    "Vehicle / Mobile Equipment":
        "Stop the unsafe movement and establish a safe "
        "separation between people and mobile equipment.",

    "Fire / Explosion":
        "Stop the activity and control ignition and "
        "flammable-material hazards before work resumes.",

    "Confined Space":
        "Stop entry until the confined-space hazards, "
        "atmosphere, and required controls are verified.",

    "Dropped Object":
        "Stop the activity and establish a controlled area "
        "to prevent exposure to falling objects."
}


def get_recommendation(precursor):

    return RECOMMENDATIONS.get(
        precursor,
        "Conduct a safety review and apply appropriate "
        "controls before continuing the activity."
    )