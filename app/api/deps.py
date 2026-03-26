from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.services.auth_service import AuthService
from app.models.empresa import Empresa

security = HTTPBearer()

def get_current_empresa(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Empresa:
    """Obtém a empresa autenticada a partir do token JWT"""
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    empresa_id = payload.get("sub")
    if not empresa_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    auth_service = AuthService(db)
    empresa = auth_service.get_empresa_by_id(int(empresa_id))
    
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Empresa não encontrada",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not empresa.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Empresa desativada"
        )
    
    return empresa