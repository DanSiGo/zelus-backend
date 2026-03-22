from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.report import Report
from src.schemas.report import ReportCreate, ReportOut

router = APIRouter(prefix="/report", tags=["Reports"])


@router.post("/", response_model=ReportOut, status_code=status.HTTP_201_CREATED)
def create_report(report_in: ReportCreate, db: Session = Depends(get_db)):
  
    new_report = Report(
        title=report_in.title,
        description=report_in.description,
        category=report_in.category,
        latitude=report_in.latitude,
        longitude=report_in.longitude,
        user_id=1  
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


@router.get("/", response_model=List[ReportOut])
def get_reports(db: Session = Depends(get_db)):
    return db.query(Report).all()