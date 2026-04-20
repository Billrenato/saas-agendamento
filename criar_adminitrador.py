import psycopg2
import bcrypt

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "saas_agendamento",
    "user": "postgres",
    "password": "@nota1000"
}

email = "renatojrmathias94@gmail.com"  # 👈 COLOQUE SEU EMAIL
senha = "Billskate1@"
nome = "Administrador"
telefone = "11972937989"

senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO empresas (nome, email, senha_hash, telefone, ativo)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (email) DO NOTHING
""", (nome, email, senha_hash, telefone, True))

conn.commit()
cursor.close()
conn.close()

print(f"✅ Admin criado: {email} / {senha}")