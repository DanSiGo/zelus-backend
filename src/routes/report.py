from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importações de conexão e lógica
from src.database import get_db
from src.schemas.report import ReportCreate, ReportResponse, ReportUpdate
from src.services import report as report_service

# Importação da segurança que está na raiz
from src.auth_utils import get_current_user_id 

router = APIRouter(prefix="/reports", tags=["Reports 📝"])

@router.post(
    "/", 
    response_model=ReportResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova denúncia",
    description="Registra um novo problema urbano (buraco, poste, lixo) no banco de dados. O 'user_id' é preenchido automaticamente pelo sistema através do Token JWT."
)
def create_new_report(
    report_data: ReportCreate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id) # Extrai o ID do Token
):
    return report_service.create_report(
        db=db, 
        report_data=report_data, 
        user_id=current_user_id
    )

@router.get(
    "/", 
    response_model=List[ReportResponse],
    summary="Listar todas as denúncias",
    description="Lista todas as denúncias registradas no sistema de forma pública. Rota ideal para plotar os pinos no mapa do aplicativo."
)
def list_all_reports(db: Session = Depends(get_db)):
    return report_service.get_all_reports(db)

@router.get(
    "/me", 
    response_model=List[ReportResponse],
    summary="Listar minhas denúncias",
    description="Retorna apenas as denúncias feitas pelo usuário logado no momento. Requer um Token de Autenticação válido."
)
def list_my_reports(
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    return report_service.get_my_reports(db, user_id=current_user_id)

@router.get(
    "/{report_id}", 
    response_model=ReportResponse,
    summary="Buscar denúncia por ID",
    description="Busca os detalhes completos de uma denúncia específica utilizando o seu número de identificação (ID)."
)
def read_report(report_id: int, db: Session = Depends(get_db)):
    db_report = report_service.get_report_by_id(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Denúncia não encontrada")
    return db_report

@router.delete(
    "/{report_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar denúncia",
    description="Apaga uma denúncia permanentemente do banco de dados. **Atenção:** Por segurança, apenas o criador original da denúncia tem permissão para deletá-la."
)
def delete_existing_report(
    report_id: int, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    success = report_service.delete_report(db, report_id, user_id=current_user_id)
    
    if success is None:
        raise HTTPException(status_code=404, detail="Denúncia não encontrada")
    
    if success == "not_authorized":
        raise HTTPException(
            status_code=403, 
            detail="Você não tem permissão para apagar uma denúncia que não é sua!"
        )
    
    return None 

@router.patch(
    "/{report_id}", 
    response_model=ReportResponse,
    summary="Atualizar denúncia (Parcial)",
    description="Atualiza uma denúncia existente. Apenas os campos enviados no corpo da requisição serão alterados (PATCH). Apenas o dono da denúncia pode editá-la."
)
def update_existing_report(
    report_id: int,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    updated_report = report_service.update_report(
        db=db, 
        report_id=report_id, 
        user_id=current_user_id, 
        report_data=report_data
    )
    
    if updated_report is None:
        raise HTTPException(status_code=404, detail="Denúncia não encontrada")
        
    if updated_report == "not_authorized":
        raise HTTPException(
            status_code=403, 
            detail="Você não tem permissão para editar uma denúncia que não é sua!"
        )
        
    return updated_report