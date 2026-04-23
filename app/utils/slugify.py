import re
import unicodedata

def slugify(text: str) -> str:
    """
    Converte um texto em slug (formato amigável para URL)
    Ex: "Minha Empresa LTDA" -> "minha-empresa-ltda"
    """
    if not text:
        return ""
    
    # Normalizar caracteres especiais
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    # Converter para minúsculas
    text = text.lower()
    # Remover caracteres não alfanuméricos
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Remover hífens do início e fim
    text = text.strip('-')
    return text


def generate_unique_slug(db, model, nome: str, current_id: int = None) -> str:
    """Gera um slug único para a empresa"""
    base_slug = slugify(nome)
    slug = base_slug
    counter = 1
    
    while True:
        query = db.query(model).filter(model.slug == slug)
        if current_id:
            query = query.filter(model.id != current_id)
        
        if not query.first():
            return slug
        
        slug = f"{base_slug}-{counter}"
        counter += 1