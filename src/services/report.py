from sqlalchemy.orm import Session
from src.models.report import Report
from src.schemas.report import ReportCreate

def create_report(db: Session, report_data: ReportCreate, user_id: int):
    # Criamos o objeto associando ao ID do usuário autenticado
    db_report = Report(
        **report_data.model_dump(),
        user_id=user_id,
        status="open" 
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_all_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Report).offset(skip).limit(limit).all()

def get_my_reports(db: Session, user_id: int):
    """Business Logic: Buscar apenas as denúncias do usuário logado"""
    return db.query(Report).filter(Report.user_id == user_id).all()