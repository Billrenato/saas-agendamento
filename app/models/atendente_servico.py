from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class AtendenteServico(Base):
    __tablename__ = "atendente_servicos"
    
    id = Column(Integer, primary_key=True, index=True)
    atendente_id = Column(Integer, ForeignKey("atendentes.id", ondelete="CASCADE"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id", ondelete="CASCADE"), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    atendente = relationship("Atendente", back_populates="servicos")
    servico = relationship("Servico", back_populates="atendentes")