from sqlalchemy.orm import Session
from app.repositories.atendente_repository import AtendenteRepository
from app.repositories.servico_repository import ServicoRepository
from app.schemas.atendente import AtendenteCreate, AtendenteUpdate
from app.models.atendente import Atendente
from typing import List, Optional

class AtendenteService:
    def __init__(self, db: Session):
        self.atendente_repo = AtendenteRepository(db)
        self.servico_repo = ServicoRepository(db)
    
    def create_atendente(self, empresa_id: int, data: AtendenteCreate) -> Atendente:
        # Verificar se os serviços existem
        for servico_id in data.servico_ids:
            if not self.servico_repo.get(servico_id):
                raise ValueError(f"Serviço {servico_id} não encontrado")
        
        # Criar atendente
        atendente = self.atendente_repo.create(
            empresa_id=empresa_id,
            nome=data.nome,
            email=data.email,
            telefone=data.telefone,
            foto=data.foto,
            ativo=data.ativo,
            ordem_exibicao=data.ordem_exibicao
        )
        
        # Vincular serviços
        if data.servico_ids:
            self.atendente_repo.sync_servicos(atendente.id, data.servico_ids)
        
        return atendente
    
    def get_atendentes_by_empresa(self, empresa_id: int, com_servicos: bool = False) -> List[Atendente]:
        if com_servicos:
            return self.atendente_repo.get_by_empresa_com_servicos(empresa_id)
        return self.atendente_repo.get_by_empresa(empresa_id)
    
    def get_atendente(self, atendente_id: int, empresa_id: int) -> Optional[Atendente]:
        atendente = self.atendente_repo.get(atendente_id)
        if not atendente or atendente.empresa_id != empresa_id:
            return None
        return atendente
    
    def update_atendente(self, atendente_id: int, empresa_id: int, data: AtendenteUpdate) -> Optional[Atendente]:
        atendente = self.get_atendente(atendente_id, empresa_id)
        if not atendente:
            return None
        
        update_data = data.model_dump(exclude_unset=True, exclude={'servico_ids'})
        if update_data:
            atendente = self.atendente_repo.update(atendente_id, **update_data)
        
        if data.servico_ids is not None:
            self.atendente_repo.sync_servicos(atendente_id, data.servico_ids)
        
        return atendente
    
    def delete_atendente(self, atendente_id: int, empresa_id: int) -> bool:
        atendente = self.get_atendente(atendente_id, empresa_id)
        if not atendente:
            return False
        
        # Soft delete (apenas desativa)
        self.atendente_repo.update(atendente_id, ativo=False)
        return True
    
    def get_servicos_do_atendente(self, atendente_id: int, empresa_id: int) -> List[int]:
        atendente = self.get_atendente(atendente_id, empresa_id)
        if not atendente:
            return []
        return self.atendente_repo.get_servicos_do_atendente(atendente_id)