from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Boolean

from datetime import datetime

from database import Base


class Report(Base):

    __tablename__ = "reports"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    report_text = Column(
        Text,
        nullable=False
    )

    risk_level = Column(
        String,
        nullable=False
    )

    primary_precursor = Column(
        String,
        nullable=False
    )

    confidence = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ==============================
# MANAGER ALERTS
# ==============================



class ManagerAlert(Base):

    __tablename__ = "manager_alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    report_id = Column(
        Integer,
        nullable=False
    )

    risk_level = Column(
        String,
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    is_read = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )