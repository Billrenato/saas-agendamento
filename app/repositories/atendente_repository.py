from sqlalchemy.orm import Session, joinedload
from app.models.atendente import Atendente
from app.models.atendente_servico import AtendenteServico
from app.models.servico import Servico
from app.repositories.base import BaseRepository
from typing import List, Optional

class AtendenteRepository(BaseRepository[Atendente]):
    def __init__(self, db: Session):
        super().__init__(db, Atendente)
    
    def get_by_empresa(self, empresa_id: int, apenas_ativos: bool = True) -> List[Atendente]:
        query = self.db.query(Atendente).filter(Atendente.empresa_id == empresa_id)
        if apenas_ativos:
            query = query.filter(Atendente.ativo == True)
        return query.order_by(Atendente.ordem_exibicao).all()
    
    def get_by_empresa_com_servicos(self, empresa_id: int) -> List[Atendente]:
        atendentes = self.db.query(Atendente).filter(
            Atendente.empresa_id == empresa_id,
            Atendente.ativo == True
        ).order_by(Atendente.ordem_exibicao).all()
        
        # Carregar serviços para cada atendente
        for atendente in atendentes:
            servicos = self.db.query(Servico).join(
                AtendenteServico, AtendenteServico.servico_id == Servico.id
            ).filter(
                AtendenteServico.atendente_id == atendente.id
            ).all()
            atendente.servicos_list = servicos
        
        return atendentes
    
    def get_servicos_do_atendente(self, atendente_id: int) -> List[int]:
        servicos = self.db.query(AtendenteServico).filter(
            AtendenteServico.atendente_id == atendente_id
        ).all()
        return [s.servico_id for s in servicos]
    
    def sync_servicos(self, atendente_id: int, servico_ids: List[int]):
        # Remove todos
        self.db.query(AtendenteServico).filter(
            AtendenteServico.atendente_id == atendente_id
        ).delete()
        
        # Adiciona os novos
        for servico_id in servico_ids:
            rel = AtendenteServico(atendente_id=atendente_id, servico_id=servico_id)
            self.db.add(rel)
        
        self.db.commit()