from pydantic import BaseModel, EmailStr
from typing import Optional

class EmpresaRegister(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    telefone: str
    segmento: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    descricao: Optional[str] = None

class EmpresaLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    empresa_id: Optional[int] = None