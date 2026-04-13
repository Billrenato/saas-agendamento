from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.empresa_service import EmpresaService
from app.schemas.empresa import EmpresaResponse
from app.api.deps import get_current_empresa
from app.models.empresa import Empresa


router = APIRouter()

@router.get("/{empresa_id}", response_model=EmpresaResponse)
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """
    Endpoint público para obter dados de uma empresa
    """
    empresa_service = EmpresaService(db)
    empresa = empresa_service.get_empresa(empresa_id)
    
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    return empresa

@router.get("/{empresa_id}/servicos")
def get_empresa_servicos(empresa_id: int, db: Session = Depends(get_db)):
    """
    Endpoint público para listar serviços de uma empresa
    """
    from app.services.servico_service import ServicoService
    
    servico_service = ServicoService(db)
    servicos = servico_service.get_servicos_by_empresa(empresa_id)
    
    return servicos

@router.get("/{empresa_id}/horarios-disponiveis")
def get_horarios_disponiveis(
    empresa_id: int,
    data: str,
    servico_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint público para obter horários disponíveis
    """
    from app.services.agenda_service import AgendaService
    
    agenda_service = AgendaService(db)
    horarios = agenda_service.get_horarios_disponiveis(empresa_id, data, servico_id)
    
    return {"horarios": horarios}



@router.get("/", response_model=List[EmpresaResponse])
def listar_empresas(
    skip: int = 0,
    limit: int = 100,
    segmento: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint público para listar todas as empresas ativas
    """
    query = db.query(Empresa).filter(Empresa.ativo == True)
    
    if segmento:
        query = query.filter(Empresa.segmento == segmento)
    
    empresas = query.offset(skip).limit(limit).all()
    return empresas

@router.get("/segmentos")
def listar_segmentos(
    db: Session = Depends(get_db)
):
    """
    Lista todos os segmentos disponíveis
    """
    segmentos = db.query(Empresa.segmento).filter(Empresa.segmento.isnot(None)).distinct().all()
    return [s[0] for s in segmentos if s[0]]