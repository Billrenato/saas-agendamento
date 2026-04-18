# app/api/v1/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.empresa import Empresa
from app.core.security import decode_token

security = HTTPBearer()

# 👇 COLOQUE SEU EMAIL REAL AQUI
ADMIN_EMAILS = [
    "renatojrmathias94@gmail.com",  # SEU EMAIL
]

# app/api/v1/deps.py

def get_current_empresa(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Empresa:
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 👇 Tenta buscar por ID ou por email
    empresa = None
    if sub.isdigit():
        empresa = db.query(Empresa).filter(Empresa.id == int(sub)).first()
    else:
        empresa = db.query(Empresa).filter(Empresa.email == sub).first()
    
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Empresa não encontrada",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return empresa

def get_current_admin(
    current_empresa: Empresa = Depends(get_current_empresa)
) -> Empresa:
    """Verifica se a empresa autenticada é administrador"""
    if current_empresa.email not in ADMIN_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return current_empresa