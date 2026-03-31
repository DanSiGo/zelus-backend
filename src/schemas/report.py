from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportBase(BaseModel):
    title: str
    description: str
    category: str
    latitude: float
    longitude: float
    image_url: Optional[str] = None 

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int
    status: str = "Aberto"
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    image_url: Optional[str] = None