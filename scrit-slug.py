# scrit-slug.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar TODOS os models na ordem correta
from app.core.database import SessionLocal
from app.models.empresa import Empresa
from app.models.atendente import Atendente
from app.models.servico import Servico
from app.models.atendente_servico import AtendenteServico  # ← SE EXISTIR
from app.models.agenda import Agenda
from app.models.agendamento import Agendamento
from app.utils.slugify import generate_unique_slug

def update_existing_slugs():
    db = SessionLocal()
    try:
        empresas = db.query(Empresa).filter(Empresa.slug.is_(None)).all()
        
        for empresa in empresas:
            slug = generate_unique_slug(db, Empresa, empresa.nome)
            empresa.slug = slug
            print(f"✅ {empresa.nome} -> {slug}")
        
        db.commit()
        print(f"\n🎉 {len(empresas)} empresas atualizadas!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_existing_slugs()