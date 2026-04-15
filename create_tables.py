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
        cursor.execute("DROP TABLE IF EXISTS servico_imagens CASCADE")
        cursor.execute("DROP TABLE IF EXISTS agendamentos CASCADE")
        cursor.execute("DROP TABLE IF EXISTS agenda CASCADE")
        cursor.execute("DROP TABLE IF EXISTS servicos CASCADE")
        cursor.execute("DROP TABLE IF EXISTS empresas CASCADE")
        
        print("✅ Tabelas antigas removidas")
        print("🔄 Criando novas tabelas...")
        
        # Criar tabela empresas com todos os campos
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
        
        # Criar tabela servicos (com campo imagem e ativo)
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
        print("✅ Tabela 'servicos' criada (com imagem e ativo)")
        
        # Criar tabela servico_imagens (para múltiplas fotos)
        cursor.execute("""
            CREATE TABLE servico_imagens (
                id SERIAL PRIMARY KEY,
                servico_id INTEGER REFERENCES servicos(id) ON DELETE CASCADE,
                imagem_url TEXT NOT NULL,
                ordem INTEGER DEFAULT 0,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabela 'servico_imagens' criada (galeria de fotos)")
        
        # Criar tabela agenda com suporte para data específica e intervalo
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
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT agenda_empresa_id_dia_semana_data_key 
                UNIQUE (empresa_id, dia_semana, data_especifica)
            )
        """)
        print("✅ Tabela 'agenda' criada (com data específica e intervalo)")
        
        # Criar tabela agendamentos
        cursor.execute("""
            CREATE TABLE agendamentos (
                id SERIAL PRIMARY KEY,
                empresa_id INTEGER REFERENCES empresas(id) ON DELETE CASCADE,
                servico_id INTEGER REFERENCES servicos(id) ON DELETE SET NULL,
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
        cursor.execute("CREATE INDEX idx_empresas_email ON empresas(email)")
        cursor.execute("CREATE INDEX idx_empresas_segmento ON empresas(segmento)")
        cursor.execute("CREATE INDEX idx_servicos_empresa ON servicos(empresa_id)")
        cursor.execute("CREATE INDEX idx_servicos_ativo ON servicos(ativo)")
        cursor.execute("CREATE INDEX idx_servico_imagens_servico ON servico_imagens(servico_id)")
        cursor.execute("CREATE INDEX idx_agenda_empresa ON agenda(empresa_id)")
        cursor.execute("CREATE INDEX idx_agenda_data_especifica ON agenda(data_especifica)")
        cursor.execute("CREATE INDEX idx_agendamentos_empresa ON agendamentos(empresa_id)")
        cursor.execute("CREATE INDEX idx_agendamentos_telefone ON agendamentos(telefone_cliente)")
        cursor.execute("CREATE INDEX idx_agendamentos_status ON agendamentos(status)")
        cursor.execute("CREATE INDEX idx_agendamentos_data_hora ON agendamentos(data_hora)")
        cursor.execute("CREATE INDEX idx_empresas_twilio ON empresas(twilio_account_sid)")
        print("✅ Índices criados")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ TODAS AS TABELAS FORAM CRIADAS COM SUCESSO!")
        print("="*60)
        print("\n📋 TABELAS CRIADAS:")
        print("   1. empresas")
        print("   2. servicos")
        print("   3. servico_imagens (galeria de fotos)")
        print("   4. agenda (com data específica e intervalo)")
        print("   5. agendamentos")
        
        print("\n📋 NOVOS CAMPOS NA TABELA 'empresas':")
        print("   - site (URL do site da empresa)")
        print("   - whatsapp_adicional (WhatsApp secundário)")
        print("   - twilio_account_sid (Account SID da Twilio)")
        print("   - twilio_auth_token (Auth Token da Twilio)")
        print("   - twilio_whatsapp_number (Número WhatsApp)")
        print("   - whatsapp_welcome_message (Mensagem de boas-vindas)")
        print("   - whatsapp_confirmation_message (Mensagem de confirmação)")
        print("   - whatsapp_cancel_message (Mensagem de cancelamento)")
        
        print("\n📋 NOVOS CAMPOS NA TABELA 'servicos':")
        print("   - imagem (URL da imagem principal)")
        print("   - ativo (para desativar serviços)")
        
        print("\n📋 NOVA TABELA 'servico_imagens':")
        print("   - servico_id (relacionamento com serviço)")
        print("   - imagem_url (URL da imagem)")
        print("   - ordem (ordem de exibição)")
        
        print("\n📋 NOVOS CAMPOS NA TABELA 'agenda':")
        print("   - data_especifica (data para horário especial)")
        print("   - intervalo_inicio (início do intervalo de almoço)")
        print("   - intervalo_fim (fim do intervalo de almoço)")
        print("   - is_excecao (indica se é horário especial)")
        print("   - dia_semana agora é opcional (NULL para exceções)")
        
        print("\n📋 CAMPOS NA TABELA 'agendamentos':")
        print("   - lembrete_enviado (controle de lembrete)")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    criar_tabelas()