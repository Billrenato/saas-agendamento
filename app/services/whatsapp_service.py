from app.core.config import settings
import httpx
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.use_twilio = settings.TWILIO_ACCOUNT_SID is not None
        self.use_cloud_api = settings.WHATSAPP_ACCESS_TOKEN is not None
        
        if self.use_twilio:
            try:
                self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                logger.info("WhatsApp service initialized with Twilio")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                self.use_twilio = False
        elif self.use_cloud_api:
            self.cloud_api_url = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
            logger.info("WhatsApp service initialized with WhatsApp Cloud API")
        else:
            logger.warning("No WhatsApp service configured. Messages will be logged only.")
    
    def send_message(self, to: str, message: str, empresa_telefone: Optional[str] = None) -> bool:
        """
        Envia mensagem via WhatsApp
        Args:
            to: Número do destinatário (formato: +5511999999999)
            message: Conteúdo da mensagem
            empresa_telefone: Telefone da empresa (usado para Twilio)
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        # Formatar número
        to = self._format_phone_number(to)
        
        if self.use_twilio:
            return self._send_twilio(to, message, empresa_telefone)
        elif self.use_cloud_api:
            return self._send_cloud_api(to, message)
        else:
            # Modo desenvolvimento: apenas log
            logger.info(f"[WHATSAPP MOCK] Para: {to} | Mensagem: {message}")
            return True
    
    def _format_phone_number(self, phone: str) -> str:
        """Formata número de telefone para o padrão internacional"""
        # Remove espaços e caracteres especiais
        phone = ''.join(filter(str.isdigit, phone))
        
        # Se não começar com código do país, assume Brasil (+55)
        if len(phone) == 11 and phone.startswith('9'):  # 9xxxxxxxxx
            phone = '55' + phone
        elif len(phone) == 10:  # 8 dígitos + DDD
            phone = '55' + phone
        
        return f"+{phone}"
    
    def _send_twilio(self, to: str, message: str, from_number: Optional[str] = None) -> bool:
        """Envia mensagem usando Twilio"""
        try:
            # Usar número da empresa se fornecido, senão usar número padrão
            from_whatsapp = from_number or settings.TWILIO_WHATSAPP_NUMBER
            
            if not from_whatsapp:
                logger.error("No WhatsApp number configured for Twilio")
                return False
            
            # Garantir que o número tem o formato correto
            if not from_whatsapp.startswith('whatsapp:'):
                from_whatsapp = f"whatsapp:{from_whatsapp}"
            
            if not to.startswith('whatsapp:'):
                to = f"whatsapp:{to}"
            
            # Enviar mensagem
            twilio_message = self.twilio_client.messages.create(
                body=message,
                from_=from_whatsapp,
                to=to
            )
            
            logger.info(f"Message sent via Twilio: SID={twilio_message.sid}")
            return True
            
        except TwilioRestException as e:
            logger.error(f"Twilio error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending WhatsApp via Twilio: {e}")
            return False
    
    def _send_cloud_api(self, to: str, message: str) -> bool:
        """Envia mensagem usando WhatsApp Cloud API"""
        try:
            headers = {
                "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "text",
                "text": {
                    "preview_url": False,
                    "body": message
                }
            }
            
            with httpx.Client() as client:
                response = client.post(
                    self.cloud_api_url,
                    json=payload,
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Message sent via WhatsApp Cloud API: {response.json()}")
                    return True
                else:
                    logger.error(f"WhatsApp Cloud API error: {response.status_code} - {response.text}")
                    return False
                    
        except httpx.TimeoutException:
            logger.error("Timeout sending WhatsApp message")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending WhatsApp via Cloud API: {e}")
            return False
    
    def send_template_message(self, to: str, template_name: str, components: list, empresa_telefone: Optional[str] = None) -> bool:
        """
        Envia mensagem usando template (apenas para Twilio ou Cloud API)
        """
        if self.use_twilio:
            return self._send_twilio_template(to, template_name, components, empresa_telefone)
        elif self.use_cloud_api:
            return self._send_cloud_template(to, template_name, components)
        else:
            logger.info(f"[WHATSAPP TEMPLATE MOCK] Para: {to} | Template: {template_name}")
            return True
    
    def _send_twilio_template(self, to: str, template_name: str, components: list, from_number: Optional[str] = None) -> bool:
        """Envia template via Twilio"""
        try:
            from_whatsapp = from_number or settings.TWILIO_WHATSAPP_NUMBER
            
            if not from_whatsapp:
                logger.error("No WhatsApp number configured for Twilio")
                return False
            
            if not from_whatsapp.startswith('whatsapp:'):
                from_whatsapp = f"whatsapp:{from_whatsapp}"
            
            if not to.startswith('whatsapp:'):
                to = f"whatsapp:{to}"
            
            # Twilio requer configuração específica para templates
            # Este é um exemplo básico - ajuste conforme necessidade
            message = self.twilio_client.messages.create(
                content_sid=template_name,
                from_=from_whatsapp,
                to=to,
                content_variables=components
            )
            
            logger.info(f"Template message sent via Twilio: SID={message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending template via Twilio: {e}")
            return False
    
    def _send_cloud_template(self, to: str, template_name: str, components: list) -> bool:
        """Envia template via WhatsApp Cloud API"""
        try:
            headers = {
                "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": "pt_BR"
                    },
                    "components": components
                }
            }
            
            with httpx.Client() as client:
                response = client.post(
                    self.cloud_api_url,
                    json=payload,
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Template sent via WhatsApp Cloud API")
                    return True
                else:
                    logger.error(f"WhatsApp Cloud API template error: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error sending template via Cloud API: {e}")
            return False