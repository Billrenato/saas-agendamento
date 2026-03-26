# test_db.py
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="saas_agendamento",
        user="saas_user",
        password="senha123"
    )
    print("✅ Conexão com PostgreSQL bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")