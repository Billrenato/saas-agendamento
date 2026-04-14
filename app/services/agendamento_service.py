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
        
        # Enviar mensagem de boas-vindas
        empresa = self.empresa_repo.get(servico.empresa_id)
        
        print(f"\n=== ENVIANDO BOAS-VINDAS ===")
        print(f"Empresa ID: {servico.empresa_id}")
        print(f"Tem Twilio? {bool(empresa.twilio_account_sid)}")
        print(f"Telefone: {agendamento_data.telefone_cliente}")
        
        # Só precisa ter Twilio configurado (mensagem pode ser padrão)
        if empresa.twilio_account_sid and empresa.twilio_auth_token:
            print("✅ Condições OK, enviando...")
            
            from app.services.whatsapp_service import WhatsAppService
            
            # Usa mensagem da empresa ou mensagem padrão
            if empresa.whatsapp_welcome_message:
                mensagem = empresa.whatsapp_welcome_message
            else:
                # Mensagem padrão
                mensagem = f"""👋 Olá {agendamento_data.nome_cliente}!

    Recebemos sua solicitação de agendamento na {empresa.nome}.

    📋 Serviço: {servico.nome}
    📅 Data: {agendamento_data.data_hora.strftime('%d/%m/%Y')}
    ⏰ Horário: {agendamento_data.data_hora.strftime('%H:%M')}

    ✅ Em breve confirmaremos seu horário.
    🔍 Você pode acompanhar o status em "Meus Agendamentos" no nosso site.

    Agradecemos a preferência!"""
            
            # Substituir variáveis
            mensagem = mensagem.replace('{cliente_nome}', agendamento_data.nome_cliente)
            mensagem = mensagem.replace('{empresa_nome}', empresa.nome)
            mensagem = mensagem.replace('{servico_nome}', servico.nome)
            mensagem = mensagem.replace('{data}', agendamento_data.data_hora.strftime('%d/%m/%Y'))
            mensagem = mensagem.replace('{horario}', agendamento_data.data_hora.strftime('%H:%M'))
            
            sucesso, resultado = WhatsAppService.send_message(
                account_sid=empresa.twilio_account_sid,
                auth_token=empresa.twilio_auth_token,
                from_number=empresa.twilio_whatsapp_number,
                to_number=agendamento_data.telefone_cliente,
                message=mensagem
            )
            
            if sucesso:
                print(f"✅ WhatsApp enviado! SID: {resultado}")
            else:
                print(f"❌ Erro: {resultado}")
        else:
            print("❌ WhatsApp não configurado na empresa")
        
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
            print("❌ Agendamento não encontrado")
            return None
        
        agendamento = self.agendamento_repo.update(agendamento_id, status=status)
        
        
        empresa = self.empresa_repo.get(empresa_id)
        servico = self.servico_repo.get(agendamento.servico_id)
        
        if not empresa.twilio_account_sid or not empresa.twilio_auth_token:
            print("❌ Empresa não configurou WhatsApp")
            return agendamento
        
        from app.services.whatsapp_service import WhatsAppService
        
        # Monta endereço completo
        endereco_completo = ""
        if empresa.endereco:
            endereco_completo = f"\n📍 {empresa.endereco}"
            if empresa.cidade:
                endereco_completo += f", {empresa.cidade}"
            if empresa.estado:
                endereco_completo += f"-{empresa.estado}"
        
        # Mensagem para ACEITO
        if status == StatusAgendamento.ACEITO:
            print("\n📱 Tentando enviar WhatsApp de confirmação...")
            
            if empresa.whatsapp_confirmation_message:
                mensagem = empresa.whatsapp_confirmation_message
            else:
                mensagem = f"""✅ Agendamento confirmado!

    👤 Cliente: {agendamento.nome_cliente}
    ✂️ Serviço: {servico.nome}
    📅 Data: {agendamento.data_hora.strftime('%d/%m/%Y')}
    ⏰ Horário: {agendamento.data_hora.strftime('%H:%M')}
    🏢 Empresa: {empresa.nome}{endereco_completo}

    Qualquer dúvida, entre em contato conosco pelo WhatsApp: {empresa.telefone}"""
        
        # Mensagem para RECUSADO
        elif status == StatusAgendamento.RECUSADO:
            print("\n📱 Tentando enviar WhatsApp de cancelamento...")
            
            if empresa.whatsapp_cancel_message:
                mensagem = empresa.whatsapp_cancel_message
            else:
                mensagem = f"""❌ Agendamento recusado!

    👤 Cliente: {agendamento.nome_cliente}
    ✂️ Serviço: {servico.nome}
    📅 Data: {agendamento.data_hora.strftime('%d/%m/%Y')}
    ⏰ Horário: {agendamento.data_hora.strftime('%H:%M')}
    🏢 Empresa: {empresa.nome}{endereco_completo}

    Infelizmente não foi possível confirmar seu agendamento.
    Entre em contato conosco pelo WhatsApp: {empresa.telefone}

    Desculpe pelo transtorno."""
        else:
            return agendamento
        
        # Substituir variáveis
        mensagem = mensagem.replace('{cliente_nome}', agendamento.nome_cliente)
        mensagem = mensagem.replace('{servico_nome}', servico.nome)
        mensagem = mensagem.replace('{data}', agendamento.data_hora.strftime('%d/%m/%Y'))
        mensagem = mensagem.replace('{horario}', agendamento.data_hora.strftime('%H:%M'))
        mensagem = mensagem.replace('{empresa_nome}', empresa.nome)
        mensagem = mensagem.replace('{endereco}', endereco_completo)
        mensagem = mensagem.replace('{empresa_telefone}', empresa.telefone)
        
        print(f"Enviando para: {agendamento.telefone_cliente}")
        print(f"Mensagem: {mensagem}")
        
        sucesso, resultado = WhatsAppService.send_message(
            account_sid=empresa.twilio_account_sid,
            auth_token=empresa.twilio_auth_token,
            from_number=empresa.twilio_whatsapp_number,
            to_number=agendamento.telefone_cliente,
            message=mensagem
        )
        
        if sucesso:
            print(f"✅ WhatsApp enviado com sucesso! SID: {resultado}")
        else:
            print(f"❌ Erro ao enviar WhatsApp: {resultado}")
        
        return agendamento