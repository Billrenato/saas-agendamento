from sqlalchemy import Column, Integer, String, ForeignKey, Time, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Agenda(Base):
    __tablename__ = "agenda"
    
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    dia_semana = Column(Integer, nullable=False)  # 0=Segunda, 1=Terça, ... 6=Domingo
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    empresa = relationship("Empresa", back_populates="agenda")