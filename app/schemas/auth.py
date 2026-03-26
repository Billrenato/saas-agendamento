from pydantic import BaseModel, EmailStr
from typing import Optional

class EmpresaRegister(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    telefone: str

class EmpresaLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    empresa_id: Optional[int] = None