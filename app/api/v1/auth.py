from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import EmpresaRegister, EmpresaLogin, Token
from app.services.auth_service import AuthService
from app.api.v1.deps import get_current_empresa
from app.schemas.empresa import EmpresaResponse

router = APIRouter()

@router.post("/register", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def register(empresa_data: EmpresaRegister, db: Session = Depends(get_db)):
    """
    Registra uma nova empresa no sistema
    """
    try:
        auth_service = AuthService(db)
        empresa = auth_service.register(empresa_data)
        return empresa
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
def login(login_data: EmpresaLogin, db: Session = Depends(get_db)):
    """
    Realiza login da empresa e retorna token JWT
    """
    auth_service = AuthService(db)
    token = auth_service.login(login_data)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=EmpresaResponse)
def get_me(current_empresa: EmpresaResponse = Depends(get_current_empresa)):
    """
    Retorna dados da empresa autenticada
    """
    return current_empresa