from sqlalchemy.orm import Session
from app.repositories.empresa_repository import EmpresaRepository
from app.schemas.auth import EmpresaRegister, EmpresaLogin
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.empresa import Empresa
from typing import Optional

class AuthService:
    def __init__(self, db: Session):
        self.empresa_repo = EmpresaRepository(db)
    
    def register(self, empresa_data: EmpresaRegister) -> Empresa:
        # Verificar se email já existe
        existing = self.empresa_repo.get_by_email(empresa_data.email)
        if existing:
            raise ValueError("Email já cadastrado")
        
        # Criar empresa
        empresa = self.empresa_repo.create(
            nome=empresa_data.nome,
            email=empresa_data.email,
            senha_hash=get_password_hash(empresa_data.senha),
            telefone=empresa_data.telefone
        )
        
        return empresa
    
    def login(self, login_data: EmpresaLogin) -> Optional[str]:
        empresa = self.empresa_repo.get_by_email(login_data.email)
        if not empresa:
            return None
        
        if not verify_password(login_data.senha, empresa.senha_hash):
            return None
        
        # Criar token
        access_token = create_access_token(data={"sub": str(empresa.id)})
        return access_token
    
    def get_empresa_by_id(self, empresa_id: int) -> Optional[Empresa]:
        return self.empresa_repo.get(empresa_id)