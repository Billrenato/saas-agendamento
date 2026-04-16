from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AtendenteBase(BaseModel):
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    foto: Optional[str] = None
    ativo: Optional[bool] = True
    ordem_exibicao: Optional[int] = 0

class AtendenteCreate(AtendenteBase):
    servico_ids: Optional[List[int]] = []

class AtendenteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    foto: Optional[str] = None
    ativo: Optional[bool] = None
    ordem_exibicao: Optional[int] = None
    servico_ids: Optional[List[int]] = None

class AtendenteResponse(AtendenteBase):
    id: int
    empresa_id: int
    criado_em: datetime
    servicos: Optional[List[dict]] = []  # Será populado com os serviços
    
    class Config:
        from_attributes = True

class AtendenteBasicoResponse(BaseModel):
    id: int
    nome: str
    foto: Optional[str] = None
    
    class Config:
        from_attributes = True