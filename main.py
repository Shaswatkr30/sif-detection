from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models

from database import engine, get_db
from schemas import ReportCreate

from nlp_model import analyze_text

from classifier import (
    detect_keywords,
    calculate_risk
)

from recommendation import get_recommendation

from text_preprocessor import normalize_text
from fastapi.staticfiles import StaticFiles

# Create database tables
models.Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="SIF Precursor Detection API",
    description="AI based safety report analysis system",
    version="1.0"
)


# --------------------------------
# HOME
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "SIF Precursor Detection API is running"
    }


# --------------------------------
# HEALTH
# --------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------
# ANALYZE REPORT
# --------------------------------

@app.post("/analyze")
def analyze_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):

    original_text = report.report_text.strip()

    if not original_text:

        raise HTTPException(
            status_code=400,
            detail="Report text cannot be empty"
        )


    # -----------------------------
    # Text preprocessing
    # -----------------------------

    processed_text = normalize_text(
        original_text
    )


    # -----------------------------
    # AI analysis
    # -----------------------------

    ai_result = analyze_text(
        processed_text
    )


    # -----------------------------
    # Keyword detection
    # -----------------------------

    keyword_result = detect_keywords(
        processed_text
    )


    detected_precursors = []


    for item in keyword_result:

        detected_precursors.append({

            "precursor": item["category"],

            "keywords": item["keywords"]

        })


    # -----------------------------
    # Risk calculation
    # -----------------------------

    risk_level = calculate_risk(
        detected_precursors
    )


    # -----------------------------
    # Primary precursor
    # -----------------------------

    if detected_precursors:

        primary_precursor = (
            detected_precursors[0]["precursor"]
        )

    else:

        primary_precursor = (
            "No significant safety precursor"
        )


    # -----------------------------
    # Recommendation
    # -----------------------------

    recommendation = get_recommendation(
        primary_precursor
    )


    # -----------------------------
    # Database save
    # -----------------------------

    new_report = models.Report(

        report_text=original_text,

        risk_level=risk_level,

        primary_precursor=primary_precursor,

        confidence="N/A"
    )


    db.add(new_report)

    db.commit()

    db.refresh(new_report)


    # -----------------------------
    # Response
    # -----------------------------

    return {

        "report_id": new_report.id,

        "original_text": original_text,

        "processed_text": processed_text,

        "risk_level": risk_level,

        "primary_precursor": primary_precursor,

        "detected_precursors": detected_precursors,

        "recommendation": recommendation,

        "ai_result": ai_result
    }


# --------------------------------
# GET ALL REPORTS
# --------------------------------

@app.get("/reports")
def get_reports(
    db: Session = Depends(get_db)
):

    reports = (
        db.query(models.Report)
        .order_by(models.Report.id.desc())
        .all()
    )

    return reports


# --------------------------------
# GET SINGLE REPORT
# --------------------------------

@app.get("/reports/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = (
        db.query(models.Report)
        .filter(models.Report.id == report_id)
        .first()
    )


    if not report:

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )


    return report


# --------------------------------
# DELETE REPORT
# --------------------------------

@app.delete("/reports/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = (
        db.query(models.Report)
        .filter(models.Report.id == report_id)
        .first()
    )


    if not report:

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )


    db.delete(report)

    db.commit()


    return {
        "message": "Report deleted successfully"
    }


# --------------------------------
# SEARCH REPORTS
# --------------------------------

@app.get("/reports/search")
def search_reports(
    keyword: str,
    db: Session = Depends(get_db)
):

    reports = (
        db.query(models.Report)
        .filter(
            models.Report.report_text.contains(keyword)
        )
        .all()
    )

    return reports


# --------------------------------
# DASHBOARD STATS
# --------------------------------

@app.get("/dashboard/stats")
def dashboard_stats(
    db: Session = Depends(get_db)
):

    reports = (
        db.query(models.Report)
        .all()
    )


    total_reports = len(reports)

    high_risk = 0

    medium_risk = 0

    low_risk = 0


    for report in reports:

        if report.risk_level == "HIGH":

            high_risk += 1

        elif report.risk_level == "MEDIUM":

            medium_risk += 1

        elif report.risk_level == "LOW":

            low_risk += 1


    return {

        "total_reports": total_reports,

        "high_risk": high_risk,

        "medium_risk": medium_risk,

        "low_risk": low_risk
    }


# --------------------------------
# HIGH RISK REPORTS
# --------------------------------

@app.get("/dashboard/high-risk")
def high_risk_reports(
    db: Session = Depends(get_db)
):

    reports = (
        db.query(models.Report)
        .filter(
            models.Report.risk_level == "HIGH"
        )
        .order_by(
            models.Report.id.desc()
        )
        .all()
    )

    return reports


# --------------------------------
# RECENT REPORTS
# --------------------------------

@app.get("/dashboard/recent-reports")
def recent_reports(
    db: Session = Depends(get_db)
):

    reports = (
        db.query(models.Report)
        .order_by(
            models.Report.id.desc()
        )
        .limit(10)
        .all()
    )

    return reports


# --------------------------------
# PRECURSOR STATISTICS
# --------------------------------

@app.get("/dashboard/precursors")
def precursor_stats(
    db: Session = Depends(get_db)
):

    reports = (
        db.query(models.Report)
        .all()
    )


    result = {}


    for report in reports:

        precursor = (
            report.primary_precursor
        )


        if precursor not in result:

            result[precursor] = 0


        result[precursor] += 1


    return result

app.mount(
    "/dashboard",
    StaticFiles(directory="frontend", html=True),
    name="dashboard"
)