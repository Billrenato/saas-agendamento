import psycopg2
import bcrypt

# Configuração do banco
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "saas_agendamento",
    "user": "postgres",
    "password": "@nota1000"
}

# Senha padrão para todas as empresas
SENHA_PADRAO = "senha123"
senha_hash = bcrypt.hashpw(SENHA_PADRAO.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Lista de empresas com dados completos - 20+ empresas
empresas = [
    # BELEZA
    {
        "nome": "Salão Beleza Total",
        "email": "contato@belezatotal.com",
        "telefone": "11999999999",
        "segmento": "Beleza",
        "endereco": "Av. Paulista, 1000",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01310-100",
        "descricao": "Salão completo com profissionais experientes. Oferecemos os melhores serviços de beleza com qualidade e preço justo.",
        "foto_capa": "https://images.unsplash.com/photo-1560066984-138dad7b1350?w=800",
        "logo": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=150",
        "servicos": [
            ("Corte de Cabelo", "Corte masculino e feminino com acabamento profissional", 30, 50.00),
            ("Manicure", "Cuidados completos para as mãos", 45, 35.00),
            ("Pedicure", "Cuidados completos para os pés", 45, 40.00),
            ("Maquiagem", "Maquiagem profissional para todas as ocasiões", 60, 80.00),
            ("Penteado", "Penteados para festas e eventos", 45, 60.00),
        ],
        "agenda": [(0, "09:00", "18:00"), (1, "09:00", "18:00"), (2, "09:00", "18:00"),
                   (3, "09:00", "18:00"), (4, "09:00", "18:00"), (5, "09:00", "14:00")]
    },
    {
        "nome": "Studio Hair Fashion",
        "email": "contato@studiohair.com",
        "telefone": "11988887777",
        "segmento": "Beleza",
        "endereco": "Rua Augusta, 1500",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01305-000",
        "descricao": "Studio especializado em cortes, coloração e tratamentos capilares.",
        "foto_capa": "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?w=800",
        "logo": "https://images.unsplash.com/photo-1562322140-8baeececf3df?w=150",
        "servicos": [
            ("Corte Feminino", "Corte moderno e personalizado", 45, 70.00),
            ("Coloração", "Tintura e mechas", 90, 120.00),
            ("Escova", "Escova modeladora", 30, 45.00),
            ("Hidratação", "Hidratação profunda", 60, 80.00),
        ],
        "agenda": [(0, "09:00", "20:00"), (1, "09:00", "20:00"), (2, "09:00", "20:00"),
                   (3, "09:00", "20:00"), (4, "09:00", "20:00"), (5, "09:00", "16:00")]
    },
    {
        "nome": "Espaço Beleza & Cia",
        "email": "contato@espacobeleza.com",
        "telefone": "11977776666",
        "segmento": "Beleza",
        "endereco": "Av. Brasil, 500",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01234-567",
        "descricao": "Espaço completo para cuidados com a beleza feminina.",
        "foto_capa": "https://images.unsplash.com/photo-1633681926022-84c23e8cb3d6?w=800",
        "logo": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=150",
        "servicos": [
            ("Depilação", "Depilação com cera", 45, 50.00),
            ("Sobrancelha", "Design de sobrancelhas", 30, 35.00),
            ("Maquiagem", "Maquiagem completa", 60, 90.00),
        ],
        "agenda": [(0, "10:00", "19:00"), (1, "10:00", "19:00"), (2, "10:00", "19:00"),
                   (3, "10:00", "19:00"), (4, "10:00", "19:00"), (5, "10:00", "15:00")]
    },

    # BARBEARIA
    {
        "nome": "Barbearia do João",
        "email": "contato@barbeariajoao.com",
        "telefone": "11888888888",
        "segmento": "Barbearia",
        "endereco": "Rua Augusta, 500",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01305-000",
        "descricao": "Barbearia tradicional com serviços de corte e barba. Ambiente masculino e descontraído.",
        "foto_capa": "https://images.unsplash.com/photo-1599351431202-1e0f013789b5?w=800",
        "logo": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=150",
        "servicos": [
            ("Corte Masculino", "Corte tradicional e moderno", 30, 40.00),
            ("Barba", "Barba completa com navalha", 30, 30.00),
            ("Corte + Barba", "Pacote completo", 60, 65.00),
            ("Pezinho", "Hidratação e corte", 20, 20.00),
        ],
        "agenda": [(0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
                   (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "08:00", "18:00")]
    },
    {
        "nome": "Barbearia Vintage",
        "email": "contato@barbeariavintage.com",
        "telefone": "11966665555",
        "segmento": "Barbearia",
        "endereco": "Rua Oscar Freire, 200",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01426-001",
        "descricao": "Barbearia estilo vintage com serviços premium e ambiente acolhedor.",
        "foto_capa": "https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=800",
        "logo": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=150",
        "servicos": [
            ("Corte Premium", "Corte com toalha quente", 45, 60.00),
            ("Barba Premium", "Barba com toalha quente", 45, 50.00),
            ("Combo Master", "Corte + Barba + Hidratação", 90, 100.00),
        ],
        "agenda": [(0, "09:00", "21:00"), (1, "09:00", "21:00"), (2, "09:00", "21:00"),
                   (3, "09:00", "21:00"), (4, "09:00", "21:00"), (5, "09:00", "17:00")]
    },
    {
        "nome": "Barbearia do Mike",
        "email": "contato@barbeariamike.com",
        "telefone": "11955554444",
        "segmento": "Barbearia",
        "endereco": "Av. Faria Lima, 300",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01451-000",
        "descricao": "Barbearia moderna com profissionais jovens e criativos.",
        "foto_capa": "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?w=800",
        "logo": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=150",
        "servicos": [
            ("Corte Degradê", "Corte com degradê", 30, 45.00),
            ("Design de Barba", "Desenho e alinhamento", 20, 25.00),
            ("Combo Moderno", "Corte + Barba + Sobrancelha", 60, 70.00),
        ],
        "agenda": [(0, "10:00", "22:00"), (1, "10:00", "22:00"), (2, "10:00", "22:00"),
                   (3, "10:00", "22:00"), (4, "10:00", "22:00"), (5, "10:00", "18:00")]
    },

    # SAÚDE E ODONTOLOGIA
    {
        "nome": "Clínica Odonto Sorriso",
        "email": "contato@odontosorriso.com",
        "telefone": "11777777777",
        "segmento": "Odontologia",
        "endereco": "Rua Vergueiro, 2000",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "04101-000",
        "descricao": "Clínica odontológica especializada em tratamentos estéticos e preventivos.",
        "foto_capa": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=800",
        "logo": "https://images.unsplash.com/photo-1606811971618-4486d14f3f99?w=150",
        "servicos": [
            ("Limpeza", "Limpeza e profilaxia", 60, 150.00),
            ("Restauração", "Tratamento de cáries", 45, 200.00),
            ("Clareamento", "Clareamento dental", 60, 300.00),
            ("Canal", "Tratamento de canal", 90, 500.00),
        ],
        "agenda": [(0, "08:00", "18:00"), (1, "08:00", "18:00"), (2, "08:00", "18:00"),
                   (3, "08:00", "18:00"), (4, "08:00", "18:00"), (5, "08:00", "12:00")]
    },
    {
        "nome": "Clínica Saúde Total",
        "email": "contato@saudetotal.com",
        "telefone": "11944443333",
        "segmento": "Saúde",
        "endereco": "Av. Brigadeiro Faria Lima, 400",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01451-000",
        "descricao": "Clínica multiprofissional com diversas especialidades médicas.",
        "foto_capa": "https://images.unsplash.com/photo-1519494029142-80d6f4530deb?w=800",
        "logo": "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?w=150",
        "servicos": [
            ("Clínico Geral", "Consulta médica", 30, 200.00),
            ("Cardiologia", "Consulta cardiológica", 45, 300.00),
            ("Dermatologia", "Consulta dermatológica", 30, 250.00),
            ("Exames", "Coleta de exames", 20, 100.00),
        ],
        "agenda": [(0, "08:00", "19:00"), (1, "08:00", "19:00"), (2, "08:00", "19:00"),
                   (3, "08:00", "19:00"), (4, "08:00", "19:00"), (5, "08:00", "13:00")]
    },
    {
        "nome": "Fisioterapia & Movimento",
        "email": "contato@fisioterapia.com",
        "telefone": "11933332222",
        "segmento": "Fisioterapia",
        "endereco": "Rua Haddock Lobo, 600",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01414-001",
        "descricao": "Clínica especializada em fisioterapia ortopédica e reabilitação.",
        "foto_capa": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800",
        "logo": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=150",
        "servicos": [
            ("Fisioterapia", "Sessão de fisioterapia", 60, 120.00),
            ("Acupuntura", "Sessão de acupuntura", 45, 100.00),
            ("Massagem Terapêutica", "Massagem relaxante", 60, 90.00),
        ],
        "agenda": [(0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
                   (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "08:00", "14:00")]
    },

    # ESTÉTICA E BEM-ESTAR
    {
        "nome": "Studio de Beleza da Ana",
        "email": "contato@studioana.com",
        "telefone": "11666666666",
        "segmento": "Estética",
        "endereco": "Alameda Santos, 1500",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01418-100",
        "descricao": "Studio especializado em design de sobrancelhas, cílios e depilação.",
        "foto_capa": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800",
        "logo": "https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?w=150",
        "servicos": [
            ("Design de Sobrancelhas", "Design com henna", 30, 45.00),
            ("Alongamento de Cílios", "Cílios fio a fio", 90, 120.00),
            ("Depilação", "Cera quente e fria", 45, 60.00),
        ],
        "agenda": [(0, "09:00", "19:00"), (1, "09:00", "19:00"), (2, "09:00", "19:00"),
                   (3, "09:00", "19:00"), (4, "09:00", "19:00"), (5, "09:00", "15:00")]
    },
    {
        "nome": "Centro Estético Renovare",
        "email": "contato@renovare.com",
        "telefone": "11555555555",
        "segmento": "Bem-estar",
        "endereco": "Rua Oscar Freire, 800",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01426-001",
        "descricao": "Centro estético com tratamentos faciais e corporais. Massagens relaxantes e terapêuticas.",
        "foto_capa": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=800",
        "logo": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=150",
        "servicos": [
            ("Limpeza de Pele", "Limpeza profunda", 60, 120.00),
            ("Massagem Relaxante", "Massagem terapêutica", 60, 100.00),
            ("Drenagem Linfática", "Drenagem modeladora", 60, 110.00),
            ("Tratamento para Acne", "Protocolo completo", 45, 150.00),
        ],
        "agenda": [(0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
                   (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "08:00", "16:00")]
    },
    {
        "nome": "Espaço Zen Massagens",
        "email": "contato@espacozent.com",
        "telefone": "11922221111",
        "segmento": "Massagem",
        "endereco": "Rua da Consolação, 2000",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01302-001",
        "descricao": "Espaço dedicado ao bem-estar com massagens e terapias holísticas.",
        "foto_capa": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=800",
        "logo": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=150",
        "servicos": [
            ("Massagem Relaxante", "Massagem com óleos essenciais", 60, 90.00),
            ("Massagem Tailandesa", "Técnica tailandesa", 90, 130.00),
            ("Quick Massage", "Massagem rápida de 30min", 30, 50.00),
        ],
        "agenda": [(0, "10:00", "20:00"), (1, "10:00", "20:00"), (2, "10:00", "20:00"),
                   (3, "10:00", "20:00"), (4, "10:00", "20:00"), (5, "10:00", "18:00")]
    },

    # OUTROS
    {
        "nome": "Pet Shop Amigo Bicho",
        "email": "contato@amigobicho.com",
        "telefone": "11911110000",
        "segmento": "Outros",
        "endereco": "Av. São João, 100",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01035-000",
        "descricao": "Pet shop completo com banho, tosa e consulta veterinária.",
        "foto_capa": "https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=800",
        "logo": "https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=150",
        "servicos": [
            ("Banho e Tosa", "Banho e tosa completa", 90, 80.00),
            ("Consulta Veterinária", "Consulta com veterinário", 30, 150.00),
            ("Vacinação", "Vacinas anuais", 20, 100.00),
        ],
        "agenda": [(0, "09:00", "18:00"), (1, "09:00", "18:00"), (2, "09:00", "18:00"),
                   (3, "09:00", "18:00"), (4, "09:00", "18:00"), (5, "09:00", "14:00")]
    },
    {
        "nome": "Academia Corpo Ativo",
        "email": "contato@corpoativo.com",
        "telefone": "11900009999",
        "segmento": "Saúde",
        "endereco": "Av. Paulista, 2000",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01310-200",
        "descricao": "Academia com personal trainers e diversas modalidades de treino.",
        "foto_capa": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800",
        "logo": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=150",
        "servicos": [
            ("Avaliação Física", "Avaliação completa", 60, 100.00),
            ("Personal Trainer", "Sessão de treino", 60, 80.00),
            ("Nutrição", "Consulta nutricional", 45, 120.00),
        ],
        "agenda": [(0, "06:00", "22:00"), (1, "06:00", "22:00"), (2, "06:00", "22:00"),
                   (3, "06:00", "22:00"), (4, "06:00", "22:00"), (5, "08:00", "18:00")]
    },
    {
        "nome": "Studio Pilates",
        "email": "contato@studiopilates.com",
        "telefone": "11988889999",
        "segmento": "Bem-estar",
        "endereco": "Rua Mourato Coelho, 500",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "05417-001",
        "descricao": "Studio especializado em Pilates para todas as idades.",
        "foto_capa": "https://images.unsplash.com/photo-1518611012118-696072aa03a1?w=800",
        "logo": "https://images.unsplash.com/photo-1518611012118-696072aa03a1?w=150",
        "servicos": [
            ("Pilates Solo", "Aula individual", 60, 90.00),
            ("Pilates Dupla", "Aula para 2 pessoas", 60, 60.00),
            ("Avaliação Postural", "Análise completa", 45, 80.00),
        ],
        "agenda": [(0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
                   (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "09:00", "13:00")]
    }
]

try:
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("=" * 60)
    print("🚀 AGENDEI - INSERÇÃO DE EMPRESAS")
    print("=" * 60)
    print("✅ Conectado ao banco de dados")
    print(f"📊 Total de empresas a inserir: {len(empresas)}")
    print("🔄 Iniciando inserção...")
    print("-" * 60)
    
    for i, empresa in enumerate(empresas, 1):
        print(f"\n📌 [{i}/{len(empresas)}] Inserindo: {empresa['nome']}")
        
        # Inserir empresa
        cursor.execute("""
            INSERT INTO empresas (
                nome, email, senha_hash, telefone, segmento, 
                endereco, cidade, estado, cep, descricao, 
                foto_capa, logo, ativo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            empresa['nome'], empresa['email'], senha_hash, empresa['telefone'],
            empresa['segmento'], empresa['endereco'], empresa['cidade'],
            empresa['estado'], empresa['cep'], empresa['descricao'],
            empresa['foto_capa'], empresa['logo'], True
        ))
        
        empresa_id = cursor.fetchone()[0]
        print(f"   ✅ Empresa ID: {empresa_id}")
        
        # Inserir serviços
        for nome, desc, duracao, preco in empresa['servicos']:
            cursor.execute("""
                INSERT INTO servicos (empresa_id, nome, descricao, duracao_minutos, preco)
                VALUES (%s, %s, %s, %s, %s)
            """, (empresa_id, nome, desc, duracao, preco))
        
        print(f"   ✅ {len(empresa['servicos'])} serviços")
        
        # Inserir agenda
        for dia, inicio, fim in empresa['agenda']:
            cursor.execute("""
                INSERT INTO agenda (empresa_id, dia_semana, hora_inicio, hora_fim)
                VALUES (%s, %s, %s, %s)
            """, (empresa_id, dia, inicio, fim))
        
        print(f"   ✅ {len(empresa['agenda'])} dias de agenda")
    
    print("\n" + "=" * 60)
    print("✅ TODAS AS EMPRESAS FORAM INSERIDAS COM SUCESSO!")
    print("=" * 60)
    print(f"\n🔐 CREDENCIAIS (para todas as empresas):")
    print(f"   Senha: {SENHA_PADRAO}")
    
    print("\n📋 EMPRESAS CADASTRADAS:")
    print("-" * 60)
    
    cursor.execute("SELECT id, nome, email, telefone, segmento FROM empresas ORDER BY id")
    empresas_db = cursor.fetchall()
    
    for emp in empresas_db:
        print(f"\n   🏢 ID: {emp[0]} | {emp[1]}")
        print(f"      📧 {emp[2]}")
        print(f"      📞 {emp[3]}")
        print(f"      🏷️  {emp[4]}")
        print(f"      🔗 http://localhost:3000/empresa/{emp[0]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("🎯 LINKS PARA TESTAR:")
    print("=" * 60)
    for emp in empresas_db[:10]:  # Mostra apenas os 10 primeiros
        print(f"   http://localhost:3000/empresa/{emp[0]}")
    
    if len(empresas_db) > 10:
        print(f"   ... e mais {len(empresas_db) - 10} empresas")
    
    print("\n✨ Total de empresas inseridas:", len(empresas_db))
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()