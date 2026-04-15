# app/repositories/agenda_repository.py
from sqlalchemy.orm import Session
from app.models.agenda import Agenda
from app.repositories.base import BaseRepository
from typing import List, Optional
from datetime import date

class AgendaRepository(BaseRepository[Agenda]):
    def __init__(self, db: Session):
        super().__init__(db, Agenda)
    
    def get_by_empresa(self, empresa_id: int) -> List[Agenda]:
        return self.db.query(Agenda).filter(Agenda.empresa_id == empresa_id).all()
    
    def get_by_dia_semana(self, empresa_id: int, dia_semana: int, data: Optional[date] = None) -> Optional[Agenda]:
        """Busca agenda por dia da semana ou data específica"""
        # Primeiro, verificar se existe exceção para esta data
        if data:
            excecao = self.db.query(Agenda).filter(
                Agenda.empresa_id == empresa_id,
                Agenda.data_especifica == data
            ).first()
            if excecao:
                return excecao
        
        # Se não tem exceção, buscar configuração padrão por dia da semana
        return self.db.query(Agenda).filter(
            Agenda.empresa_id == empresa_id,
            Agenda.dia_semana == dia_semana,
            Agenda.data_especifica.is_(None)
        ).first()
    
    def get_by_data_especifica(self, empresa_id: int, data: date) -> Optional[Agenda]:
        return self.db.query(Agenda).filter(
            Agenda.empresa_id == empresa_id,
            Agenda.data_especifica == data
        ).first()