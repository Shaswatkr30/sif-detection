# ==========================================
# SIF PRECURSOR CATEGORIES
# ==========================================

SIF_CATEGORIES = {

    "Hydrocarbon / Gas Leak": [
        "oil leak",
        "oil leakage",
        "gas leak",
        "gas leakage",
        "hydrocarbon leak",
        "oil spill",
        "gas release",
        "hydrocarbon release"
    ],

    "Fire / Explosion": [
        "fire",
        "explosion",
        "flame",
        "spark",
        "ignition",
        "flammable"
    ],

    "Pressure / Process Safety": [
        "high pressure",
        "overpressure",
        "pressurized line",
        "pressure leak",
        "pressure release"
    ],

    "Electrical Hazard": [
        "live wire",
        "energized equipment",
        "electrical shock",
        "electrical hazard",
        "electric shock"
    ],

    "H2S / Toxic Gas": [
        "h2s",
        "toxic gas",
        "gas exposure",
        "h2s exposure",
        "alarm failure"
    ],

    "Confined Space": [
        "confined space",
        "low oxygen",
        "oxygen deficiency"
    ],

    "Isolation / LOTO": [
        "loto",
        "lockout",
        "lockout tagout",
        "failed isolation",
        "isolation failure",
        "energized"
    ],

    "Dropped Object": [
        "dropped object",
        "falling object",
        "object fell"
    ],

    "Working at Height": [
        "fall from height",
        "working at height",
        "height",
        "scaffold",
        "ladder"
    ],

    "Crane / Lifting": [
        "crane",
        "crane overload",
        "lifting",
        "suspended load"
    ],

    "Vehicle / Pedestrian": [
        "vehicle",
        "forklift",
        "pedestrian",
        "unsafe reversing",
        "vehicle reversing"
    ],

    "Equipment Failure": [
        "pump vibration",
        "pump leak",
        "compressor vibration",
        "equipment malfunction",
        "equipment failure",
        "equipment damaged"
    ],

    "Chemical Hazard": [
        "chemical spill",
        "chemical leak",
        "chemical exposure"
    ],

    "Hot Work": [
        "hot work",
        "welding",
        "grinding"
    ],

    "Structural / Containment Failure": [
        "tank rupture",
        "pipeline rupture",
        "pipe rupture",
        "containment failure",
        "esd failure"
    ],

    "Corrosion": [
        "corrosion",
        "corroded pipe",
        "severe corrosion",
        "corroded vessel"
    ],

    "PPE / Procedure": [
        "ppe missing",
        "no ppe",
        "ppe not worn",
        "procedure not followed",
        "unsafe procedure"
    ]
}
# ==========================================
# KEYWORD DETECTION
# ==========================================

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


# ==========================================
# RISK CALCULATION
# ==========================================

