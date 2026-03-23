from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 1. Definição básica (o que é comum a todos)
class ReportBase(BaseModel):
    title: str
    description: str
    category: str
    latitude: float
    longitude: float
    image_url: Optional[str] = None # Deixe aqui para facilitar a Tarefa #4 depois!

# 2. O que o usuário envia (Request)
class ReportCreate(ReportBase):
    pass

# 3. O que a API devolve (Response) - ESSA PARTE É A QUE ESTÁ FALTANDO!
class ReportOut(ReportBase):
    id: int
    status: str = "Aberto"
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True