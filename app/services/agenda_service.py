# app/services/agenda_service.py
from sqlalchemy.orm import Session
from app.repositories.agenda_repository import AgendaRepository
from app.schemas.agenda import AgendaCreate
from app.models.agenda import Agenda
from typing import List, Optional
from datetime import date
import logging

logger = logging.getLogger(__name__)

class AgendaService:
    def __init__(self, db: Session):
        self.agenda_repo = AgendaRepository(db)
    
    def create_agenda(self, empresa_id: int, agenda_data: AgendaCreate) -> Agenda:
        # Se for exceção (data específica), dia_semana deve ser None
        if agenda_data.is_excecao:
            agenda_data.dia_semana = None
        
        # Verificar se já existe configuração para este dia/data E atendente
        if agenda_data.data_especifica:
            # Buscar por data específica e atendente
            existing = self.agenda_repo.db.query(Agenda).filter(
                Agenda.empresa_id == empresa_id,
                Agenda.data_especifica == agenda_data.data_especifica,
                Agenda.atendente_id == agenda_data.atendente_id
            ).first()
        else:
            # Buscar por dia da semana e atendente
            existing = self.agenda_repo.db.query(Agenda).filter(
                Agenda.empresa_id == empresa_id,
                Agenda.dia_semana == agenda_data.dia_semana,
                Agenda.data_especifica.is_(None),
                Agenda.atendente_id == agenda_data.atendente_id
            ).first()
        
        if existing:
            raise ValueError("Já existe uma configuração para este dia/data para este atendente")
        
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
            atendente_id=agenda_data.atendente_id
        )
    
    def get_agenda_by_empresa(self, empresa_id: int) -> List[Agenda]:
        return self.agenda_repo.get_by_empresa(empresa_id)
    
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
        
        # Verificar conflito com outra configuração (considerando atendente)
        if agenda_data.data_especifica:
            existing = self.agenda_repo.db.query(Agenda).filter(
                Agenda.empresa_id == empresa_id,
                Agenda.data_especifica == agenda_data.data_especifica,
                Agenda.atendente_id == agenda_data.atendente_id,
                Agenda.id != agenda_id
            ).first()
        else:
            existing = self.agenda_repo.db.query(Agenda).filter(
                Agenda.empresa_id == empresa_id,
                Agenda.dia_semana == agenda_data.dia_semana,
                Agenda.data_especifica.is_(None),
                Agenda.atendente_id == agenda_data.atendente_id,
                Agenda.id != agenda_id
            ).first()
        
        if existing:
            raise ValueError("Já existe uma configuração para este dia/data para este atendente")
        
        return self.agenda_repo.update(
            agenda_id,
            dia_semana=agenda_data.dia_semana,
            data_especifica=agenda_data.data_especifica,
            hora_inicio=agenda_data.hora_inicio,
            hora_fim=agenda_data.hora_fim,
            intervalo_inicio=agenda_data.intervalo_inicio,
            intervalo_fim=agenda_data.intervalo_fim,
            is_excecao=agenda_data.is_excecao or False,
            atendente_id=agenda_data.atendente_id
        )
    
    def delete_agenda(self, agenda_id: int, empresa_id: int) -> bool:
        agenda = self.get_agenda(agenda_id, empresa_id)
        if not agenda:
            return False
        
        return self.agenda_repo.delete(agenda_id)
    
    def get_horarios_disponiveis(self, empresa_id: int, data: str, servico_id: int = None, atendente_id: int = None) -> List[str]:
        from datetime import datetime, timedelta
        from app.repositories.servico_repository import ServicoRepository
        from app.repositories.agendamento_repository import AgendamentoRepository
        
        # 1. Parsing da Data
        try:
            data_obj = datetime.strptime(data, "%Y-%m-%d")
            data_date = data_obj.date()
            logger.info(f"🔍 Data recebida: {data}, parseada: {data_date}")
        except ValueError as e:
            logger.error(f"❌ Erro ao parsear data {data}: {e}")
            return []
        
        dia_semana = data_obj.weekday()
        logger.info(f"🔍 Dia da semana: {dia_semana}")
        
        # 2. Buscar agenda do dia
        agenda = self.agenda_repo.get_by_dia_semana(empresa_id, dia_semana, data_date, atendente_id)
        
        if not agenda:
            logger.warning(f"⚠️ Nenhuma agenda encontrada para {data_date}")
            return []
        
        logger.info(f"✅ Agenda encontrada: ID={agenda.id}, hora_inicio={agenda.hora_inicio}, hora_fim={agenda.hora_fim}")
        
        # 3. Definir duração do serviço
        duracao_minutos = 30
        if servico_id:
            servico_repo = ServicoRepository(self.agenda_repo.db)
            servico = servico_repo.get(servico_id)
            if servico and servico.duracao_minutos:
                duracao_minutos = servico.duracao_minutos
                logger.info(f"✅ Serviço duração: {duracao_minutos} minutos")
        
        # 4. Buscar agendamentos do dia
        agendamento_repo = AgendamentoRepository(self.agenda_repo.db)
        
        if atendente_id:
            agendamentos = agendamento_repo.get_by_atendente_e_data(empresa_id, atendente_id, data_obj)
            logger.info(f"📅 Encontrados {len(agendamentos)} agendamentos para o atendente {atendente_id}")
        else:
            agendamentos = agendamento_repo.get_by_data(empresa_id, data_obj)
            logger.info(f"📅 Encontrados {len(agendamentos)} agendamentos totais")
        
        # 5. Gerar horários disponíveis
        horarios = []
        hora_atual = datetime.combine(data_date, agenda.hora_inicio)
        hora_fim = datetime.combine(data_date, agenda.hora_fim)
        
        intervalo_inicio = None
        intervalo_fim = None
        if agenda.intervalo_inicio and agenda.intervalo_fim:
            intervalo_inicio = datetime.combine(data_date, agenda.intervalo_inicio)
            intervalo_fim = datetime.combine(data_date, agenda.intervalo_fim)
            logger.info(f"🍽️ Intervalo: {intervalo_inicio} - {intervalo_fim}")
        
        while hora_atual + timedelta(minutes=duracao_minutos) <= hora_fim:
            # Verificar intervalo de almoço
            if intervalo_inicio and intervalo_fim and intervalo_inicio <= hora_atual < intervalo_fim:
                hora_atual = intervalo_fim
                continue
            
            # Verificar conflitos
            conflito = False
            for agendamento in agendamentos:
                ag_fim = agendamento.data_hora + timedelta(minutes=agendamento.servico.duracao_minutos)
                if (hora_atual < ag_fim and hora_atual + timedelta(minutes=duracao_minutos) > agendamento.data_hora):
                    conflito = True
                    break
            
            if not conflito:
                horarios.append(hora_atual.strftime("%H:%M"))
            
            hora_atual += timedelta(minutes=30)
        
        logger.info(f"🎉 Total de horários disponíveis: {len(horarios)}")
        return horarios