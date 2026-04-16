from sqlalchemy.orm import Session
from app.repositories.servico_repository import ServicoRepository
from app.schemas.servico import ServicoCreate
from app.models.servico import Servico
from typing import List, Optional

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
    
    def get_servico(self, servico_id: int, empresa_id: int) -> Optional[Servico]:
        servico = self.servico_repo.get(servico_id)
        if not servico or servico.empresa_id != empresa_id:
            return None
        return servico
    
    def update_servico(self, servico_id: int, empresa_id: int, servico_data: ServicoCreate) -> Optional[Servico]:
        servico = self.get_servico(servico_id, empresa_id)
        if not servico:
            return None
        
        return self.servico_repo.update(servico_id, **servico_data.dict())
    
    def delete_servico(self, servico_id: int, empresa_id: int) -> bool:
        servico = self.get_servico(servico_id, empresa_id)
        if not servico:
            return False
        
        return self.servico_repo.delete(servico_id)
    
    # 👇 NOVO MÉTODO - ADICIONAR NO FINAL
    def get_servicos_by_ids(self, servico_ids: List[int], empresa_id: int) -> List[Servico]:
        """
        Busca serviços por uma lista de IDs, verificando se pertencem à empresa
        """
        if not servico_ids:
            return []
        
        return self.servico_repo.db.query(Servico).filter(
            Servico.id.in_(servico_ids),
            Servico.empresa_id == empresa_id
        ).all()