import re
from datetime import datetime, time
from typing import Optional

def validate_phone(phone: str) -> bool:
    """
    Valida número de telefone brasileiro
    Formatos aceitos:
    - (11) 99999-9999
    - 11999999999
    - +5511999999999
    """
    # Remove caracteres não numéricos
    phone = re.sub(r'\D', '', phone)
    
    # Verifica tamanho (DDD + 8 ou 9 dígitos)
    if len(phone) not in [10, 11, 13]:  # 13 com +55
        return False
    
    # Remove código do país se presente
    if phone.startswith('55') and len(phone) == 13:
        phone = phone[2:]
    
    # Verifica se tem DDD válido (11 a 99)
    if len(phone) >= 2:
        ddd = int(phone[:2])
        if ddd < 11 or ddd > 99:
            return False
    
    return True

def validate_email(email: str) -> bool:
    """
    Valida formato de email
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_time_range(start_time: time, end_time: time) -> bool:
    """
    Valida se horário de início é menor que horário de fim
    """
    return start_time < end_time

def validate_weekday(weekday: int) -> bool:
    """
    Valida se o dia da semana é válido (0-6)
    """
    return 0 <= weekday <= 6

def validate_future_date(date: datetime) -> bool:
    """
    Valida se a data é futura
    """
    return date > datetime.now()

def validate_business_hours(
    date: datetime,
    start_time: time,
    end_time: time
) -> bool:
    """
    Valida se o horário está dentro do expediente
    """
    time_only = date.time()
    return start_time <= time_only <= end_time