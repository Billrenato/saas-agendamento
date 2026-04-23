from sqlalchemy.orm import Session
from app.repositories.empresa_repository import EmpresaRepository
from app.models.empresa import Empresa
from typing import Optional

class EmpresaService:
    def __init__(self, db: Session):
        self.empresa_repo = EmpresaRepository(db)
    
    def get_empresa(self, empresa_id: int) -> Optional[Empresa]:
        return self.empresa_repo.get(empresa_id)
    
    def get_empresa_by_email(self, email: str) -> Optional[Empresa]:
        return self.empresa_repo.get_by_email(email)
    
    def get_empresa_by_slug(self, slug: str) -> Optional[Empresa]:
        return self.empresa_repo.get_by_slug(slug)