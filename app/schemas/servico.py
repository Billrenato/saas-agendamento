from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.atendente import AtendenteBasicoResponse

class ServicoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    duracao_minutos: int
    preco: Optional[float] = None
    ativo: Optional[bool] = True
    imagem: Optional[str] = None

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    duracao_minutos: Optional[int] = None
    preco: Optional[float] = None
    ativo: Optional[bool] = None
    imagem: Optional[str] = None

class ServicoResponse(ServicoBase):
    id: int
    empresa_id: int
    criado_em: datetime
    
    class Config:
        from_attributes = True

class ServicoBasicoResponse(BaseModel):
    """Versão simplificada do serviço (sem empresa_id)"""
    id: int
    nome: str
    duracao_minutos: int
    preco: Optional[float] = None
    
    class Config:
        from_attributes = True

class ServicoComAtendentesResponse(ServicoResponse):
    """Serviço com lista de atendentes que o realizam"""
    atendentes: Optional[List['AtendenteBasicoResponse']] = []

# Resolve a importação circular
from app.schemas.atendente import AtendenteBasicoResponse
ServicoComAtendentesResponse.model_rebuild()