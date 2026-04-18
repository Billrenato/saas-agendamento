from app.core.config import settings

print("=" * 50)
print("🔧 CONFIGURAÇÕES DO SISTEMA")
print("=" * 50)
print(f"🌍 Ambiente: {settings.ENVIRONMENT}")
print(f"🔐 JWT Algorithm: {settings.ALGORITHM}")
print(f"🔑 SECRET_KEY configurada: {'✅ SIM' if settings.SECRET_KEY != 'sua-chave-secreta-aqui' else '❌ NÃO'}")
print(f"🌐 CORS: {settings.ALLOWED_ORIGINS}")
print(f"📁 Upload dir: {settings.UPLOAD_DIR}")
print(f"📦 Max upload: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB")
print(f"📱 Twilio configurado: {'✅ SIM' if settings.twilio_configured else '❌ NÃO (opcional)'}")
print("=" * 50)