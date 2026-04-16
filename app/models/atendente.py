from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Atendente(Base):
    __tablename__ = "atendentes"
    
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    telefone = Column(String(20), nullable=True)
    foto = Column(String(500), nullable=True)
    ativo = Column(Boolean, default=True)
    ordem_exibicao = Column(Integer, default=0)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    empresa = relationship("Empresa", back_populates="atendentes")
    servicos = relationship("AtendenteServico", back_populates="atendente", cascade="all, delete-orphan")
    agenda = relationship("Agenda", back_populates="atendente")
    agendamentos = relationship("Agendamento", back_populates="atendente")