def calculate_risk(detected, text=""):

    text = text.lower().strip()

    # ======================================
    # INVALID INPUT
    # ======================================

    safety_words = [
        "oil", "gas", "hydrocarbon", "pipeline",
        "tank", "pump", "compressor", "valve",
        "pressure", "leak", "leakage", "spill",
        "fire", "explosion", "electrical",
        "electric", "machine", "scaffold",
        "ladder", "height", "confined space",
        "h2s", "chemical", "ppe", "worker",
        "maintenance", "inspection", "permit",
        "loto", "lockout", "crane", "forklift",
        "vehicle", "hazard", "safety",
        "accident", "incident", "injury",
        "corrosion", "flame", "spark",
        "welding"
    ]

    # Random/unnecessary input
    if not any(word in text for word in safety_words):
        return "INVALID"


    # ======================================
    # HIGH RISK
    # ======================================

    high_conditions = [

        # Oil + ignition
        (
            "oil leak" in text
            and any(x in text for x in
                    ["spark", "flame", "ignition", "hot work"])
        ),

        # Gas + ignition
        (
            "gas leak" in text
            and any(x in text for x in
                    ["fire", "spark", "ignition", "flame"])
        ),

        # Hydrocarbon + ignition
        (
            "hydrocarbon leak" in text
            and any(x in text for x in
                    ["fire", "spark", "ignition", "flame"])
        ),

        # Fire / explosion
        (
            "fire" in text
            and "explosion" in text
        ),

        # Pressure
        (
            "high pressure" in text
            and "leak" in text
        ),

        (
            "pressurized line" in text
            and "leak" in text
        ),

        "overpressure" in text,

        # Electrical
        "live wire" in text,
        "energized equipment" in text,
        "electrical shock" in text,

        # H2S
        (
            "h2s" in text
            and any(x in text for x in
                    ["exposure", "alarm failure",
                     "alarm not working"])
        ),

        # Confined space
        (
            "confined space" in text
            and any(x in text for x in
                    ["h2s", "low oxygen",
                     "oxygen deficiency"])
        ),

        # Isolation
        (
            "loto" in text
            and "energized" in text
        ),

        (
            "lockout" in text
            and "energized" in text
        ),

        "failed isolation" in text,
        "isolation failure" in text,

        # Dropped object
        (
            "dropped object" in text
            and "worker" in text
        ),

        (
            "falling object" in text
            and "worker" in text
        ),

        # Crane
        (
            "crane" in text
            and "overload" in text
        ),

        (
            "crane" in text
            and "worker" in text
        ),

        # Vehicle / pedestrian
        (
            "vehicle" in text
            and "pedestrian" in text
        ),

        (
            "forklift" in text
            and "pedestrian" in text
        ),

        # Major failure
        "tank rupture" in text,
        "pipeline rupture" in text,
        "pipe rupture" in text,
        "containment failure" in text,
        "esd failure" in text,

        # Hot work
        (
            "hot work" in text
            and "hydrocarbon" in text
        ),

        (
            "welding" in text
            and "flammable" in text
        ),

        (
            "grinding" in text
            and "flammable" in text
        )
    ]

    if any(high_conditions):
        return "HIGH"


    # ======================================
    # MEDIUM RISK
    # ======================================

    medium_conditions = [

        # Leak / spill
        "oil leak" in text,
        "oil leakage" in text,
        "oil spill" in text,
        "gas leakage" in text,
        "minor gas leak" in text,
        "chemical spill" in text,

        # Equipment
        "pump vibration" in text,
        "pump leak" in text,
        "compressor vibration" in text,
        "equipment malfunction" in text,
        "equipment failure" in text,
        "equipment damaged" in text,

        # Maintenance
        "maintenance overdue" in text,
        "maintenance missing" in text,

        # Inspection
        "inspection overdue" in text,
        "inspection missing" in text,

        # PPE
        "ppe missing" in text,
        "no ppe" in text,
        "ppe not worn" in text,

        # Permit
        "permit missing" in text,
        "no work permit" in text,
        "expired permit" in text,

        # Procedure
        "procedure not followed" in text,
        "unsafe procedure" in text,

        # Vehicle
        "unsafe reversing" in text,
        "vehicle reversing" in text,

        # Scaffold
        "damaged scaffold" in text,
        "incomplete scaffold" in text,

        # Ladder
        "unsafe ladder" in text,
        "damaged ladder" in text,

        # Corrosion
        "corroded pipe" in text,
        "severe corrosion" in text,
        "corroded vessel" in text,

        # Valve / flange / gasket
        "valve leak" in text,
        "flange leak" in text,
        "gasket leak" in text,

        # Housekeeping
        "oil on floor" in text,
        "slippery floor" in text,
        "blocked walkway" in text
    ]

    if any(medium_conditions):
        return "MEDIUM"


    # ======================================
    # LOW RISK
    # ======================================

    low_conditions = [

        "routine inspection",
        "safety observation",
        "minor housekeeping",
        "clean work area",
        "proper ppe",
        "ppe worn",
        "safe condition",
        "no hazard",
        "no issue",
        "normal operation",
        "routine maintenance",
        "safety meeting",
        "safety training",
        "toolbox talk",
        "hazard controlled",
        "hazard removed"
    ]

    if any(word in text for word in low_conditions):
        return "LOW"


    # Safety-related report but no serious condition
    return "LOW"