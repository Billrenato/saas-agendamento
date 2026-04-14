from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.servico_service import ServicoService
from app.schemas.servico import ServicoCreate, ServicoResponse
from app.api.deps import get_current_empresa
from app.models.empresa import Empresa
from app.models.servico import Servico
from typing import List
from fastapi import UploadFile, File
import shutil
import uuid
import os
from fastapi import UploadFile, File
import shutil
import uuid
import os
from app.core.config import settings

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
    Remove um serviço permanentemente (apenas se não tiver agendamentos)
    """
    servico_service = ServicoService(db)
    
    # Verificar se existem agendamentos para este serviço
    from app.models.agendamento import Agendamento
    agendamentos_count = db.query(Agendamento).filter(
        Agendamento.servico_id == servico_id,
        Agendamento.empresa_id == current_empresa.id,
        Agendamento.status.in_(['pendente', 'aceito'])
    ).count()
    
    if agendamentos_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível excluir este serviço. Existem {agendamentos_count} agendamentos pendentes ou confirmados. Desative o serviço ao invés de excluir."
        )
    
    deleted = servico_service.delete_servico(servico_id, current_empresa.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    return None

@router.patch("/{servico_id}/desativar")
def desativar_servico(
    servico_id: int,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Desativa um serviço (não aparece mais para clientes, mas mantém histórico)
    """
    servico = db.query(Servico).filter(
        Servico.id == servico_id,
        Servico.empresa_id == current_empresa.id
    ).first()
    
    if not servico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    servico.ativo = False
    db.commit()
    
    return {"message": "Serviço desativado com sucesso", "servico_id": servico_id}

@router.patch("/{servico_id}/reativar")
def reativar_servico(
    servico_id: int,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """
    Reativa um serviço desativado
    """
    servico = db.query(Servico).filter(
        Servico.id == servico_id,
        Servico.empresa_id == current_empresa.id
    ).first()
    
    if not servico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    servico.ativo = True
    db.commit()
    
    return {"message": "Serviço reativado com sucesso", "servico_id": servico_id}

# Criar pasta se não existir
os.makedirs("uploads/servicos", exist_ok=True)

@router.post("/{servico_id}/upload-imagem")
async def upload_imagem_servico(
    servico_id: int,
    file: UploadFile = File(...),
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    # Verificar se serviço existe
    servico = db.query(Servico).filter(
        Servico.id == servico_id,
        Servico.empresa_id == current_empresa.id
    ).first()
    
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    # Validar tipo
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem")
    
    # Criar pasta
    os.makedirs("uploads/servicos", exist_ok=True)
    
    # Gerar nome único
    extensao = file.filename.split('.')[-1]
    nome_arquivo = f"servico_{servico_id}_{uuid.uuid4()}.{extensao}"
    caminho_arquivo = f"uploads/servicos/{nome_arquivo}"
    
    # Salvar arquivo
    with open(caminho_arquivo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    url_imagem = f"http://localhost:8000/uploads/servicos/{nome_arquivo}"
    
    # SALVAR NO BANCO
    servico.imagem = url_imagem
    db.commit()
    db.refresh(servico)  # ← ADICIONE ESTA LINHA
    
    print(f"DEBUG: Serviço ID: {servico_id}")
    print(f"DEBUG: URL salva: {url_imagem}")
    print(f"DEBUG: Serviço após commit: {servico.imagem}")
    
    return {"url": url_imagem, "message": "Imagem enviada com sucesso"}

@router.delete("/{servico_id}/remover-imagem")
def remover_imagem_servico(
    servico_id: int,
    current_empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    """Remove a imagem do serviço"""
    
    servico = db.query(Servico).filter(
        Servico.id == servico_id,
        Servico.empresa_id == current_empresa.id
    ).first()
    
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    # Remover arquivo do disco
    if servico.imagem and servico.imagem.startswith('/uploads/'):
        caminho_arquivo = servico.imagem[1:]
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
    
    servico.imagem = None
    db.commit()
    
    return {"message": "Imagem removida com sucesso"}

