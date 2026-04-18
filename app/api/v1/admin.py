from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.api.v1.deps import get_current_admin
from app.models.empresa import Empresa
from app.models.agendamento import Agendamento
from app.models.servico import Servico
from app.schemas.empresa import EmpresaCreate, EmpresaResponse, EmpresaUpdate

router = APIRouter(prefix="/admin", tags=["Administração"])

# ============================================
# DASHBOARD
# ============================================

@router.get("/dashboard")
def get_dashboard_stats(
    admin: Empresa = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Estatísticas do dashboard administrativo"""
    
    # Total de empresas
    total_empresas = db.query(Empresa).count()
    empresas_ativas = db.query(Empresa).filter(Empresa.ativo == True).count()
    empresas_inativas = total_empresas - empresas_ativas
    
    # Empresas cadastradas no último mês
    um_mes_atras = datetime.now() - timedelta(days=30)
    novas_empresas = db.query(Empresa).filter(
        Empresa.criado_em >= um_mes_atras
    ).count()
    
    # Total de agendamentos
    total_agendamentos = db.query(Agendamento).count()
    
    # Agendamentos por status
    pendentes = db.query(Agendamento).filter(Agendamento.status == "pendente").count()
    confirmados = db.query(Agendamento).filter(Agendamento.status == "aceito").count()
    
    # Total de serviços
    total_servicos = db.query(Servico).count()
    
    # Crescimento mensal (últimos 6 meses)
    crescimento = []
    for i in range(5, -1, -1):
        data_inicio = datetime.now() - timedelta(days=30 * (i + 1))
        data_fim = datetime.now() - timedelta(days=30 * i)
        count = db.query(Empresa).filter(
            Empresa.criado_em >= data_inicio,
            Empresa.criado_em < data_fim
        ).count()
        mes_nome = (data_fim - timedelta(days=15)).strftime("%b")
        crescimento.append({
            "mes": mes_nome,
            "empresas": count
        })
    
    return {
        "total_empresas": total_empresas,
        "empresas_ativas": empresas_ativas,
        "empresas_inativas": empresas_inativas,
        "novas_empresas": novas_empresas,
        "total_agendamentos": total_agendamentos,
        "agendamentos_pendentes": pendentes,
        "agendamentos_confirmados": confirmados,
        "total_servicos": total_servicos,
        "crescimento": crescimento
    }


# ============================================
# RELATÓRIOS
# ============================================

@router.get("/relatorios")
def get_relatorios(
    periodo: str = Query("30d", regex="^(7d|30d|90d)$"),
    admin: Empresa = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Gera relatórios detalhados da plataforma"""
    
    # Calcular data inicial baseada no período
    dias = 30
    if periodo == "7d":
        dias = 7
    elif periodo == "90d":
        dias = 90
    
    data_inicio = datetime.now() - timedelta(days=dias)
    
    # Total de agendamentos
    total_agendamentos = db.query(Agendamento).count()
    
    # Total de empresas
    total_empresas = db.query(Empresa).count()
    
    # Taxa de confirmação
    total_aceitos = db.query(Agendamento).filter(Agendamento.status == "aceito").count()
    taxa_confirmacao = round((total_aceitos / total_agendamentos * 100) if total_agendamentos > 0 else 0, 1)
    
    # Agendamentos por dia (últimos X dias)
    agendamentos_por_dia = []
    for i in range(dias, -1, -1):
        data = datetime.now() - timedelta(days=i)
        data_inicio_dia = datetime(data.year, data.month, data.day, 0, 0, 0)
        data_fim_dia = datetime(data.year, data.month, data.day, 23, 59, 59)
        
        count = db.query(Agendamento).filter(
            Agendamento.data_hora >= data_inicio_dia,
            Agendamento.data_hora <= data_fim_dia
        ).count()
        
        agendamentos_por_dia.append({
            "data": data.strftime("%Y-%m-%d"),
            "total": count
        })
    
    # Empresas por segmento
    segmentos_count = db.query(
        Empresa.segmento, 
        func.count(Empresa.id).label("total")
    ).filter(Empresa.segmento.isnot(None)).group_by(Empresa.segmento).all()
    
    empresas_por_segmento = [
        {"segmento": s[0] if s[0] else "Não informado", "total": s[1]} 
        for s in segmentos_count
    ]
    
    # Top 10 empresas com mais agendamentos
    top_empresas = db.query(
        Empresa.id, 
        Empresa.nome, 
        func.count(Agendamento.id).label("total")
    ).join(Agendamento, Agendamento.empresa_id == Empresa.id).group_by(Empresa.id).order_by(
        func.count(Agendamento.id).desc()
    ).limit(10).all()
    
    top_empresas_lista = [
        {"id": t[0], "nome": t[1], "total": t[2]} 
        for t in top_empresas
    ]
    
    # Agendamentos por status
    agendamentos_por_status = []
    for status_val in ["pendente", "aceito", "recusado"]:
        count = db.query(Agendamento).filter(Agendamento.status == status_val).count()
        agendamentos_por_status.append({"status": status_val, "total": count})
    
    return {
        "total_agendamentos": total_agendamentos,
        "total_empresas": total_empresas,
        "taxa_confirmacao": taxa_confirmacao,
        "agendamentos_por_dia": agendamentos_por_dia,
        "empresas_por_segmento": empresas_por_segmento,
        "top_empresas": top_empresas_lista,
        "agendamentos_por_status": agendamentos_por_status
    }


# ============================================
# AGENDAMENTOS (ADMIN)
# ============================================

@router.get("/agendamentos")
def listar_agendamentos_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    admin: Empresa = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Lista todos os agendamentos da plataforma com filtros"""
    query = db.query(Agendamento)
    
    # Filtro por busca (cliente, telefone ou empresa)
    if search:
        query = query.join(Empresa, Agendamento.empresa_id == Empresa.id).filter(
            (Agendamento.nome_cliente.ilike(f"%{search}%")) |
            (Agendamento.telefone_cliente.ilike(f"%{search}%")) |
            (Empresa.nome.ilike(f"%{search}%"))
        )
    
    # Filtro por status
    if status:
        query = query.filter(Agendamento.status == status)
    
    agendamentos = query.order_by(Agendamento.data_hora.desc()).offset(skip).limit(limit).all()
    
    result = []
    for ag in agendamentos:
        empresa = db.query(Empresa).filter(Empresa.id == ag.empresa_id).first()
        servico = db.query(Servico).filter(Servico.id == ag.servico_id).first()
        
        result.append({
            "id": ag.id,
            "nome_cliente": ag.nome_cliente,
            "telefone_cliente": ag.telefone_cliente,
            "data_hora": ag.data_hora,
            "status": ag.status.value if hasattr(ag.status, 'value') else str(ag.status),
            "servico_nome": servico.nome if servico else "Serviço não encontrado",
            "empresa_nome": empresa.nome if empresa else "Empresa não encontrada",
            "criado_em": ag.criado_em
        })
    
    return result


# ============================================
# CRUD EMPRESAS
# ============================================

@router.get("/empresas", response_model=List[EmpresaResponse])
def listar_empresas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    admin: Empresa = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Lista todas as empresas com filtros"""
    query = db.query(Empresa)
    
    # Filtro por busca (nome ou email)
    if search:
        query = query.filter(
            (Empresa.nome.ilike(f"%{search}%")) |
            (Empresa.email.ilike(f"%{search}%"))
        )
    
    # Filtro por status
    if status == "ativo":
        query = query.filter(Empresa.ativo == True)
    elif status == "inativo":
        query = query.filter(Empresa.ativo == False)
    
    return query.order_by(Empresa.id.desc()).offset(skip).limit(limit).all()


@router.get("/empresas/{empresa_id}", response_model=EmpresaResponse)
def get_empresa(
    empresa_id: int,
    admin: Empresa = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de uma empresa"""
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa


@router.post("/empresas", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def criar_empresa(
    data: EmpresaCreate,
    admin: Empresa = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Cria uma nova empresa (apenas admin)"""
    from app.core.security import get_password_hash
    
    # Verificar se email já existe
    existing = db.query(Empresa).filter(Empresa.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Criar empresa - APENAS COM CAMPOS QUE EXISTEM NO SCHEMA
    empresa = Empresa(
        nome=data.nome,
        email=data.email,
        senha_hash=get_password_hash(data.senha),
        telefone=data.telefone,
        segmento=getattr(data, 'segmento', None),
        endereco=getattr(data, 'endereco', None),
        cidade=getattr(data, 'cidade', None),
        estado=getattr(data, 'estado', None),
        cep=getattr(data, 'cep', None),
        descricao=getattr(data, 'descricao', None),
        #site=getattr(data, 'site', None),  # 👈 COMENTE OU REMOVA
        ativo=True
    )
    
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    
    return empresa


@router.put("/empresas/{empresa_id}", response_model=EmpresaResponse)
def atualizar_empresa(
    empresa_id: int,
    data: EmpresaUpdate,
    admin: Empresa = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Atualiza uma empresa"""
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    update_data = data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(empresa, field, value)
    
    db.commit()
    db.refresh(empresa)
    
    return empresa


@router.patch("/empresas/{empresa_id}/status")
def toggle_empresa_status(
    empresa_id: int,
    admin: Empresa = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Alterna o status da empresa (ativo/inativo)"""
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    empresa.ativo = not empresa.ativo
    db.commit()
    
    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "ativo": empresa.ativo,
        "message": f"Empresa {empresa.nome} {'ativada' if empresa.ativo else 'desativada'} com sucesso"
    }


@router.delete("/empresas/{empresa_id}")
def deletar_empresa(
    empresa_id: int,
    admin: Empresa = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Remove permanentemente uma empresa"""
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    db.delete(empresa)
    db.commit()
    
    return {"message": f"Empresa {empresa.nome} removida com sucesso"}