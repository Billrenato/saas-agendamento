from app.core.database import SessionLocal
from app.models.servico import Servico

db = SessionLocal()

# Busca um serviço específico que você sabe que tem imagem (ID 56)
servico = db.query(Servico).filter(Servico.id == 56).first()

if servico:
    print(f"ID: {servico.id}")
    print(f"Nome: {servico.nome}")
    print(f"Imagem: {servico.imagem}")
    print(f"Tipo do campo imagem: {type(servico.imagem)}")
else:
    print("Serviço não encontrado")

db.close()