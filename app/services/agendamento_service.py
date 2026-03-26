from sqlalchemy.orm import Session
from app.repositories.agendamento_repository import AgendamentoRepository
from app.repositories.servico_repository import ServicoRepository
from app.repositories.empresa_repository import EmpresaRepository
from app.schemas.agendamento import AgendamentoCreate, StatusAgendamento
from app.models.agendamento import Agendamento
from app.services.whatsapp_service import WhatsAppService
from typing import List, Optional
from datetime import datetime

class AgendamentoService:
    def __init__(self, db: Session):
        self.agendamento_repo = AgendamentoRepository(db)
        self.servico_repo = ServicoRepository(db)
        self.empresa_repo = EmpresaRepository(db)
        self.whatsapp_service = WhatsAppService()
    
    def create_agendamento(self, agendamento_data: AgendamentoCreate) -> Optional[Agendamento]:
        # Verificar serviço
        servico = self.servico_repo.get(agendamento_data.servico_id)
        if not servico:
            raise ValueError("Serviço não encontrado")
        
        # Verificar conflito de horário
        conflito = self.agendamento_repo.check_conflict(
            servico.empresa_id,
            agendamento_data.data_hora,
            servico.duracao_minutos
        )
        
        if conflito:
            raise ValueError("Horário já ocupado")
        
        # Criar agendamento
        agendamento = self.agendamento_repo.create(
            empresa_id=servico.empresa_id,
            servico_id=agendamento_data.servico_id,
            nome_cliente=agendamento_data.nome_cliente,
            telefone_cliente=agendamento_data.telefone_cliente,
            data_hora=agendamento_data.data_hora,
            status=StatusAgendamento.PENDENTE
        )
        
        return agendamento
    
    def get_agendamentos_by_empresa(self, empresa_id: int, skip: int = 0, limit: int = 100) -> List[Agendamento]:
        return self.agendamento_repo.get_by_empresa(empresa_id, skip, limit)
    
    def get_agendamento(self, agendamento_id: int, empresa_id: int) -> Optional[Agendamento]:
        agendamento = self.agendamento_repo.get(agendamento_id)
        if not agendamento or agendamento.empresa_id != empresa_id:
            return None
        return agendamento
    
    def update_status(self, agendamento_id: int, empresa_id: int, status: StatusAgendamento) -> Optional[Agendamento]:
        agendamento = self.get_agendamento(agendamento_id, empresa_id)
        if not agendamento:
            return None
        
        agendamento = self.agendamento_repo.update(agendamento_id, status=status)
        
        # Enviar WhatsApp se status for ACEITO
        if status == StatusAgendamento.ACEITO:
            empresa = self.empresa_repo.get(empresa_id)
            servico = self.servico_repo.get(agendamento.servico_id)
            
            mensagem = f"Agendamento confirmado:\nCliente: {agendamento.nome_cliente}\nServiço: {servico.nome}\nData: {agendamento.data_hora.strftime('%d/%m/%Y às %H:%M')}"
            
            self.whatsapp_service.send_message(
                to=agendamento.telefone_cliente,
                message=mensagem,
                empresa_telefone=empresa.telefone
            )
        
        return agendamento