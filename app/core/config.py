from pydantic_settings import BaseSettings
from typing import Optional, List, Union
import json

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_WHATSAPP_NUMBER: Optional[str] = None
    
    # WhatsApp Cloud API
    WHATSAPP_ACCESS_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None
    WHATSAPP_BUSINESS_ACCOUNT_ID: Optional[str] = None
    
    ENVIRONMENT: str = "development"
    ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Converter ALLOWED_ORIGINS para lista se for string
        if isinstance(self.ALLOWED_ORIGINS, str):
            try:
                self.ALLOWED_ORIGINS = json.loads(self.ALLOWED_ORIGINS)
            except:
                self.ALLOWED_ORIGINS = [self.ALLOWED_ORIGINS]

settings = Settings()