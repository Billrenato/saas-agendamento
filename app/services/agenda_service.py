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
    
    # app/services/agenda_service.py - SUBSTITUA O MÉTODO get_horarios_disponiveis

    def get_horarios_disponiveis(self, empresa_id: int, data: str, servico_id: int = None, atendente_id: int = None) -> List[str]:
        from datetime import datetime, timedelta
        
        print(f"🔍 [INICIO] Buscando horários para empresa {empresa_id}, data {data}, atendente_id {atendente_id}")
        
        data_obj = datetime.strptime(data, "%Y-%m-%d")
        data_date = data_obj.date()
        dia_semana = data_obj.weekday()
        
        print(f"🔍 [1] Data: {data_date}, dia_semana: {dia_semana}")
        
        # Buscar agendas do dia
        agendas = self.agenda_repo.get_by_dia_semana(empresa_id, dia_semana, data_date, atendente_id)
        
        if not agendas:
            print(f"⚠️ [2] NENHUMA agenda encontrada para {data_date}")
            return []
        
        print(f"✅ [3] Encontradas {len(agendas)} agenda(s)")
        
        # Buscar agendamentos do dia
        from app.repositories.agendamento_repository import AgendamentoRepository
        agendamento_repo = AgendamentoRepository(self.agenda_repo.db)
        
        if atendente_id:
            agendamentos = agendamento_repo.get_by_atendente_e_data(empresa_id, atendente_id, data_obj)
            print(f"📅 [4] Encontrados {len(agendamentos)} agendamentos para atendente {atendente_id}")
        else:
            agendamentos = agendamento_repo.get_by_data(empresa_id, data_obj)
            print(f"📅 [4] Encontrados {len(agendamentos)} agendamentos totais")
        
        # Obter duração do serviço
        duracao_servico = 30  # padrão
        if servico_id:
            from app.repositories.servico_repository import ServicoRepository
            servico_repo = ServicoRepository(self.agenda_repo.db)
            servico = servico_repo.get(servico_id)
            if servico:
                duracao_servico = servico.duracao_minutos
                print(f"⏱️ [5] Duração do serviço: {duracao_servico} min")
        
        # Criar lista de intervalos ocupados (considerando duração do serviço)
        intervalos_ocupados = []
        for ag in agendamentos:
            inicio = ag.data_hora
            fim = inicio + timedelta(minutes=ag.servico.duracao_minutos if hasattr(ag, 'servico') and ag.servico else duracao_servico)
            intervalos_ocupados.append((inicio, fim))
            print(f"   - Ocupado: {inicio.strftime('%H:%M')} até {fim.strftime('%H:%M')}")
        
        # Gerar horários disponíveis
        todos_horarios = []
        TEMPO_ENTRE_AGENDAMENTOS = 15  # minutos de intervalo entre atendimentos
        
        for agenda in agendas:
            print(f"📋 Processando agenda: ID={agenda.id}, inicio={agenda.hora_inicio}, fim={agenda.hora_fim}")
            
            hora_atual = datetime.combine(data_obj.date(), agenda.hora_inicio)
            hora_fim = datetime.combine(data_obj.date(), agenda.hora_fim)
            
            # Intervalo de almoço
            intervalo_inicio = None
            intervalo_fim = None
            if agenda.intervalo_inicio and agenda.intervalo_fim:
                intervalo_inicio = datetime.combine(data_obj.date(), agenda.intervalo_inicio)
                intervalo_fim = datetime.combine(data_obj.date(), agenda.intervalo_fim)
                print(f"🍽️ [6] Intervalo de almoço: {intervalo_inicio.strftime('%H:%M')} - {intervalo_fim.strftime('%H:%M')}")
            
            print(f"⏰ [7] Gerando horários entre {hora_atual.strftime('%H:%M')} e {hora_fim.strftime('%H:%M')}")
            
            # Gerar horários a cada 30 minutos (independente da duração do serviço)
            while hora_atual + timedelta(minutes=duracao_servico) <= hora_fim:
                hora_fim_servico = hora_atual + timedelta(minutes=duracao_servico)
                
                # Verificar intervalo de almoço
                if intervalo_inicio and intervalo_fim:
                    # Se o horário começa antes do intervalo e termina dentro ou depois
                    if hora_atual < intervalo_fim and hora_fim_servico > intervalo_inicio:
                        # Pular para o fim do intervalo
                        hora_atual = intervalo_fim
                        continue
                
                # Verificar se o horário está ocupado
                conflito = False
                for inicio_ocupado, fim_ocupado in intervalos_ocupados:
                    # Verifica se há sobreposição
                    if not (hora_fim_servico <= inicio_ocupado or hora_atual >= fim_ocupado):
                        conflito = True
                        break
                
                if not conflito:
                    todos_horarios.append(hora_atual.strftime("%H:%M"))
                
                # Avançar para o próximo horário (a cada 30 minutos, não baseado na duração do serviço)
                hora_atual += timedelta(minutes=30)
            
            # Se ainda temos tempo no final do expediente, verificar último horário
            # (já foi verificado no loop)
        
        # Remover duplicatas e ordenar
        todos_horarios = sorted(list(set(todos_horarios)))
        
        print(f"🎉 [8] TOTAL de horários disponíveis: {len(todos_horarios)}")
        print(f"📋 Horários: {todos_horarios}")
        
        return todos_horarios