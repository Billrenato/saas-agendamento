from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1 import auth, empresas, servicos, agenda, agendamentos, atendentes, admin  # 👈 ADICIONOU admin
from app.api.v1.agendamentos import public_router 
import os

app = FastAPI(
    title="SaaS Agendamento API",
    description="API para sistema de agendamento de serviços",
    version="1.0.0",
    docs_url="/api/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Criar pasta de uploads se não existir
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/servicos", exist_ok=True)
os.makedirs("uploads/empresas", exist_ok=True)

# Servir arquivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ENVIRONMENT == "development" else settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticação"])
app.include_router(empresas.router, prefix="/api/v1/empresas", tags=["Empresas"])
app.include_router(servicos.router, prefix="/api/v1/servicos", tags=["Serviços"])
app.include_router(agenda.router, prefix="/api/v1/agenda", tags=["Agenda"])
app.include_router(agendamentos.router, prefix="/api/v1/agendamentos", tags=["Agendamentos"])
app.include_router(atendentes.router, prefix="/api/v1/atendentes", tags=["Atendentes"])
app.include_router(admin.router, prefix="/api/v1", tags=["Administração"])  # 👈 ADICIONOU
app.include_router(public_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "SaaS Agendamento API", "status": "online"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}