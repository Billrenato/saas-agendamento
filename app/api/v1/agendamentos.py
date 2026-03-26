from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.agendamento_service import AgendamentoService
from app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse, AgendamentoStatusUpdate, StatusAgendamento
from app.api.deps import get_current_empresa
from app.models.empresa import Empresa
from typing import List

router = APIRouter()

# Endpoints públicos
@router.post("/", response_model=AgendamentoResponse, status_code=status.HTTP_201_CREATED)
def create_agendamento(
    agendamento_data: AgendamentoCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint público para criar um novo agendamento
    """
    agendamento_service = AgendamentoService(db)
    try:
        agendamento = agendamento_service.create_agendamento(agendamento_data)
        return agendamento
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Endpoints privados (empresa)
@router.get("/", response_model=List[AgendamentoResponse])
def list_agendamentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Lista todos os agendamentos da empresa autenticada
    """
    agendamento_service = AgendamentoService(db)
    agendamentos = agendamento_service.get_agendamentos_by_empresa(
        current_empresa.id, skip, limit
    )
    return agendamentos

@router.get("/{agendamento_id}", response_model=AgendamentoResponse)
def get_agendamento(
    agendamento_id: int,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Obtém detalhes de um agendamento específico
    """
    agendamento_service = AgendamentoService(db)
    agendamento = agendamento_service.get_agendamento(agendamento_id, current_empresa.id)
    
    if not agendamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
    
    return agendamento

@router.patch("/{agendamento_id}/status", response_model=AgendamentoResponse)
def update_agendamento_status(
    agendamento_id: int,
    status_update: AgendamentoStatusUpdate,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Atualiza o status de um agendamento (aceitar/recusar)
    """
    agendamento_service = AgendamentoService(db)
    agendamento = agendamento_service.update_status(
        agendamento_id, current_empresa.id, status_update.status
    )
    
    if not agendamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
    
    return agendamento