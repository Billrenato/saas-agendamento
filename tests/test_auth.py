import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.empresa import Empresa

def test_register(client: TestClient, db_session: Session):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "nome": "Empresa Teste",
            "email": "teste@empresa.com",
            "senha": "senha123",
            "telefone": "11999999999"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Empresa Teste"
    assert data["email"] == "teste@empresa.com"

def test_register_duplicate_email(client: TestClient, db_session: Session):
    # Criar primeira empresa
    empresa = Empresa(
        nome="Empresa Teste",
        email="teste@empresa.com",
        senha_hash=get_password_hash("senha123"),
        telefone="11999999999"
    )
    db_session.add(empresa)
    db_session.commit()
    
    # Tentar criar com mesmo email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "nome": "Outra Empresa",
            "email": "teste@empresa.com",
            "senha": "senha123",
            "telefone": "11999999999"
        }
    )
    
    assert response.status_code == 400
    assert "Email já cadastrado" in response.json()["detail"]

def test_login(client: TestClient, db_session: Session):
    # Criar empresa
    empresa = Empresa(
        nome="Empresa Teste",
        email="login@teste.com",
        senha_hash=get_password_hash("senha123"),
        telefone="11999999999"
    )
    db_session.add(empresa)
    db_session.commit()
    
    # Fazer login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@teste.com",
            "senha": "senha123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient, db_session: Session):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "naoexiste@teste.com",
            "senha": "senhaerrada"
        }
    )
    
    assert response.status_code == 401
    assert "Email ou senha incorretos" in response.json()["detail"]