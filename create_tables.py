import psycopg2
from psycopg2 import sql

# Configuração do banco
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "saas_agendamento",
    "user": "postgres",
    "password": "010203"  # ← Coloque sua senha do PostgreSQL
}

def criar_tabelas():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("🔄 Conectado ao PostgreSQL")
        print("🗑️  Removendo tabelas existentes...")
        
        # Dropar tabelas na ordem correta (respeitando chaves estrangeiras)
        cursor.execute("DROP TABLE IF EXISTS agendamentos CASCADE")
        cursor.execute("DROP TABLE IF EXISTS agenda CASCADE")
        cursor.execute("DROP TABLE IF EXISTS servicos CASCADE")
        cursor.execute("DROP TABLE IF EXISTS empresas CASCADE")
        
        print("✅ Tabelas antigas removidas")
        print("🔄 Criando novas tabelas...")
        
        # Criar tabela empresas
        cursor.execute("""
            CREATE TABLE empresas (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                senha_hash VARCHAR(255) NOT NULL,
                telefone VARCHAR(20) NOT NULL,
                segmento VARCHAR(100),
                endereco TEXT,
                cidade VARCHAR(100),
                estado VARCHAR(2),
                cep VARCHAR(10),
                foto_capa TEXT,
                logo TEXT,
                descricao TEXT,
                horario_funcionamento TEXT,
                ativo BOOLEAN DEFAULT TRUE,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabela 'empresas' criada")
        
        # Criar tabela servicos
        cursor.execute("""
            CREATE TABLE servicos (
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
            CREATE TABLE agenda (
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
            CREATE TABLE agendamentos (
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
        
        # Criar índices
        print("🔄 Criando índices...")
        cursor.execute("CREATE INDEX idx_empresas_email ON empresas(email)")
        cursor.execute("CREATE INDEX idx_empresas_segmento ON empresas(segmento)")
        cursor.execute("CREATE INDEX idx_servicos_empresa ON servicos(empresa_id)")
        cursor.execute("CREATE INDEX idx_agenda_empresa ON agenda(empresa_id)")
        cursor.execute("CREATE INDEX idx_agendamentos_empresa ON agendamentos(empresa_id)")
        cursor.execute("CREATE INDEX idx_agendamentos_telefone ON agendamentos(telefone_cliente)")
        print("✅ Índices criados")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*50)
        print("✅ TODAS AS TABELAS FORAM CRIADAS COM SUCESSO!")
        print("="*50)
        print("\n📋 TABELAS CRIADAS:")
        print("   - empresas")
        print("   - servicos")
        print("   - agenda")
        print("   - agendamentos")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    criar_tabelas()