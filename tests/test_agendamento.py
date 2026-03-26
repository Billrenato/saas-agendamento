import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.empresa import Empresa
from app.models.servico import Servico
from app.core.security import get_password_hash
from app.core.database import Base

def test_create_agendamento_publico(client: TestClient, db_session: Session):
    # Criar empresa
    empresa = Empresa(
        nome="Empresa Teste",
        email="teste@empresa.com",
        senha_hash=get_password_hash("senha123"),
        telefone="11999999999"
    )
    db_session.add(empresa)
    db_session.flush()
    
    # Criar serviço
    servico = Servico(
        empresa_id=empresa.id,
        nome="Corte de Cabelo",
        duracao_minutos=30,
        preco=50.00
    )
    db_session.add(servico)
    db_session.commit()
    
    # Criar agendamento
    data_hora = datetime.now() + timedelta(days=1)
    data_hora = data_hora.replace(hour=10, minute=0, second=0, microsecond=0)
    
    response = client.post(
        "/api/v1/agendamentos/",
        json={
            "nome_cliente": "Cliente Teste",
            "telefone_cliente": "11988888888",
            "data_hora": data_hora.isoformat(),
            "servico_id": servico.id
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome_cliente"] == "Cliente Teste"
    assert data["status"] == "pendente"

def test_create_agendamento_horario_conflito(client: TestClient, db_session: Session):
    # Criar empresa e serviço
    empresa = Empresa(
        nome="Empresa Teste",
        email="conflito@empresa.com",
        senha_hash=get_password_hash("senha123"),
        telefone="11999999999"
    )
    db_session.add(empresa)
    db_session.flush()
    
    servico = Servico(
        empresa_id=empresa.id,
        nome="Corte de Cabelo",
        duracao_minutos=30,
        preco=50.00
    )
    db_session.add(servico)
    db_session.commit()
    
    data_hora = datetime.now() + timedelta(days=1)
    data_hora = data_hora.replace(hour=10, minute=0, second=0, microsecond=0)
    
    # Primeiro agendamento
    response1 = client.post(
        "/api/v1/agendamentos/",
        json={
            "nome_cliente": "Cliente 1",
            "telefone_cliente": "11988888881",
            "data_hora": data_hora.isoformat(),
            "servico_id": servico.id
        }
    )
    assert response1.status_code == 201
    
    # Segundo agendamento no mesmo horário
    response2 = client.post(
        "/api/v1/agendamentos/",
        json={
            "nome_cliente": "Cliente 2",
            "telefone_cliente": "11988888882",
            "data_hora": data_hora.isoformat(),
            "servico_id": servico.id
        }
    )
    
    assert response2.status_code == 400
    assert "Horário já ocupado" in response2.json()["detail"]