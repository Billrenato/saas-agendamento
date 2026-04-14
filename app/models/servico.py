from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Servico(Base):
    __tablename__ = "servicos"
    
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    duracao_minutos = Column(Integer, nullable=False)
    preco = Column(Float, nullable=True)
    ativo = Column(Boolean, default=True)  # ← NOVO CAMPO
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    imagem = Column(String, nullable=True)

    
    # Relacionamentos
    empresa = relationship("Empresa", back_populates="servicos")
    agendamentos = relationship("Agendamento", back_populates="servico")