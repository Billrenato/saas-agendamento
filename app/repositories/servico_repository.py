# app/repositories/servico_repository.py
from sqlalchemy.orm import Session
from app.models.servico import Servico
from app.repositories.base import BaseRepository
from typing import List, Optional

class ServicoRepository(BaseRepository[Servico]):
    def __init__(self, db: Session):
        super().__init__(db, Servico)
    
    def get_by_empresa(self, empresa_id: int, apenas_ativos: bool = False) -> List[Servico]:
        query = self.db.query(Servico).filter(Servico.empresa_id == empresa_id)
        if apenas_ativos:
            query = query.filter(Servico.ativo == True)
        return query.all()