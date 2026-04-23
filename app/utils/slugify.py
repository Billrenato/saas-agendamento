import re
import unicodedata
from sqlalchemy.orm import Session

def slugify(text: str) -> str:
    """
    Converte um texto em slug (formato amigável para URL)
    Ex: "Minha Empresa LTDA" -> "minha-empresa-ltda"
    """
    if not text:
        return ""
    
    # Normalizar caracteres especiais (á, é, í, ó, ú, ç, etc.)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    
    # Converter para minúsculas
    text = text.lower()
    
    # Remover caracteres não alfanuméricos (exceto espaços e hífens)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    
    # Substituir espaços e múltiplos hífens por um único hífen
    text = re.sub(r'[\s-]+', '-', text)
    
    # Remover hífens do início e fim
    text = text.strip('-')
    
    return text


def generate_unique_slug(db: Session, model, nome: str, current_id: int = None) -> str:
    """Gera um slug único para a empresa"""
    base_slug = slugify(nome)
    slug = base_slug
    counter = 1
    
    while True:
        # Verificar se o slug já existe
        query = db.query(model).filter(model.slug == slug)
        if current_id:
            query = query.filter(model.id != current_id)
        
        if not query.first():
            return slug
        
        # Se existe, adicionar número
        slug = f"{base_slug}-{counter}"
        counter += 1