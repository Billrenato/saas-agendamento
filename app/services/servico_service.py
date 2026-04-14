from sqlalchemy.orm import Session
from app.repositories.servico_repository import ServicoRepository
from app.schemas.servico import ServicoCreate
from app.models.servico import Servico
from typing import List

class ServicoService:
    def __init__(self, db: Session):
        self.servico_repo = ServicoRepository(db)
    
    def create_servico(self, empresa_id: int, servico_data: ServicoCreate) -> Servico:
        return self.servico_repo.create(
            empresa_id=empresa_id,
            **servico_data.dict()
        )
    
    def get_servicos_by_empresa(self, empresa_id: int, apenas_ativos: bool = False) -> List[Servico]:
        """Lista serviços da empresa"""
        query = self.servico_repo.db.query(Servico).filter(Servico.empresa_id == empresa_id)
        
        if apenas_ativos:
            query = query.filter(Servico.ativo == True)
        
        return query.all()
    
    """def get_servicos_by_empresa(self, empresa_id: int, apenas_ativos: bool = False) -> List[Servico]:
    Lista serviços da empresa
    return self.servico_repo.get_by_empresa(empresa_id, apenas_ativos)"""
    
    def get_servico(self, servico_id: int, empresa_id: int) -> Servico:
        servico = self.servico_repo.get(servico_id)
        if not servico or servico.empresa_id != empresa_id:
            return None
        return servico
    
    def update_servico(self, servico_id: int, empresa_id: int, servico_data: ServicoCreate) -> Servico:
        servico = self.get_servico(servico_id, empresa_id)
        if not servico:
            return None
        
        return self.servico_repo.update(servico_id, **servico_data.dict())
    
    def delete_servico(self, servico_id: int, empresa_id: int) -> bool:
        servico = self.get_servico(servico_id, empresa_id)
        if not servico:
            return False
        
        return self.servico_repo.delete(servico_id)