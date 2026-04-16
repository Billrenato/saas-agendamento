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
        cursor.execute("DROP TABLE IF EXISTS atendente_servicos CASCADE")
        cursor.execute("DROP TABLE IF EXISTS atendentes CASCADE")
        cursor.execute("DROP TABLE IF EXISTS servico_imagens CASCADE")
        cursor.execute("DROP TABLE IF EXISTS agendamentos CASCADE")
        cursor.execute("DROP TABLE IF EXISTS agenda CASCADE")
        cursor.execute("DROP TABLE IF EXISTS servicos CASCADE")
        cursor.execute("DROP TABLE IF EXISTS empresas CASCADE")
        
        print("✅ Tabelas antigas removidas")
        print("🔄 Criando novas tabelas...")
        
        # 1. Criar tabela empresas
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
                site VARCHAR(255),
                whatsapp_adicional VARCHAR(20),
                ativo BOOLEAN DEFAULT TRUE,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                twilio_account_sid VARCHAR(100),
                twilio_auth_token VARCHAR(100),
                twilio_whatsapp_number VARCHAR(20),
                whatsapp_welcome_message TEXT,
                whatsapp_confirmation_message TEXT,
                whatsapp_cancel_message TEXT,
                send_reminder_hours INTEGER DEFAULT 24
            )
        """)
        print("✅ Tabela 'empresas' criada")
        
        # 2. Criar tabela servicos (antes de atendente_servicos)
        cursor.execute("""
            CREATE TABLE servicos (
                id SERIAL PRIMARY KEY,
                empresa_id INTEGER REFERENCES empresas(id) ON DELETE CASCADE,
                nome VARCHAR(255) NOT NULL,
                descricao TEXT,
                duracao_minutos INTEGER NOT NULL,
                preco DECIMAL(10,2),
                imagem VARCHAR(500),
                ativo BOOLEAN DEFAULT TRUE,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabela 'servicos' criada")
        
        # 3. Criar tabela servico_imagens
        cursor.execute("""
            CREATE TABLE servico_imagens (
                id SERIAL PRIMARY KEY,
                servico_id INTEGER REFERENCES servicos(id) ON DELETE CASCADE,
                imagem_url TEXT NOT NULL,
                ordem INTEGER DEFAULT 0,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabela 'servico_imagens' criada")
        
        # 4. Criar tabela atendentes (antes de agenda e agendamentos)
        cursor.execute("""
            CREATE TABLE atendentes (
                id SERIAL PRIMARY KEY,
                empresa_id INTEGER REFERENCES empresas(id) ON DELETE CASCADE,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                telefone VARCHAR(20),
                foto TEXT,
                ativo BOOLEAN DEFAULT TRUE,
                ordem_exibicao INTEGER DEFAULT 0,
                criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabela 'atendentes' criada")
        
        # 5. Criar tabela atendente_servicos (agora servicos já existe!)
        cursor.execute("""
            CREATE TABLE atendente_servicos (
                id SERIAL PRIMARY KEY,
                atendente_id INTEGER REFERENCES atendentes(id) ON DELETE CASCADE,
                servico_id INTEGER REFERENCES servicos(id) ON DELETE CASCADE,
                criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(atendente_id, servico_id)
            )
        """)
        print("✅ Tabela 'atendente_servicos' criada")
        
        # 6. Criar tabela agenda (com atendente_id)
        cursor.execute("""
            CREATE TABLE agenda (
                id SERIAL PRIMARY KEY,
                empresa_id INTEGER REFERENCES empresas(id) ON DELETE CASCADE,
                dia_semana INTEGER,
                data_especifica DATE,
                hora_inicio TIME NOT NULL,
                hora_fim TIME NOT NULL,
                intervalo_inicio TIME,
                intervalo_fim TIME,
                is_excecao BOOLEAN DEFAULT FALSE,
                atendente_id INTEGER REFERENCES atendentes(id) ON DELETE CASCADE,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabela 'agenda' criada")
        
        # 7. Criar tabela agendamentos (com atendente_id)
        cursor.execute("""
            CREATE TABLE agendamentos (
                id SERIAL PRIMARY KEY,
                empresa_id INTEGER REFERENCES empresas(id) ON DELETE CASCADE,
                servico_id INTEGER REFERENCES servicos(id) ON DELETE SET NULL,
                atendente_id INTEGER REFERENCES atendentes(id) ON DELETE SET NULL,
                nome_cliente VARCHAR(255) NOT NULL,
                telefone_cliente VARCHAR(20) NOT NULL,
                data_hora TIMESTAMP NOT NULL,
                status VARCHAR(20) DEFAULT 'pendente',
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                lembrete_enviado BOOLEAN DEFAULT FALSE
            )
        """)
        print("✅ Tabela 'agendamentos' criada")
        
        # Criar índices
        print("🔄 Criando índices...")
        
        # Índices empresas
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_empresas_email ON empresas(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_empresas_segmento ON empresas(segmento)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_empresas_twilio ON empresas(twilio_account_sid)")
        
        # Índices servicos
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_servicos_empresa ON servicos(empresa_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_servicos_ativo ON servicos(ativo)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_servico_imagens_servico ON servico_imagens(servico_id)")
        
        # Índices atendentes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_atendentes_empresa ON atendentes(empresa_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_atendentes_email ON atendentes(email)")
        
        # Índices atendente_servicos
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_atendente_servicos_atendente ON atendente_servicos(atendente_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_atendente_servicos_servico ON atendente_servicos(servico_id)")
        
        # Índices agenda
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agenda_empresa ON agenda(empresa_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agenda_data_especifica ON agenda(data_especifica)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agenda_atendente ON agenda(atendente_id)")
        
        # Índices agendamentos
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agendamentos_empresa ON agendamentos(empresa_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agendamentos_telefone ON agendamentos(telefone_cliente)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agendamentos_status ON agendamentos(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agendamentos_data_hora ON agendamentos(data_hora)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agendamentos_atendente ON agendamentos(atendente_id)")
        
        print("✅ Índices criados")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ TODAS AS TABELAS FORAM CRIADAS COM SUCESSO!")
        print("="*60)
        print("\n📋 TABELAS CRIADAS NA ORDEM CORRETA:")
        print("   1. empresas")
        print("   2. servicos")
        print("   3. servico_imagens")
        print("   4. atendentes")
        print("   5. atendente_servicos")
        print("   6. agenda (com atendente_id)")
        print("   7. agendamentos (com atendente_id)")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    criar_tabelas()