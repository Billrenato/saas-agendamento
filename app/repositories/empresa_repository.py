from sqlalchemy.orm import Session
from app.models.empresa import Empresa
from app.repositories.base import BaseRepository
from typing import Optional

class EmpresaRepository(BaseRepository[Empresa]):
    def __init__(self, db: Session):
        super().__init__(db, Empresa)
    
    def get_by_email(self, email: str) -> Optional[Empresa]:
        return self.db.query(Empresa).filter(Empresa.email == email).first()