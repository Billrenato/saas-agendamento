from sqlalchemy.orm import Session
from app.repositories.agenda_repository import AgendaRepository
from app.schemas.agenda import AgendaCreate
from app.models.agenda import Agenda
from typing import List, Optional
from datetime import time

class AgendaService:
    def __init__(self, db: Session):
        self.agenda_repo = AgendaRepository(db)
    
    def create_agenda(self, empresa_id: int, agenda_data: AgendaCreate) -> Agenda:
        # Verificar se já existe agenda para este dia
        existing = self.agenda_repo.get_by_dia_semana(empresa_id, agenda_data.dia_semana)
        if existing:
            raise ValueError("Agenda já existe para este dia da semana")
        
        return self.agenda_repo.create(
            empresa_id=empresa_id,
            **agenda_data.dict()
        )
    
    def get_agenda_by_empresa(self, empresa_id: int) -> List[Agenda]:
        return self.agenda_repo.get_by_empresa(empresa_id)
    
    def get_agenda(self, agenda_id: int, empresa_id: int) -> Optional[Agenda]:
        agenda = self.agenda_repo.get(agenda_id)
        if not agenda or agenda.empresa_id != empresa_id:
            return None
        return agenda
    
    def update_agenda(self, agenda_id: int, empresa_id: int, agenda_data: AgendaCreate) -> Optional[Agenda]:
        agenda = self.get_agenda(agenda_id, empresa_id)
        if not agenda:
            return None
        
        # Verificar conflito de dia
        existing = self.agenda_repo.get_by_dia_semana(empresa_id, agenda_data.dia_semana)
        if existing and existing.id != agenda_id:
            raise ValueError("Outra agenda já existe para este dia da semana")
        
        return self.agenda_repo.update(agenda_id, **agenda_data.dict())
    
    def delete_agenda(self, agenda_id: int, empresa_id: int) -> bool:
        agenda = self.get_agenda(agenda_id, empresa_id)
        if not agenda:
            return False
        
        return self.agenda_repo.delete(agenda_id)
    
    def get_horarios_disponiveis(self, empresa_id: int, data: str, servico_id: int = None) -> List[str]:
        from datetime import datetime, timedelta
        import pytz
        
        data_obj = datetime.strptime(data, "%Y-%m-%d")
        dia_semana = data_obj.weekday()
        
        # Buscar agenda do dia
        agenda = self.agenda_repo.get_by_dia_semana(empresa_id, dia_semana)
        if not agenda:
            return []
        
        # Buscar agendamentos do dia
        from app.repositories.agendamento_repository import AgendamentoRepository
        agendamento_repo = AgendamentoRepository(self.agenda_repo.db)
        agendamentos = agendamento_repo.get_by_data(empresa_id, data_obj)
        
        # Gerar horários disponíveis
        horarios = []
        hora_atual = datetime.combine(data_obj.date(), agenda.hora_inicio)
        hora_fim = datetime.combine(data_obj.date(), agenda.hora_fim)
        
        # Se não tem serviço específico, usar duração padrão de 30 minutos
        duracao_padrao = 30
        if servico_id:
            from app.repositories.servico_repository import ServicoRepository
            servico_repo = ServicoRepository(self.agenda_repo.db)
            servico = servico_repo.get(servico_id)
            if servico:
                duracao_padrao = servico.duracao_minutos
        
        while hora_atual + timedelta(minutes=duracao_padrao) <= hora_fim:
            # Verificar conflito
            conflito = False
            for agendamento in agendamentos:
                agendamento_fim = agendamento.data_hora + timedelta(minutes=agendamento.servico.duracao_minutos)
                if (hora_atual < agendamento_fim and 
                    hora_atual + timedelta(minutes=duracao_padrao) > agendamento.data_hora):
                    conflito = True
                    break
            
            if not conflito:
                horarios.append(hora_atual.strftime("%H:%M"))
            
            hora_atual += timedelta(minutes=30)  # Intervalo de 30 minutos
        
        return horarios