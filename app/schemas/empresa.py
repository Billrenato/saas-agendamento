from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class EmpresaBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str = Field(..., min_length=10, max_length=11)
    segmento: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    foto_capa: Optional[str] = None
    logo: Optional[str] = None
    descricao: Optional[str] = None
    horario_funcionamento: Optional[str] = None



class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    segmento: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    descricao: Optional[str] = None
    foto_capa: Optional[str] = None
    logo: Optional[str] = None
    horario_funcionamento: Optional[str] = None
        

class EmpresaCreate(EmpresaBase):
    senha: str

class EmpresaResponse(EmpresaBase):
    id: int
    ativo: bool
    criado_em: datetime
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_whatsapp_number: Optional[str] = None
    send_reminder_hours: Optional[int] = None
    whatsapp_confirmation_message: Optional[str] = None
    whatsapp_welcome_message: Optional[str] = None
    whatsapp_cancel_message: Optional[str] = None
    
    class Config:
        from_attributes = True



