from sqlalchemy.orm import Session
from src.models.report import Report
from src.schemas.report import ReportCreate, ReportUpdate

def create_report(db: Session, report_data: ReportCreate, user_id: int):
    db_report = Report(
        **report_data.model_dump(),
        user_id=user_id,
        status="open" 
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_report_by_id(db: Session, report_id: int):
    return db.query(Report).filter(Report.id == report_id).first()

def get_all_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Report).offset(skip).limit(limit).all()

def get_my_reports(db: Session, user_id: int):
    """Business Logic: Buscar apenas as denúncias do usuário logado"""
    return db.query(Report).filter(Report.user_id == user_id).all()

def delete_report(db: Session, report_id: int, user_id: int):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    
    if not db_report:
        return None
    
    if db_report.user_id != user_id:
        return "not_authorized"

    db.delete(db_report)
    db.commit()
    return True

def update_report(db: Session, report_id: int, user_id: int, report_data: ReportUpdate):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    
    if not db_report:
        return None
        
    if db_report.user_id != user_id:
        return "not_authorized"
        
    update_data = report_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_report, key, value) # Substitui o valor antigo pelo novo
        
    db.commit()
    db.refresh(db_report)
    return db_report