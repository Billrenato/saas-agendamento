from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.v1.deps import get_current_empresa
from app.models.empresa import Empresa
from app.services.atendente_service import AtendenteService
from app.schemas.atendente import AtendenteCreate, AtendenteUpdate, AtendenteResponse

router = APIRouter()

@router.get("/", response_model=List[AtendenteResponse])
def list_atendentes(
    apenas_ativos: bool = Query(True),
    empresa_id: Optional[int] = Query(None, description="ID da empresa para filtrar atendentes"),
    db: Session = Depends(get_db)
):
    """
    Lista atendentes (público - não precisa de autenticação)
    Se empresa_id for informado, retorna apenas os atendentes daquela empresa
    """
    from app.services.atendente_service import AtendenteService
    
    if not empresa_id:
        return []
    
    service = AtendenteService(db)
    atendentes = service.get_atendentes_by_empresa(empresa_id, com_servicos=True)
    
    # Converter para resposta com serviços
    result = []
    for a in atendentes:
        a_dict = {
            "id": a.id,
            "empresa_id": a.empresa_id,
            "nome": a.nome,
            "email": a.email,
            "telefone": a.telefone,
            "foto": a.foto,
            "ativo": a.ativo,
            "ordem_exibicao": a.ordem_exibicao,
            "criado_em": a.criado_em,
            "servicos": [{"id": s.id, "nome": s.nome} for s in getattr(a, 'servicos_list', [])]
        }
        result.append(a_dict)
    
    if apenas_ativos:
        result = [a for a in result if a.get("ativo", True)]
    
    return result

@router.post("/", response_model=AtendenteResponse, status_code=status.HTTP_201_CREATED)
def create_atendente(
    data: AtendenteCreate,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """Cria um novo atendente"""
    service = AtendenteService(db)
    try:
        atendente = service.create_atendente(current_empresa.id, data)
        
        # Buscar serviços para retornar
        from app.repositories.servico_repository import ServicoRepository
        servico_repo = ServicoRepository(db)
        servicos = [servico_repo.get(sid) for sid in data.servico_ids if servico_repo.get(sid)]
        
        return {
            "id": atendente.id,
            "empresa_id": atendente.empresa_id,
            "nome": atendente.nome,
            "email": atendente.email,
            "telefone": atendente.telefone,
            "foto": atendente.foto,
            "ativo": atendente.ativo,
            "ordem_exibicao": atendente.ordem_exibicao,
            "criado_em": atendente.criado_em,
            "servicos": [{"id": s.id, "nome": s.nome} for s in servicos if s]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{atendente_id}", response_model=AtendenteResponse)
def get_atendente(
    atendente_id: int,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um atendente específico"""
    service = AtendenteService(db)
    atendente = service.get_atendente(atendente_id, current_empresa.id)
    
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente não encontrado")
    
    # Buscar serviços
    from app.repositories.servico_repository import ServicoRepository
    servico_repo = ServicoRepository(db)
    servico_ids = service.get_servicos_do_atendente(atendente_id, current_empresa.id)
    servicos = [servico_repo.get(sid) for sid in servico_ids if servico_repo.get(sid)]
    
    return {
        "id": atendente.id,
        "empresa_id": atendente.empresa_id,
        "nome": atendente.nome,
        "email": atendente.email,
        "telefone": atendente.telefone,
        "foto": atendente.foto,
        "ativo": atendente.ativo,
        "ordem_exibicao": atendente.ordem_exibicao,
        "criado_em": atendente.criado_em,
        "servicos": [{"id": s.id, "nome": s.nome} for s in servicos if s]
    }

@router.put("/{atendente_id}", response_model=AtendenteResponse)
def update_atendente(
    atendente_id: int,
    data: AtendenteUpdate,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """Atualiza um atendente"""
    service = AtendenteService(db)
    atendente = service.update_atendente(atendente_id, current_empresa.id, data)
    
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente não encontrado")
    
    # Buscar serviços
    from app.repositories.servico_repository import ServicoRepository
    servico_repo = ServicoRepository(db)
    servico_ids = service.get_servicos_do_atendente(atendente_id, current_empresa.id)
    servicos = [servico_repo.get(sid) for sid in servico_ids if servico_repo.get(sid)]
    
    return {
        "id": atendente.id,
        "empresa_id": atendente.empresa_id,
        "nome": atendente.nome,
        "email": atendente.email,
        "telefone": atendente.telefone,
        "foto": atendente.foto,
        "ativo": atendente.ativo,
        "ordem_exibicao": atendente.ordem_exibicao,
        "criado_em": atendente.criado_em,
        "servicos": [{"id": s.id, "nome": s.nome} for s in servicos if s]
    }

@router.delete("/{atendente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_atendente(
    atendente_id: int,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """Remove (desativa) um atendente"""
    service = AtendenteService(db)
    result = service.delete_atendente(atendente_id, current_empresa.id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Atendente não encontrado")