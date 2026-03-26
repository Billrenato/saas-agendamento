from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.servico_service import ServicoService
from app.schemas.servico import ServicoCreate, ServicoResponse
from app.api.deps import get_current_empresa
from app.models.empresa import Empresa
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ServicoResponse])
def list_servicos(
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Lista todos os serviços da empresa autenticada
    """
    servico_service = ServicoService(db)
    servicos = servico_service.get_servicos_by_empresa(current_empresa.id)
    return servicos

@router.post("/", response_model=ServicoResponse, status_code=status.HTTP_201_CREATED)
def create_servico(
    servico_data: ServicoCreate,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Cria um novo serviço para a empresa autenticada
    """
    servico_service = ServicoService(db)
    servico = servico_service.create_servico(current_empresa.id, servico_data)
    return servico

@router.get("/{servico_id}", response_model=ServicoResponse)
def get_servico(
    servico_id: int,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Obtém detalhes de um serviço específico
    """
    servico_service = ServicoService(db)
    servico = servico_service.get_servico(servico_id, current_empresa.id)
    
    if not servico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    return servico

@router.put("/{servico_id}", response_model=ServicoResponse)
def update_servico(
    servico_id: int,
    servico_data: ServicoCreate,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Atualiza um serviço existente
    """
    servico_service = ServicoService(db)
    servico = servico_service.update_servico(servico_id, current_empresa.id, servico_data)
    
    if not servico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    return servico

@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_servico(
    servico_id: int,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Remove um serviço
    """
    servico_service = ServicoService(db)
    deleted = servico_service.delete_servico(servico_id, current_empresa.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    return None