from pydantic import BaseModel, ConfigDict
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
    pass # No POST, enviamos exatamente o que está na Base

class ReportResponse(ReportBase):
    id: int
    status: str
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)