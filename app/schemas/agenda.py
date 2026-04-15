# app/schemas/agenda.py
from pydantic import BaseModel
from datetime import time, datetime, date
from typing import Optional

class AgendaBase(BaseModel):
    dia_semana: Optional[int] = None
    data_especifica: Optional[date] = None
    hora_inicio: time
    hora_fim: time
    intervalo_inicio: Optional[time] = None
    intervalo_fim: Optional[time] = None
    is_excecao: Optional[bool] = False

class AgendaCreate(AgendaBase):
    pass

class AgendaResponse(AgendaBase):
    id: int
    empresa_id: int
    criado_em: datetime
    
    class Config:
        from_attributes = True