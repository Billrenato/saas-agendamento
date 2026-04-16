# app/models/agenda.py
from sqlalchemy import Column, Integer, String, ForeignKey, Time, DateTime, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Agenda(Base):
    __tablename__ = "agenda"
    
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    dia_semana = Column(Integer, nullable=True)  # Pode ser NULL para exceções
    data_especifica = Column(Date, nullable=True)  # Data específica para exceções
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    intervalo_inicio = Column(Time, nullable=True)
    intervalo_fim = Column(Time, nullable=True)
    is_excecao = Column(Boolean, default=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    empresa = relationship("Empresa", back_populates="agenda")
    atendente_id = Column(Integer, ForeignKey("atendentes.id", ondelete="CASCADE"), nullable=True)
    atendente = relationship("Atendente", back_populates="agenda")