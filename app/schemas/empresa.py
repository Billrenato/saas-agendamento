from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class EmpresaBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    segmento: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    foto_capa: Optional[str] = None
    logo: Optional[str] = None
    descricao: Optional[str] = None
    horario_funcionamento: Optional[str] = None

class EmpresaCreate(EmpresaBase):
    senha: str

class EmpresaResponse(EmpresaBase):
    id: int
    ativo: bool
    criado_em: datetime
    
    class Config:
        from_attributes = True