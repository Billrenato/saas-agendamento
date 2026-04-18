from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.agendamento_service import AgendamentoService
from app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse, AgendamentoStatusUpdate, StatusAgendamento
from app.api.v1.deps import get_current_empresa
from app.models.empresa import Empresa
from app.models.servico import Servico
from app.models.agendamento import Agendamento
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

# Router público (sem autenticação)
public_router = APIRouter(prefix="/public", tags=["Agendamentos Públicos"])

@public_router.get("/consultar")
def consultar_agendamentos_publico(
    telefone: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint público para cliente consultar seus agendamentos por telefone
    """
    from app.models.empresa import Empresa
    from app.models.servico import Servico
    from app.models.atendente import Atendente 
    
    telefone_limpo = ''.join(filter(str.isdigit, telefone))
    
    agendamentos = db.query(Agendamento).filter(
        Agendamento.telefone_cliente == telefone_limpo
    ).order_by(
        Agendamento.data_hora.desc()
    ).all()
    
    result = []
    for ag in agendamentos:
        empresa = db.query(Empresa).filter(Empresa.id == ag.empresa_id).first()
        servico = db.query(Servico).filter(Servico.id == ag.servico_id).first()
        
        # 👈 BUSCAR O NOME DO ATENDENTE CORRETAMENTE
        atendente_nome = None
        if ag.atendente_id:
            atendente = db.query(Atendente).filter(Atendente.id == ag.atendente_id).first()
            atendente_nome = atendente.nome if atendente else None
        
        result.append({
            "id": ag.id,
            "empresa_nome": empresa.nome if empresa else "",
            "servico_nome": servico.nome if servico else "",
            "atendente_nome": atendente_nome,  # 👈 AGORA ESTÁ DEFINIDO
            "data_hora": ag.data_hora.strftime("%d/%m/%Y às %H:%M"),
            "status": ag.status.value if hasattr(ag.status, 'value') else str(ag.status),
            "criado_em": ag.criado_em.strftime("%d/%m/%Y %H:%M") if ag.criado_em else ""
        })
    
    return {"agendamentos": result}