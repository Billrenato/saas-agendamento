from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class StatusAgendamento(str, enum.Enum):
    PENDENTE = "pendente"
    ACEITO = "aceito"
    RECUSADO = "recusado"
    CANCELADO = "cancelado"

class Agendamento(Base):
    __tablename__ = "agendamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id", ondelete="CASCADE"), nullable=False)
    nome_cliente = Column(String, nullable=False)
    telefone_cliente = Column(String, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    status = Column(Enum(StatusAgendamento), default=StatusAgendamento.PENDENTE)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    empresa = relationship("Empresa", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")
    # Adicione no final da classe Agendamento:
    atendente_id = Column(Integer, ForeignKey("atendentes.id", ondelete="SET NULL"), nullable=True)
    atendente = relationship("Atendente", back_populates="agendamentos")