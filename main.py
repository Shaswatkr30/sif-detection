
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models

from database import engine, get_db
from schemas import ReportCreate

from nlp_model import analyze_text
from classifier import detect_keywords, calculate_risk
from recommendation import get_recommendation
from text_preprocessor import normalize_text

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path


# =========================
# APP SETUP
# =========================

BASE_DIR = Path(__file__).resolve().parent

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# =========================
# FRONTEND
# =========================

@app.get("/")
def serve_frontend():
    return FileResponse(BASE_DIR / "frontend" / "index.html")

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "healthy"}
# --------------------------------
# ANALYZE REPORT
# --------------------------------




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


@app.post("/analyze")
def analyze_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):

    # ======================================
    # 1. ORIGINAL INPUT
    # ======================================

    original_text = report.report_text.strip()

    if not original_text:
        raise HTTPException(
            status_code=400,
            detail="Report text cannot be empty"
        )


    # ======================================
    # 2. TEXT PREPROCESSING
    # ======================================

    processed_text = normalize_text(original_text)


    # ======================================
    # 3. AI ANALYSIS
    # ======================================

    ai_result = analyze_text(processed_text)


    # ======================================
    # 4. KEYWORD DETECTION
    # ======================================

    keyword_result = detect_keywords(processed_text)

    detected_precursors = []

    for item in keyword_result:

        detected_precursors.append({
            "precursor": item["category"],
            "keywords": item["keywords"]
        })


    # ======================================
    # 5. RISK CALCULATION
    # ======================================

    risk_level = calculate_risk(
        detected_precursors,
        processed_text
    )


    # ======================================
    # 6. INVALID INPUT
    # ======================================

    if risk_level == "INVALID":

        return {
            "status": "invalid",
            "message": "Please enter a valid oil & gas safety report.",
            "risk_level": "INVALID",
            "primary_precursor": "Not applicable",
            "detected_precursors": [],
            "recommendation": (
                "Enter a valid oil & gas safety "
                "incident, hazard, or observation."
            )
        }


    # ======================================
    # 7. PRIMARY PRECURSOR
    # ======================================

    if detected_precursors:

        primary_precursor = (
            detected_precursors[0]["precursor"]
        )

    else:

        primary_precursor = (
            "No significant safety precursor"
        )


    # ======================================
    # 8. RECOMMENDATION
    # ======================================

    recommendation = get_recommendation(
        primary_precursor
    )

# ======================================
    # 9. SAVE TO DATABASE
    # ======================================

    new_report = models.Report(
        report_text=original_text,
        risk_level=risk_level,
        primary_precursor=primary_precursor,
        confidence="N/A"
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    # ======================================
    # MANAGER ALERT FOR HIGH RISK
    # ======================================

    if risk_level == "HIGH":

        alert = models.ManagerAlert(
            report_id=new_report.id,
            risk_level="HIGH",
            message=(
                f"High risk safety report #{new_report.id} "
                "requires manager review."
            ),
            is_read=False
        )

        db.add(alert)
        db.commit()

    # ======================================
    # 10. RESPONSE
    # ======================================

    return {
        "status": "success",
        "report_id": new_report.id,
        "original_text": original_text,
        "processed_text": processed_text,
        "risk_level": risk_level,
        "primary_precursor": primary_precursor,
        "detected_precursors": detected_precursors,
        "recommendation": recommendation,
        "ai_result": ai_result
    }
    
    # ======================================
# MANAGER ALERTS
# ======================================

@app.get("/manager/alerts")
def manager_alerts(
    db: Session = Depends(get_db)
):
    alerts = (
        db.query(models.ManagerAlert)
        .filter(
            models.ManagerAlert.is_read.is_(False)
        )
        .order_by(
            models.ManagerAlert.id.desc()
        )
        .all()
    )

    return alerts

# ======================================
# MARK ALERT AS READ
# ======================================

@app.patch("/manager/alerts/{alert_id}/read")
def mark_alert_read(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = (
        db.query(models.ManagerAlert)
        .filter(
            models.ManagerAlert.id == alert_id
        )
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.is_read = True

    db.commit()

    return {
        "message": "Alert marked as read"
    }