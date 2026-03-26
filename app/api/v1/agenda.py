from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.agenda_service import AgendaService
from app.schemas.agenda import AgendaCreate, AgendaResponse
from app.api.deps import get_current_empresa
from app.models.empresa import Empresa
from typing import List

router = APIRouter()

@router.get("/", response_model=List[AgendaResponse])
def list_agenda(
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Lista toda a agenda da empresa autenticada
    """
    agenda_service = AgendaService(db)
    agenda = agenda_service.get_agenda_by_empresa(current_empresa.id)
    return agenda

@router.post("/", response_model=AgendaResponse, status_code=status.HTTP_201_CREATED)
def create_agenda(
    agenda_data: AgendaCreate,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Cria um novo horário de funcionamento
    """
    agenda_service = AgendaService(db)
    try:
        agenda = agenda_service.create_agenda(current_empresa.id, agenda_data)
        return agenda
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{agenda_id}", response_model=AgendaResponse)
def get_agenda(
    agenda_id: int,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Obtém detalhes de um horário específico
    """
    agenda_service = AgendaService(db)
    agenda = agenda_service.get_agenda(agenda_id, current_empresa.id)
    
    if not agenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horário não encontrado"
        )
    
    return agenda

@router.put("/{agenda_id}", response_model=AgendaResponse)
def update_agenda(
    agenda_id: int,
    agenda_data: AgendaCreate,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Atualiza um horário de funcionamento
    """
    agenda_service = AgendaService(db)
    try:
        agenda = agenda_service.update_agenda(agenda_id, current_empresa.id, agenda_data)
        
        if not agenda:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Horário não encontrado"
            )
        
        return agenda
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{agenda_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agenda(
    agenda_id: int,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Remove um horário de funcionamento
    """
    agenda_service = AgendaService(db)
    deleted = agenda_service.delete_agenda(agenda_id, current_empresa.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horário não encontrado"
        )
    
    return None