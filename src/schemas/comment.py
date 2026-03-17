from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    report_id: int

class CommentCreate(CommentBase):
    pass  # O que o front-end envia para criar um comentário

class CommentResponse(CommentBase):
    id: int
    user_id: int
    created_at: datetime

    # Necessário para converter o objeto do banco (SQLAlchemy) para JSON
    model_config = ConfigDict(from_attributes=True)