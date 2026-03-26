from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class StatusAgendamento(str, Enum):
    PENDENTE = "pendente"
    ACEITO = "aceito"
    RECUSADO = "recusado"
    CANCELADO = "cancelado"

class AgendamentoBase(BaseModel):
    nome_cliente: str
    telefone_cliente: str
    data_hora: datetime
    servico_id: int

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoResponse(AgendamentoBase):
    id: int
    empresa_id: int
    status: StatusAgendamento
    criado_em: datetime
    
    class Config:
        from_attributes = True

class AgendamentoStatusUpdate(BaseModel):
    status: StatusAgendamento