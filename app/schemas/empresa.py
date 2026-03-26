from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class EmpresaBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str

class EmpresaCreate(EmpresaBase):
    senha: str

class EmpresaResponse(EmpresaBase):
    id: int
    ativo: bool
    criado_em: datetime
    
    class Config:
        from_attributes = True