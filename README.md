# SaaS Agendamento - Backend

API completa para sistema de agendamento de serviços (beleza, dentistas, médicos, etc).

## 🚀 Tecnologias

- **Python 3.11**
- **FastAPI** - Framework web
- **PostgreSQL** - Banco de dados
- **SQLAlchemy** - ORM
- **Alembic** - Migrações
- **JWT** - Autenticação
- **Twilio/WhatsApp Cloud API** - Integração WhatsApp

## 📋 Funcionalidades

### Cliente (Sem Login)
- Visualizar serviços disponíveis
- Visualizar horários disponíveis
- Agendar serviços

### Empresa (Com Login)
- Cadastro e autenticação
- CRUD de serviços
- Configuração de agenda (horários de funcionamento)
- Gerenciamento de agendamentos
- Confirmação/recusa de agendamentos
- Envio automático de confirmação via WhatsApp

## 🏗️ Estrutura do Projeto
saas-agendamento/
├── app/
│ ├── api/ # Rotas/endpoints
│ ├── core/ # Configurações, database, security
│ ├── models/ # Modelos SQLAlchemy
│ ├── repositories/ # Camada de acesso a dados
│ ├── schemas/ # Schemas Pydantic
│ ├── services/ # Lógica de negócio
│ └── utils/ # Utilitários
├── alembic/ # Migrações
├── tests/ # Testes
├── docker-compose.yml
├── Dockerfile
└── requirements.txt

text

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11 (opcional, para execução local)

### Com Docker

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd saas-agendamento
Configure as variáveis de ambiente:

bash
cp .env.example .env
# Edite .env com suas configurações
Execute com Docker Compose:

bash
docker-compose up -d
Acesse a documentação:

Swagger: http://localhost:8000/api/docs

Redoc: http://localhost:8000/api/redoc

Local (sem Docker)
Crie um ambiente virtual:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
Instale as dependências:

bash
pip install -r requirements.txt
Configure o banco de dados:

bash
# Edite .env com sua DATABASE_URL
cp .env.example .env
Execute as migrações:

bash
alembic upgrade head
Popule o banco com dados iniciais:

bash
python seed.py
Execute a aplicação:

bash
uvicorn app.main:app --reload
📡 Endpoints Principais
Públicos
GET /api/v1/empresas/{id} - Dados da empresa

GET /api/v1/empresas/{id}/servicos - Serviços disponíveis

GET /api/v1/empresas/{id}/horarios-disponiveis?data=YYYY-MM-DD - Horários livres

POST /api/v1/agendamentos - Criar agendamento

Privados (Requer Token)
POST /api/v1/auth/register - Cadastro

POST /api/v1/auth/login - Login

GET /api/v1/auth/me - Dados da empresa

GET /api/v1/servicos - Listar serviços

POST /api/v1/servicos - Criar serviço

PUT /api/v1/servicos/{id} - Atualizar serviço

DELETE /api/v1/servicos/{id} - Remover serviço

GET /api/v1/agenda - Listar agenda

POST /api/v1/agenda - Adicionar horário

PUT /api/v1/agenda/{id} - Atualizar horário

DELETE /api/v1/agenda/{id} - Remover horário

GET /api/v1/agendamentos - Listar agendamentos

PATCH /api/v1/agendamentos/{id}/status - Atualizar status

🔒 Autenticação
Cadastre uma empresa:

bash
POST /api/v1/auth/register
{
  "nome": "Minha Empresa",
  "email": "empresa@exemplo.com",
  "senha": "senha123",
  "telefone": "11999999999"
}
Faça login para obter o token:

bash
POST /api/v1/auth/login
{
  "email": "empresa@exemplo.com",
  "senha": "senha123"
}
Use o token nas requisições:

bash
Authorization: Bearer <seu-token>
📱 Integração WhatsApp
O sistema suporta duas formas de envio de mensagens:

Twilio
Configure no .env:

text
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
WhatsApp Cloud API (Meta)
Configure no .env:

text
WHATSAPP_ACCESS_TOKEN=seu_token
WHATSAPP_PHONE_NUMBER_ID=seu_phone_number_id
WHATSAPP_BUSINESS_ACCOUNT_ID=seu_business_account_id
🧪 Testes
bash
# Executar todos os testes
pytest -v

# Executar com cobertura
pytest --cov=app tests/
📦 Deploy
Preparação para produção
Altere a SECRET_KEY no .env

Configure ENVIRONMENT=production

Defina ALLOWED_ORIGINS para seu domínio

Use PostgreSQL em produção (não SQLite)

Configure SSL/TLS

Use variáveis de ambiente seguras

Exemplo com Docker em produção
bash
# Construir imagem
docker build -t saas-agendamento .

# Executar container
docker run -d \
  --name saas-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=sua-chave-secreta \
  -e ENVIRONMENT=production \
  saas-agendamento
🤝 Contribuição
Fork o projeto

Crie sua branch (git checkout -b feature/nova-funcionalidade)

Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')

Push para a branch (git push origin feature/nova-funcionalidade)

Abra um Pull Request

📄 Licença
Este projeto está sob a licença MIT.

📞 Suporte
Para dúvidas ou problemas, abra uma issue no repositório.

text

## 60. Criar estrutura de diretórios

```bash
# Comandos para criar a estrutura de diretórios
mkdir -p app/{api/v1,core,models,repositories,schemas,services,utils}
mkdir -p alembic/versions
mkdir -p tests
touch alembic/versions/.gitkeep
✅ Projeto Completo!
O backend SaaS de agendamento está 100% completo com:

Características Implementadas:
✅ FastAPI com rotas públicas e privadas
✅ PostgreSQL com SQLAlchemy ORM
✅ JWT para autenticação segura
✅ Clean Architecture com separação de camadas
✅ CRUD completo para serviços, agenda e agendamentos
✅ Integração WhatsApp (Twilio + WhatsApp Cloud API)
✅ Validação de horários e prevenção de conflitos
✅ Docker e Docker Compose para fácil deploy
✅ Seed inicial com dados de exemplo
✅ Testes básicos implementados
✅ Documentação automática via Swagger

Para começar:
bash
# Clone o projeto
git clone <seu-repositorio>
cd saas-agendamento

# Configure as variáveis de ambiente
cp .env.example .env

# Execute com Docker
docker-compose up -d

# Acesse a documentação
# http://localhost:8000/api/docs