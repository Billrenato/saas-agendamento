# app/services/whatsapp_service.py
from twilio.rest import Client
from typing import Tuple, Optional

class WhatsAppService:
    """Serviço para envio de mensagens WhatsApp via Twilio"""
    
    @staticmethod
    def send_message(
        account_sid: str, 
        auth_token: str, 
        from_number: str, 
        to_number: str, 
        message: str
    ) -> Tuple[bool, str]:
        """
        Envia uma mensagem WhatsApp usando as credenciais da empresa
        """
        try:
            # --- Formatação do FROM_NUMBER (Remetente - Sandbox) ---
            # IMPORTANTE: O número do Sandbox deve ser usado EXATAMENTE como está no banco.
            # Não adicione ou remova códigos de país.
            from_number_full = from_number
            if not from_number_full.startswith('whatsapp:'):
                from_number_full = f'whatsapp:{from_number_full}'

            # --- Formatação do TO_NUMBER (Destinatário - Cliente) ---
            # 1. Remove tudo que não é dígito
            to_number_clean = ''.join(filter(str.isdigit, to_number))
            
            # 2. Garante o código do país 55 para o Brasil
            if not to_number_clean.startswith('55'):
                to_number_clean = '55' + to_number_clean
                
            # 3. Formata para o Twilio
            to_number_full = f'whatsapp:+{to_number_clean}'
            
            print(f"📱 Enviando mensagem...")
            print(f"   From: {from_number_full}") # Deve imprimir "whatsapp:+14155238886"
            print(f"   To: {to_number_full}")
            
            # Inicializa cliente Twilio
            client = Client(account_sid, auth_token)
            
            # Envia mensagem
            msg = client.messages.create(
                body=message,
                from_=from_number_full,
                to=to_number_full
            )
            
            print(f"✅ Mensagem enviada! SID: {msg.sid}")
            return True, msg.sid
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False, str(e)
    
    @staticmethod
    def send_confirmation(
        empresa,
        cliente_nome: str,
        servico_nome: str,
        data: str,
        horario: str,
        telefone_cliente: str
    ) -> Tuple[bool, str]:
        """
        Envia mensagem de confirmação de agendamento usando as configurações da empresa
        
        Args:
            empresa: Objeto Empresa (com as credenciais e mensagens)
            cliente_nome: Nome do cliente
            servico_nome: Nome do serviço
            data: Data do agendamento (DD/MM/YYYY)
            horario: Horário do agendamento (HH:MM)
            telefone_cliente: Telefone do cliente
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem_ou_erro)
        """
        # Verifica se empresa tem WhatsApp configurado
        if not empresa.twilio_account_sid or not empresa.twilio_auth_token:
            return False, "WhatsApp não configurado na empresa"
        
        # Usa mensagem personalizada ou padrão
        if empresa.whatsapp_confirmation_message:
            mensagem = empresa.whatsapp_confirmation_message
            mensagem = mensagem.replace('{cliente_nome}', cliente_nome)
            mensagem = mensagem.replace('{servico_nome}', servico_nome)
            mensagem = mensagem.replace('{data}', data)
            mensagem = mensagem.replace('{horario}', horario)
            mensagem = mensagem.replace('{empresa_nome}', empresa.nome)
        else:
            mensagem = f"""✅ Agendamento confirmado!

📋 Serviço: {servico_nome}
📅 Data: {data}
⏰ Horário: {horario}
🏢 Empresa: {empresa.nome}

Qualquer dúvida, entre em contato conosco."""
        
        # Envia a mensagem
        return WhatsAppService.send_message(
            account_sid=empresa.twilio_account_sid,
            auth_token=empresa.twilio_auth_token,
            from_number=empresa.twilio_whatsapp_number,
            to_number=telefone_cliente,
            message=mensagem
        )
    
    @staticmethod
    def send_welcome(
        empresa,
        cliente_nome: str,
        telefone_cliente: str
    ) -> Tuple[bool, str]:
        """
        Envia mensagem de boas-vindas para novo cliente
        """
        if not empresa.twilio_account_sid or not empresa.twilio_auth_token:
            return False, "WhatsApp não configurado na empresa"
        
        if empresa.whatsapp_welcome_message:
            mensagem = empresa.whatsapp_welcome_message
            mensagem = mensagem.replace('{cliente_nome}', cliente_nome)
            mensagem = mensagem.replace('{empresa_nome}', empresa.nome)
        else:
            mensagem = f"""👋 Olá {cliente_nome}!

Bem-vindo(a) à {empresa.nome}! 

Você receberá notificações de agendamento por aqui.
Qualquer dúvida, estamos à disposição."""
        
        return WhatsAppService.send_message(
            account_sid=empresa.twilio_account_sid,
            auth_token=empresa.twilio_auth_token,
            from_number=empresa.twilio_whatsapp_number,
            to_number=telefone_cliente,
            message=mensagem
        )
    
    @staticmethod
    def send_reminder(
        empresa,
        cliente_nome: str,
        servico_nome: str,
        data: str,
        horario: str,
        telefone_cliente: str
    ) -> Tuple[bool, str]:
        """
        Envia mensagem de lembrete antes do agendamento
        """
        if not empresa.twilio_account_sid or not empresa.twilio_auth_token:
            return False, "WhatsApp não configurado na empresa"
        
        if empresa.whatsapp_reminder_message:
            mensagem = empresa.whatsapp_reminder_message
            mensagem = mensagem.replace('{cliente_nome}', cliente_nome)
            mensagem = mensagem.replace('{servico_nome}', servico_nome)
            mensagem = mensagem.replace('{data}', data)
            mensagem = mensagem.replace('{horario}', horario)
            mensagem = mensagem.replace('{empresa_nome}', empresa.nome)
        else:
            mensagem = f"""🔔 Lembrete!

Seu agendamento está chegando:

📋 Serviço: {servico_nome}
📅 Data: {data}
⏰ Horário: {horario}
🏢 Empresa: {empresa.nome}

Confirme sua presença ou remaneje se necessário."""
        
        return WhatsAppService.send_message(
            account_sid=empresa.twilio_account_sid,
            auth_token=empresa.twilio_auth_token,
            from_number=empresa.twilio_whatsapp_number,
            to_number=telefone_cliente,
            message=mensagem
        )
    
    @staticmethod
    def send_cancel(
        empresa,
        cliente_nome: str,
        servico_nome: str,
        data: str,
        horario: str,
        telefone_cliente: str
    ) -> Tuple[bool, str]:
        """
        Envia mensagem de cancelamento do agendamento
        """
        if not empresa.twilio_account_sid or not empresa.twilio_auth_token:
            return False, "WhatsApp não configurado na empresa"
        
        if empresa.whatsapp_cancel_message:
            mensagem = empresa.whatsapp_cancel_message
            mensagem = mensagem.replace('{cliente_nome}', cliente_nome)
            mensagem = mensagem.replace('{servico_nome}', servico_nome)
            mensagem = mensagem.replace('{data}', data)
            mensagem = mensagem.replace('{horario}', horario)
            mensagem = mensagem.replace('{empresa_nome}', empresa.nome)
        else:
            mensagem = f"""❌ Agendamento cancelado!

📋 Serviço: {servico_nome}
📅 Data: {data}
⏰ Horário: {horario}
🏢 Empresa: {empresa.nome}

Para reagendar, entre em contato conosco."""
        
        return WhatsAppService.send_message(
            account_sid=empresa.twilio_account_sid,
            auth_token=empresa.twilio_auth_token,
            from_number=empresa.twilio_whatsapp_number,
            to_number=telefone_cliente,
            message=mensagem
        )
    
    @staticmethod
    def test_connection(account_sid: str, auth_token: str) -> Tuple[bool, str]:
        """
        Testa se as credenciais da Twilio são válidas
        """
        try:
            client = Client(account_sid, auth_token)
            # Tenta buscar informações da conta para validar
            client.api.accounts(account_sid).fetch()
            return True, "Conexão OK"
        except Exception as e:
            return False, str(e)