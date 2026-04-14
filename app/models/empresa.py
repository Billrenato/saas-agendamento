from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

# app/models/empresa.py
class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    
    # Campos existentes
    segmento = Column(String(100), nullable=True)
    endereco = Column(Text, nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    cep = Column(String(10), nullable=True)
    foto_capa = Column(Text, nullable=True)
    logo = Column(Text, nullable=True)
    descricao = Column(Text, nullable=True)
    horario_funcionamento = Column(Text, nullable=True)
    
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    # WhatsApp / Twilio
    twilio_account_sid = Column(String(100), nullable=True)
    twilio_auth_token = Column(String(100), nullable=True)
    twilio_whatsapp_number = Column(String(20), nullable=True)
    
    # Mensagens personalizadas
    whatsapp_welcome_message = Column(Text, nullable=True)
    whatsapp_confirmation_message = Column(Text, nullable=True)
    whatsapp_cancel_message = Column(Text, nullable=True)
    send_reminder_hours = Column(Integer, default=24)
    
    # Relacionamentos
    servicos = relationship("Servico", back_populates="empresa", cascade="all, delete-orphan")
    agenda = relationship("Agenda", back_populates="empresa", cascade="all, delete-orphan")
    agendamentos = relationship("Agendamento", back_populates="empresa", cascade="all, delete-orphan")