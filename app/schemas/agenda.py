from pydantic import BaseModel
from datetime import time, datetime, date
from typing import Optional

class AgendaBase(BaseModel):
    dia_semana: Optional[int] = None  # 0=segunda a 6=domingo
    data_especifica: Optional[date] = None
    hora_inicio: time
    hora_fim: time
    intervalo_inicio: Optional[time] = None
    intervalo_fim: Optional[time] = None
    is_excecao: Optional[bool] = False
    atendente_id: Optional[int] = None  # 👈 NOVO

class AgendaCreate(AgendaBase):
    pass

class AgendaUpdate(BaseModel):
    dia_semana: Optional[int] = None
    data_especifica: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fim: Optional[time] = None
    intervalo_inicio: Optional[time] = None
    intervalo_fim: Optional[time] = None
    is_excecao: Optional[bool] = None
    atendente_id: Optional[int] = None

class AgendaResponse(AgendaBase):
    id: int
    empresa_id: int
    criado_em: datetime
    atendente_nome: Optional[str] = None  # 👈 NOVO (para mostrar no front)
    
    class Config:
        from_attributes = True