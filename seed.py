"""
Script para popular o banco de dados com dados iniciais
"""
from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.models.empresa import Empresa
from app.models.servico import Servico
from app.models.agenda import Agenda
from app.core.security import get_password_hash
from datetime import time

def seed():
    db = SessionLocal()
    
    try:
        # Verificar se já existem dados
        if db.query(Empresa).count() > 0:
            print("Banco de dados já possui dados. Seed ignorado.")
            return
        
        print("Criando dados iniciais...")
        
        # Criar empresa exemplo
        empresa = Empresa(
            nome="Salão Beleza Total",
            email="contato@belezatotal.com",
            senha_hash=get_password_hash("senha123"),
            telefone="5511999999999",
            ativo=True
        )
        db.add(empresa)
        db.flush()
        
        # Criar serviços
        servicos = [
            Servico(
                empresa_id=empresa.id,
                nome="Corte de Cabelo",
                descricao="Corte masculino e feminino",
                duracao_minutos=30,
                preco=50.00
            ),
            Servico(
                empresa_id=empresa.id,
                nome="Manicure",
                descricao="Unhas das mãos",
                duracao_minutos=45,
                preco=35.00
            ),
            Servico(
                empresa_id=empresa.id,
                nome="Pedicure",
                descricao="Unhas dos pés",
                duracao_minutos=45,
                preco=40.00
            ),
            Servico(
                empresa_id=empresa.id,
                nome="Maquiagem",
                descricao="Maquiagem profissional",
                duracao_minutos=60,
                preco=80.00
            )
        ]
        
        for servico in servicos:
            db.add(servico)
        
        # Criar agenda (Segunda a Sexta)
        dias_semana = [
            (0, "Segunda"),
            (1, "Terça"),
            (2, "Quarta"),
            (3, "Quinta"),
            (4, "Sexta")
        ]
        
        for dia, nome in dias_semana:
            agenda = Agenda(
                empresa_id=empresa.id,
                dia_semana=dia,
                hora_inicio=time(9, 0),  # 09:00
                hora_fim=time(18, 0)     # 18:00
            )
            db.add(agenda)
        
        # Sábado
        agenda_sabado = Agenda(
            empresa_id=empresa.id,
            dia_semana=5,
            hora_inicio=time(9, 0),
            hora_fim=time(14, 0)
        )
        db.add(agenda_sabado)
        
        db.commit()
        
        print(f"Seed concluído! Empresa ID: {empresa.id}")
        print(f"Email: {empresa.email}")
        print(f"Senha: senha123")
        
    except Exception as e:
        print(f"Erro ao executar seed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()