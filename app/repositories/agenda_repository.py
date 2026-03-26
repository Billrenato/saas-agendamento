from sqlalchemy.orm import Session
from app.models.agenda import Agenda
from app.repositories.base import BaseRepository
from typing import List, Optional

class AgendaRepository(BaseRepository[Agenda]):
    def __init__(self, db: Session):
        super().__init__(db, Agenda)
    
    def get_by_empresa(self, empresa_id: int) -> List[Agenda]:
        return self.db.query(Agenda).filter(Agenda.empresa_id == empresa_id).all()
    
    def get_by_dia_semana(self, empresa_id: int, dia_semana: int) -> Optional[Agenda]:
        return self.db.query(Agenda).filter(
            Agenda.empresa_id == empresa_id,
            Agenda.dia_semana == dia_semana
        ).first()