from pydantic import BaseModel
from datetime import time, datetime
from typing import Optional

class AgendaBase(BaseModel):
    dia_semana: int  # 0-6
    hora_inicio: time
    hora_fim: time

class AgendaCreate(AgendaBase):
    pass

class AgendaResponse(AgendaBase):
    id: int
    empresa_id: int
    criado_em: datetime
    
    class Config:
        from_attributes = True