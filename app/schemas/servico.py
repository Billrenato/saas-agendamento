from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ServicoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    duracao_minutos: int
    preco: Optional[float] = None
    ativo: Optional[bool] = True
    imagem: Optional[str] = None  # ← SÓ AQUI JÁ BASTA

class ServicoCreate(ServicoBase):
    pass

class ServicoResponse(ServicoBase):
    id: int
    empresa_id: int
    criado_em: datetime
    
    class Config:
        from_attributes = True