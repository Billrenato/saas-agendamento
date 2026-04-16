# app/services/agenda_service.py
from sqlalchemy.orm import Session
from app.repositories.agenda_repository import AgendaRepository
from app.schemas.agenda import AgendaCreate
from app.models.agenda import Agenda
from typing import List, Optional
from datetime import date

class AgendaService:
    def __init__(self, db: Session):
        self.agenda_repo = AgendaRepository(db)
    
    def create_agenda(self, empresa_id: int, agenda_data: AgendaCreate) -> Agenda:
        # Se for exceção (data específica), dia_semana deve ser None
        if agenda_data.is_excecao:
            agenda_data.dia_semana = None
        
        # Verificar se já existe configuração para este dia/data
        if agenda_data.data_especifica:
            # Buscar por data específica
            existing = self.agenda_repo.db.query(Agenda).filter(
                Agenda.empresa_id == empresa_id,
                Agenda.data_especifica == agenda_data.data_especifica
            ).first()
        else:
            # Buscar por dia da semana (apenas configurações padrão)
            existing = self.agenda_repo.db.query(Agenda).filter(
                Agenda.empresa_id == empresa_id,
                Agenda.dia_semana == agenda_data.dia_semana,
                Agenda.data_especifica.is_(None)
            ).first()
        
        if existing:
            raise ValueError("Já existe uma configuração para este dia/data")
        
        # Criar novo registro
        return self.agenda_repo.create(
            empresa_id=empresa_id,
            dia_semana=agenda_data.dia_semana,
            data_especifica=agenda_data.data_especifica,
            hora_inicio=agenda_data.hora_inicio,
            hora_fim=agenda_data.hora_fim,
            intervalo_inicio=agenda_data.intervalo_inicio,
            intervalo_fim=agenda_data.intervalo_fim,
            is_excecao=agenda_data.is_excecao or False,
            atendente_id=agenda_data.atendente_id  # 👈 NOVO
        )
    
    def get_agenda_by_empresa(self, empresa_id: int) -> List[Agenda]:
        return self.agenda_repo.get_by_empresa(empresa_id)
    
    # 👇 NOVO MÉTODO
    def get_agenda_by_atendente(self, empresa_id: int, atendente_id: int) -> List[Agenda]:
        """Busca agenda de um atendente específico"""
        return self.agenda_repo.get_by_atendente(atendente_id, empresa_id)
    
    def get_agenda(self, agenda_id: int, empresa_id: int) -> Optional[Agenda]:
        agenda = self.agenda_repo.get(agenda_id)
        if not agenda or agenda.empresa_id != empresa_id:
            return None
        return agenda
    
    def update_agenda(self, agenda_id: int, empresa_id: int, agenda_data: AgendaCreate) -> Optional[Agenda]:
        agenda = self.get_agenda(agenda_id, empresa_id)
        if not agenda:
            return None
        
        # Se for exceção, manter dia_semana como None
        if agenda_data.is_excecao:
            agenda_data.dia_semana = None
        
        # Verificar conflito com outra configuração
        if agenda_data.data_especifica:
            existing = self.agenda_repo.db.query(Agenda).filter(
                Agenda.empresa_id == empresa_id,
                Agenda.data_especifica == agenda_data.data_especifica,
                Agenda.id != agenda_id
            ).first()
        else:
            existing = self.agenda_repo.db.query(Agenda).filter(
                Agenda.empresa_id == empresa_id,
                Agenda.dia_semana == agenda_data.dia_semana,
                Agenda.data_especifica.is_(None),
                Agenda.id != agenda_id
            ).first()
        
        if existing:
            raise ValueError("Já existe uma configuração para este dia/data")
        
        return self.agenda_repo.update(
            agenda_id,
            dia_semana=agenda_data.dia_semana,
            data_especifica=agenda_data.data_especifica,
            hora_inicio=agenda_data.hora_inicio,
            hora_fim=agenda_data.hora_fim,
            intervalo_inicio=agenda_data.intervalo_inicio,
            intervalo_fim=agenda_data.intervalo_fim,
            is_excecao=agenda_data.is_excecao or False,
            atendente_id=agenda_data.atendente_id  # 👈 NOVO
        )
    
    def delete_agenda(self, agenda_id: int, empresa_id: int) -> bool:
        agenda = self.get_agenda(agenda_id, empresa_id)
        if not agenda:
            return False
        
        return self.agenda_repo.delete(agenda_id)
    
    def get_horarios_disponiveis(self, empresa_id: int, data: str, servico_id: int = None, atendente_id: int = None) -> List[str]:
        from datetime import datetime, timedelta
        
        data_obj = datetime.strptime(data, "%Y-%m-%d")
        data_date = data_obj.date()
        dia_semana = data_obj.weekday()
        
        # Buscar agenda do dia (prioriza exceção por data específica)
        agenda = self.agenda_repo.get_by_dia_semana(empresa_id, dia_semana, data_date, atendente_id)
        if not agenda:
            return []
        
        # Buscar agendamentos do dia (para o atendente específico)
        from app.repositories.agendamento_repository import AgendamentoRepository
        agendamento_repo = AgendamentoRepository(self.agenda_repo.db)
        
        if atendente_id:
            agendamentos = agendamento_repo.get_by_atendente_e_data(empresa_id, atendente_id, data_obj)
        else:
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
        
        # Configurar intervalo de almoço
        intervalo_inicio = None
        intervalo_fim = None
        if agenda.intervalo_inicio and agenda.intervalo_fim:
            intervalo_inicio = datetime.combine(data_obj.date(), agenda.intervalo_inicio)
            intervalo_fim = datetime.combine(data_obj.date(), agenda.intervalo_fim)
        
        while hora_atual + timedelta(minutes=duracao_padrao) <= hora_fim:
            # Verificar se está dentro do intervalo de almoço
            if intervalo_inicio and intervalo_fim:
                if intervalo_inicio <= hora_atual < intervalo_fim:
                    hora_atual = intervalo_fim
                    continue
            
            # Verificar conflito com agendamentos existentes
            conflito = False
            for agendamento in agendamentos:
                agendamento_fim = agendamento.data_hora + timedelta(minutes=agendamento.servico.duracao_minutos)
                if (hora_atual < agendamento_fim and 
                    hora_atual + timedelta(minutes=duracao_padrao) > agendamento.data_hora):
                    conflito = True
                    break
            
            if not conflito:
                horarios.append(hora_atual.strftime("%H:%M"))
            
            hora_atual += timedelta(minutes=30)
        
        return horarios