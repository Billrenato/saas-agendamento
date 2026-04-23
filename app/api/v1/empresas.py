from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.empresa_service import EmpresaService
from app.schemas.empresa import EmpresaResponse, EmpresaCreate
from app.api.v1.deps import get_current_empresa
from app.models.empresa import Empresa
from app.repositories.empresa_repository import EmpresaRepository
import os
import uuid
import shutil
from app.services.cloudinary_service import CloudinaryService

router = APIRouter()

# Criar pastas de upload
os.makedirs("uploads/empresas", exist_ok=True)

@router.get("/{empresa_id}/agenda")
def get_empresa_agenda_publica(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint público para listar agenda da empresa
    """
    from app.models.agenda import Agenda
    
    agenda = db.query(Agenda).filter(
        Agenda.empresa_id == empresa_id,
        Agenda.data_especifica.is_(None)
    ).order_by(Agenda.dia_semana).all()
    
    return agenda

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
    atendente_id: int = None,  # ← ADICIONE ESTA LINHA
    db: Session = Depends(get_db)
):
    """
    Endpoint público para obter horários disponíveis
    """
    from app.services.agenda_service import AgendaService
    
    agenda_service = AgendaService(db)
    horarios = agenda_service.get_horarios_disponiveis(
        empresa_id, 
        data, 
        servico_id, 
        atendente_id  # ← PASSE O PARÂMETRO
    )
    
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
    
    # Se segmento for fornecido, filtra. Senão, mostra todas (incluindo sem segmento)
    if segmento:
        query = query.filter(Empresa.segmento == segmento)
    # Não adiciona filtro de segmento quando não tem segmento especificado
    
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

from app.schemas.empresa import EmpresaResponse, EmpresaCreate, EmpresaUpdate

@router.put("/me", response_model=EmpresaResponse)
def atualizar_empresa(
    empresa_data: EmpresaUpdate,  # ← MUDE PARA EmpresaUpdate
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados da empresa autenticada
    """
    try:
        # Limpa o telefone se veio
        if empresa_data.telefone:
            telefone_limpo = ''.join(filter(str.isdigit, empresa_data.telefone))
            current_empresa.telefone = telefone_limpo
        
        # Limpa o CEP se veio
        if empresa_data.cep:
            cep_limpo = ''.join(filter(str.isdigit, empresa_data.cep))
            current_empresa.cep = cep_limpo
        
        # Verificar se email já existe (se estiver mudando)
        if empresa_data.email and empresa_data.email != current_empresa.email:
            existing = db.query(Empresa).filter(Empresa.email == empresa_data.email).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado"
                )
        
        # Atualizar apenas os campos que vieram
        for key, value in empresa_data.dict(exclude_unset=True).items():
            if hasattr(current_empresa, key):
                setattr(current_empresa, key, value)
        
        db.commit()
        db.refresh(current_empresa)
        
        return current_empresa
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

    

