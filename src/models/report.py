from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    category = Column(String(50))  # Ex: "Buraco", "Poste Caído", "Vazamento"
    
    # Coordenadas para o mapa
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    image_url = Column(String(255), nullable=True) # Link da foto no Supabase/S3
    status = Column(String(20), default="aberto")  # aberto, em_analise, resolvido
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Chave estrangeira para o usuário que criou
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relacionamentos
    owner = relationship("User", back_populates="reports")
    comments = relationship("Comment", back_populates="report")