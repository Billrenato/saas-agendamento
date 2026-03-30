from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.agendamento import Agendamento, StatusAgendamento
from app.repositories.base import BaseRepository
from datetime import datetime
from typing import List, Optional

class AgendamentoRepository(BaseRepository[Agendamento]):
    def __init__(self, db: Session):
        super().__init__(db, Agendamento)
    
    def get_by_empresa(self, empresa_id: int, skip: int = 0, limit: int = 100) -> List[Agendamento]:
        return self.db.query(Agendamento).filter(
            Agendamento.empresa_id == empresa_id
        ).order_by(Agendamento.data_hora.desc()).offset(skip).limit(limit).all()
    
    def get_by_data(self, empresa_id: int, data: datetime) -> List[Agendamento]:
        start = datetime(data.year, data.month, data.day, 0, 0, 0)
        end = datetime(data.year, data.month, data.day, 23, 59, 59)
        return self.db.query(Agendamento).filter(
            and_(
                Agendamento.empresa_id == empresa_id,
                Agendamento.data_hora >= start,
                Agendamento.data_hora <= end,
                Agendamento.status.in_([StatusAgendamento.PENDENTE, StatusAgendamento.ACEITO])
            )
        ).all()
    
    def check_conflict(self, empresa_id: int, data_hora: datetime, duracao_minutos: int) -> bool:
        from datetime import timedelta
        from sqlalchemy import and_
        
        end_time = data_hora + timedelta(minutes=duracao_minutos)
        
        # Buscar todos agendamentos ativos da empresa
        agendamentos = self.db.query(Agendamento).filter(
            and_(
                Agendamento.empresa_id == empresa_id,
                Agendamento.status.in_([StatusAgendamento.PENDENTE, StatusAgendamento.ACEITO])
            )
        ).all()
        
        # Verificar conflito em Python (mais simples e evita erros de SQL)
        for ag in agendamentos:
            ag_end = ag.data_hora + timedelta(minutes=ag.servico.duracao_minutos)
            if (data_hora < ag_end and end_time > ag.data_hora):
                return True
        
        return False