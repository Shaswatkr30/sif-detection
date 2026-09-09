from pydantic import BaseModel


class ReportCreate(BaseModel):

    report_text: str


class ReportResponse(BaseModel):

    id: int
    report_text: str
    risk_level: str
    primary_precursor: str
    confidence: float

    class Config:
        from_attributes = True