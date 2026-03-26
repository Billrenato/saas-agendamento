@echo off
echo 🚀 Iniciando backend do SaaS Agendamento...
echo ========================================

cd C:\Users\Renat\saas-agendamento

echo 📦 Verificando dependências...
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] pydantic pydantic-settings python-multipart alembic twilio httpx python-dotenv pytz email-validator bcrypt

echo.
echo 🗄️  Verificando banco de dados...
python -c "from sqlalchemy import create_engine; engine = create_engine('postgresql://saas_user:senha123@localhost:5432/saas_agendamento'); conn = engine.connect(); conn.close(); print('✅ Banco conectado')"

echo.
echo 🌱 Verificando dados iniciais...
python seed_data.py

echo.
echo 🎯 Iniciando servidor...
echo    API: http://localhost:8000
echo    Docs: http://localhost:8000/api/docs
echo.
echo Pressione Ctrl+C para parar
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000