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



@router.put("/me", response_model=EmpresaResponse)
def atualizar_empresa(
    empresa_data: EmpresaCreate,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados da empresa autenticada
    """
    empresa_repo = EmpresaRepository(db)
    
    # Verificar se email já existe (se estiver mudando)
    if empresa_data.email != current_empresa.email:
        existing = empresa_repo.get_by_email(empresa_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
    
    # Atualizar campos
    for key, value in empresa_data.dict(exclude_unset=True).items():
        if key != 'senha':
            setattr(current_empresa, key, value)
    
    db.commit()
    db.refresh(current_empresa)
    
    return current_empresa

@router.patch("/me/logo")
def upload_logo(
    logo_url: str,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Atualiza a logo da empresa
    """
    current_empresa.logo = logo_url
    db.commit()
    return {"logo": logo_url}

@router.patch("/me/capa")
def upload_capa(
    capa_url: str,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Atualiza a foto de capa da empresa
    """
    current_empresa.foto_capa = capa_url
    db.commit()
    return {"foto_capa": capa_url}

# app/api/v1/empresas.py

# 1. Salvar credenciais (você já tem)
@router.put("/me/whatsapp")
def update_whatsapp(
    data: dict,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    current_empresa.twilio_account_sid = data.get('twilio_account_sid')
    current_empresa.twilio_auth_token = data.get('twilio_auth_token')
    current_empresa.twilio_whatsapp_number = data.get('twilio_whatsapp_number')
    db.commit()
    return {"message": "WhatsApp configurado"}

# 2. Buscar credenciais (para mostrar no frontend)
@router.get("/me/whatsapp")
def get_whatsapp(
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Retorna as configurações de WhatsApp da empresa
    """
    return {
        "twilio_account_sid": current_empresa.twilio_account_sid,
        "twilio_auth_token": current_empresa.twilio_auth_token,
        "twilio_whatsapp_number": current_empresa.twilio_whatsapp_number
    }

# 3. Testar conexão (você já deve ter)
@router.post("/me/whatsapp/test")
def test_whatsapp(
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    from app.services.whatsapp_service import WhatsAppService
    
    if not current_empresa.twilio_account_sid:
        raise HTTPException(status_code=400, detail="Credenciais não configuradas")
    
    success, message = WhatsAppService.test_connection(
        account_sid=current_empresa.twilio_account_sid,
        auth_token=current_empresa.twilio_auth_token
    )
    
    if not success:
        raise HTTPException(status_code=401, detail=message)
    
    return {"success": True, "message": "Conexão bem sucedida!"}


@router.put("/me/whatsapp-messages")
def update_whatsapp_messages(
    data: dict,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    current_empresa.send_reminder_hours = data.get('send_reminder_hours', 24)
    current_empresa.whatsapp_confirmation_message = data.get('whatsapp_confirmation_message')
    current_empresa.whatsapp_reminder_message = data.get('whatsapp_reminder_message')
    current_empresa.whatsapp_welcome_message = data.get('whatsapp_welcome_message')
    current_empresa.whatsapp_cancel_message = data.get('whatsapp_cancel_message')
    db.commit()
    return {"message": "Mensagens atualizadas"}