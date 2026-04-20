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
    
    def get_by_empresa_com_atendentes(self, empresa_id: int) -> List[Agenda]:
        """Busca todas as agendas da empresa, incluindo informações do atendente"""
        return self.db.query(Agenda).filter(Agenda.empresa_id == empresa_id).all()
    
    def get_by_atendente(self, atendente_id: int, empresa_id: int) -> List[Agenda]:
        """Busca agenda de um atendente específico"""
        return self.db.query(Agenda).filter(
            Agenda.empresa_id == empresa_id,
            Agenda.atendente_id == atendente_id
        ).all()
    
    def get_by_dia_semana(self, empresa_id: int, dia_semana: int, data: Optional[date] = None, atendente_id: Optional[int] = None) -> Optional[Agenda]:
        """Busca agenda por dia da semana ou data específica, podendo filtrar por atendente"""
        # Primeiro, verificar se existe exceção para esta data
        if data:
            query = self.db.query(Agenda).filter(
                Agenda.empresa_id == empresa_id,
                Agenda.data_especifica == data
            )
            if atendente_id:
                query = query.filter(Agenda.atendente_id == atendente_id)
            # 👈 REMOVA O ELSE! Não filtrar por NULL!
            
            excecao = query.first()
            if excecao:
                return excecao
        
        # Se não tem exceção, buscar configuração padrão por dia da semana
        query = self.db.query(Agenda).filter(
            Agenda.empresa_id == empresa_id,
            Agenda.dia_semana == dia_semana,
            Agenda.data_especifica.is_(None)
        )
        
        if atendente_id:
            query = query.filter(Agenda.atendente_id == atendente_id)
        # 👈 REMOVA O ELSE! Não filtrar por NULL!
        
        return query.first()
    
    def get_by_data_especifica(self, empresa_id: int, data: date, atendente_id: Optional[int] = None) -> Optional[Agenda]:
        query = self.db.query(Agenda).filter(
            Agenda.empresa_id == empresa_id,
            Agenda.data_especifica == data
        )
        
        if atendente_id:
            query = query.filter(Agenda.atendente_id == atendente_id)
        else:
            query = query.filter(Agenda.atendente_id.is_(None))
        
        return query.first()