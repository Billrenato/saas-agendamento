# criar_tabelas.py
import psycopg2
from psycopg2 import sql

# Configuração - conectando como postgres (usuário mestre)
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="saas_agendamento",
        user="postgres",
        password="@nota1000"  # senha que você definiu durante a instalação do PostgreSQL
    )
    
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("✅ Conectado ao PostgreSQL como postgres")
    print("🔄 Criando tabelas...")
    
    # Criar tabela empresas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            senha_hash VARCHAR(255) NOT NULL,
            telefone VARCHAR(20) NOT NULL,
            ativo BOOLEAN DEFAULT TRUE,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'empresas' criada")
    
    # Criar tabela servicos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id SERIAL PRIMARY KEY,
            empresa_id INTEGER REFERENCES empresas(id) ON DELETE CASCADE,
            nome VARCHAR(255) NOT NULL,
            descricao TEXT,
            duracao_minutos INTEGER NOT NULL,
            preco DECIMAL(10,2),
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'servicos' criada")
    
    # Criar tabela agenda
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agenda (
            id SERIAL PRIMARY KEY,
            empresa_id INTEGER REFERENCES empresas(id) ON DELETE CASCADE,
            dia_semana INTEGER NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fim TIME NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'agenda' criada")
    
    # Criar tabela agendamentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id SERIAL PRIMARY KEY,
            empresa_id INTEGER REFERENCES empresas(id) ON DELETE CASCADE,
            servico_id INTEGER REFERENCES servicos(id) ON DELETE CASCADE,
            nome_cliente VARCHAR(255) NOT NULL,
            telefone_cliente VARCHAR(20) NOT NULL,
            data_hora TIMESTAMP NOT NULL,
            status VARCHAR(20) DEFAULT 'pendente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'agendamentos' criada")
    
    # Dar permissões para o usuário saas_user
    cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO saas_user")
    cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO saas_user")
    print("✅ Permissões concedidas para saas_user")
    
    print("\n📋 Tabelas criadas com sucesso!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erro: {e}")
    print("\nSe a senha do postgres não for 'postgres', altere no código ou tente:")
    print("psql -U postgres -d saas_agendamento")