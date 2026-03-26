from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    servicos = relationship("Servico", back_populates="empresa", cascade="all, delete-orphan")
    agenda = relationship("Agenda", back_populates="empresa", cascade="all, delete-orphan")
    agendamentos = relationship("Agendamento", back_populates="empresa", cascade="all, delete-orphan")