@router.post("/me/upload-logo")
async def upload_logo(
    file: UploadFile = File(...),
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    # Validar se é imagem
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem")
    
    # Ler o conteúdo do arquivo
    contents = await file.read()
    
    # Upload para Cloudinary
    cloudinary_service = CloudinaryService()
    logo_url = await cloudinary_service.upload_image(
        contents, 
        f"empresas/{current_empresa.id}/logo"
    )
    
    # Salvar URL no banco
    current_empresa.logo = logo_url
    db.commit()
    
    return {"url": logo_url, "message": "Logo atualizada com sucesso!"}


@router.post("/me/upload-capa")
async def upload_capa(
    file: UploadFile = File(...),
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    # Validar se é imagem
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem")
    
    # Ler o conteúdo do arquivo
    contents = await file.read()
    
    # Upload para Cloudinary
    cloudinary_service = CloudinaryService()
    capa_url = await cloudinary_service.upload_image(
        contents, 
        f"empresas/{current_empresa.id}/capa"
    )
    
    # Salvar URL no banco
    current_empresa.foto_capa = capa_url
    db.commit()
    
    return {"url": capa_url, "message": "Capa atualizada com sucesso!"}

@router.delete("/me/logo")
def remover_logo(
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """Remove a logo da empresa"""
    # Só remove a referência no banco (Cloudinary gerencia o arquivo)
    current_empresa.logo = None
    db.commit()
    
    return {"message": "Logo removida"}

@router.delete("/me/capa")
def remover_capa(
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """Remove a foto de capa da empresa"""
    # Só remove a referência no banco (Cloudinary gerencia o arquivo)
    current_empresa.foto_capa = None
    db.commit()
    
    return {"message": "Capa removida"}

@router.put("/me/whatsapp")
def update_whatsapp(
    data: dict,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """Salva as credenciais do WhatsApp"""
    current_empresa.twilio_account_sid = data.get('twilio_account_sid')
    current_empresa.twilio_auth_token = data.get('twilio_auth_token')
    current_empresa.twilio_whatsapp_number = data.get('twilio_whatsapp_number')
    db.commit()
    return {"message": "WhatsApp configurado"}

@router.get("/me/whatsapp")
def get_whatsapp(
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """Retorna as configurações de WhatsApp da empresa"""
    return {
        "twilio_account_sid": current_empresa.twilio_account_sid,
        "twilio_auth_token": current_empresa.twilio_auth_token,
        "twilio_whatsapp_number": current_empresa.twilio_whatsapp_number
    }

@router.post("/me/whatsapp/test")
def test_whatsapp(
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """Testa a conexão com Twilio"""
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
    """Atualiza as mensagens personalizadas"""
    current_empresa.whatsapp_confirmation_message = data.get('whatsapp_confirmation_message')
    current_empresa.whatsapp_welcome_message = data.get('whatsapp_welcome_message')
    current_empresa.whatsapp_cancel_message = data.get('whatsapp_cancel_message')
    db.commit()
    return {"message": "Mensagens atualizadas"}


@router.get("/slug/{slug}", response_model=EmpresaResponse)
def get_empresa_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint público para obter dados de uma empresa pelo slug (nome amigável)
    """
    empresa_service = EmpresaService(db)
    empresa = empresa_service.get_empresa_by_slug(slug)
    
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    return empresa



from app.schemas.empresa import EmpresaCreate, EmpresaUpdate, EmpresaResponse
from app.utils.slugify import generate_unique_slug
from app.core.security import hash_password  # ou sua função de hash

# ============================================
# ENDPOINTS DE CRIAÇÃO E ATUALIZAÇÃO (ADMIN)
# ============================================

@router.post("/", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def create_empresa(
    empresa_data: EmpresaCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova empresa (endpoint admin)
    """
    # Verificar se email já existe
    existing = db.query(Empresa).filter(Empresa.email == empresa_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Criar nova empresa
    nova_empresa = Empresa(
        nome=empresa_data.nome,
        email=empresa_data.email,
        senha_hash=hash_password(empresa_data.senha),
        telefone=empresa_data.telefone,
        segmento=empresa_data.segmento,
        endereco=empresa_data.endereco,
        cidade=empresa_data.cidade,
        estado=empresa_data.estado,
        cep=empresa_data.cep,
        descricao=empresa_data.descricao,
        ativo=True
    )
    
    db.add(nova_empresa)
    db.flush()  # Para obter o ID
    
    # 🔥 GERAR SLUG AUTOMATICAMENTE
    nova_empresa.slug = generate_unique_slug(db, Empresa, empresa_data.nome)
    
    db.commit()
    db.refresh(nova_empresa)
    
    return nova_empresa


@router.put("/{empresa_id}", response_model=EmpresaResponse)
def update_empresa_admin(
    empresa_id: int,
    empresa_data: EmpresaUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza uma empresa (endpoint admin)
    """
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    # Se o nome foi alterado, atualizar o slug
    nome_alterado = empresa_data.nome and empresa_data.nome != empresa.nome
    
    # Atualizar campos
    for key, value in empresa_data.dict(exclude_unset=True).items():
        if hasattr(empresa, key) and value is not None:
            setattr(empresa, key, value)
    
    # Atualizar slug se o nome mudou
    if nome_alterado:
        empresa.slug = generate_unique_slug(db, Empresa, empresa_data.nome, empresa_id)
    
    db.commit()
    db.refresh(empresa)
    
    return empresa



