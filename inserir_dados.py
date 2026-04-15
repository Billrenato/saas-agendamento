import psycopg2
import bcrypt
from datetime import datetime

# Configuração do banco
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "saas_agendamento",
    "user": "postgres",
    "password": "010203"
}

# Senha padrão para todas as empresas
SENHA_PADRAO = "senha123"
senha_hash = bcrypt.hashpw(SENHA_PADRAO.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# URLs de imagens para serviços - MAIS IMAGENS
IMAGENS_SERVICOS = {
    "corte": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=400",
    "corte_feminino": "https://images.unsplash.com/photo-1562322140-8baeececf3df?w=400",
    "manicure": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400",
    "pedicure": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=400",
    "maquiagem": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=400",
    "maquiagem_noiva": "https://images.unsplash.com/photo-1512496015851-a90fb38f796f?w=400",
    "barba": "https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=400",
    "massagem": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=400",
    "limpeza": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400",
    "pilates": "https://images.unsplash.com/photo-1518611012118-696072aa03a1?w=400",
    "dental": "https://images.unsplash.com/photo-1606811971618-4486d14f3f99?w=400",
    "fisioterapia": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400",
    "pet": "https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=400",
    "academia": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400",
    "tatuagem": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400",
    "spa": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=400",
}

# Lista de empresas
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
        "site": "https://www.belezatotal.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1560066984-138dad7b1350?w=800",
        "logo": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=150",
        "servicos": [
            ("Corte de Cabelo", "Corte masculino e feminino com acabamento profissional", 30, 50.00, IMAGENS_SERVICOS["corte"]),
            ("Manicure", "Cuidados completos para as mãos", 45, 35.00, IMAGENS_SERVICOS["manicure"]),
            ("Pedicure", "Cuidados completos para os pés", 45, 40.00, IMAGENS_SERVICOS["pedicure"]),
            ("Maquiagem", "Maquiagem profissional para todas as ocasiões", 60, 80.00, IMAGENS_SERVICOS["maquiagem"]),
            ("Penteado", "Penteados para festas e eventos", 45, 60.00, IMAGENS_SERVICOS["corte_feminino"]),
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
        "site": None,
        "foto_capa": "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?w=800",
        "logo": "https://images.unsplash.com/photo-1562322140-8baeececf3df?w=150",
        "servicos": [
            ("Corte Feminino", "Corte moderno e personalizado", 45, 70.00, IMAGENS_SERVICOS["corte_feminino"]),
            ("Coloração", "Tintura e mechas", 90, 120.00, IMAGENS_SERVICOS["corte_feminino"]),
            ("Escova", "Escova modeladora", 30, 45.00, IMAGENS_SERVICOS["corte_feminino"]),
            ("Hidratação", "Hidratação profunda", 60, 80.00, IMAGENS_SERVICOS["corte_feminino"]),
        ],
        "agenda": [(0, "09:00", "20:00"), (1, "09:00", "20:00"), (2, "09:00", "20:00"),
                   (3, "09:00", "20:00"), (4, "09:00", "20:00"), (5, "09:00", "16:00")]
    },
    {
        "nome": "Make Up Studio",
        "email": "contato@makeupstudio.com",
        "telefone": "11944443333",
        "segmento": "Beleza",
        "endereco": "Alameda Santos, 200",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01419-001",
        "descricao": "Studio especializado em maquiagem profissional para eventos e noivas.",
        "site": "https://www.makeupstudio.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1512496015851-a90fb38f796f?w=800",
        "logo": "https://images.unsplash.com/photo-1512496015851-a90fb38f796f?w=150",
        "servicos": [
            ("Maquiagem Social", "Maquiagem para eventos", 60, 100.00, IMAGENS_SERVICOS["maquiagem"]),
            ("Maquiagem Noiva", "Maquiagem para casamento", 90, 200.00, IMAGENS_SERVICOS["maquiagem_noiva"]),
            ("Curso de Auto Maquiagem", "Aprenda a se maquiar", 120, 250.00, IMAGENS_SERVICOS["maquiagem"]),
        ],
        "agenda": [(0, "09:00", "19:00"), (1, "09:00", "19:00"), (2, "09:00", "19:00"),
                   (3, "09:00", "19:00"), (4, "09:00", "19:00"), (5, "09:00", "15:00")]
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
        "site": None,
        "foto_capa": "https://images.unsplash.com/photo-1599351431202-1e0f013789b5?w=800",
        "logo": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=150",
        "servicos": [
            ("Corte Masculino", "Corte tradicional e moderno", 30, 40.00, IMAGENS_SERVICOS["corte"]),
            ("Barba", "Barba completa com navalha", 30, 30.00, IMAGENS_SERVICOS["barba"]),
            ("Corte + Barba", "Pacote completo", 60, 65.00, IMAGENS_SERVICOS["corte"]),
            ("Hidratação Capilar", "Hidratação para barba e cabelo", 45, 50.00, IMAGENS_SERVICOS["corte"]),
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
        "site": "https://www.barbeariavintage.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=800",
        "logo": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=150",
        "servicos": [
            ("Corte Premium", "Corte com toalha quente", 45, 60.00, IMAGENS_SERVICOS["corte"]),
            ("Barba Premium", "Barba com toalha quente", 45, 50.00, IMAGENS_SERVICOS["barba"]),
            ("Combo Master", "Corte + Barba + Hidratação", 90, 100.00, IMAGENS_SERVICOS["corte"]),
            ("Massagem Capilar", "Massagem relaxante no couro cabeludo", 30, 40.00, IMAGENS_SERVICOS["massagem"]),
        ],
        "agenda": [(0, "09:00", "21:00"), (1, "09:00", "21:00"), (2, "09:00", "21:00"),
                   (3, "09:00", "21:00"), (4, "09:00", "21:00"), (5, "09:00", "17:00")]
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
        "site": "https://www.odontosorriso.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=800",
        "logo": "https://images.unsplash.com/photo-1606811971618-4486d14f3f99?w=150",
        "servicos": [
            ("Limpeza", "Limpeza e profilaxia", 60, 150.00, IMAGENS_SERVICOS["dental"]),
            ("Restauração", "Tratamento de cáries", 45, 200.00, IMAGENS_SERVICOS["dental"]),
            ("Clareamento", "Clareamento dental", 60, 300.00, IMAGENS_SERVICOS["dental"]),
            ("Canal", "Tratamento de canal", 90, 500.00, IMAGENS_SERVICOS["dental"]),
            ("Implante", "Implante dentário", 120, 1500.00, IMAGENS_SERVICOS["dental"]),
        ],
        "agenda": [(0, "08:00", "18:00"), (1, "08:00", "18:00"), (2, "08:00", "18:00"),
                   (3, "08:00", "18:00"), (4, "08:00", "18:00"), (5, "08:00", "12:00")]
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
        "site": None,
        "foto_capa": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800",
        "logo": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=150",
        "servicos": [
            ("Fisioterapia", "Sessão de fisioterapia", 60, 120.00, IMAGENS_SERVICOS["fisioterapia"]),
            ("Acupuntura", "Sessão de acupuntura", 45, 100.00, IMAGENS_SERVICOS["fisioterapia"]),
            ("Massagem Terapêutica", "Massagem relaxante", 60, 90.00, IMAGENS_SERVICOS["massagem"]),
            ("Pilates", "Pilates clínico", 60, 110.00, IMAGENS_SERVICOS["pilates"]),
        ],
        "agenda": [(0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
                   (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "08:00", "14:00")]
    },

    # ESTÉTICA E BEM-ESTAR
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
        "site": "https://www.renovare.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=800",
        "logo": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=150",
        "servicos": [
            ("Limpeza de Pele", "Limpeza profunda", 60, 120.00, IMAGENS_SERVICOS["limpeza"]),
            ("Massagem Relaxante", "Massagem terapêutica", 60, 100.00, IMAGENS_SERVICOS["massagem"]),
            ("Drenagem Linfática", "Drenagem modeladora", 60, 110.00, IMAGENS_SERVICOS["massagem"]),
            ("Tratamento para Acne", "Protocolo completo", 45, 150.00, IMAGENS_SERVICOS["limpeza"]),
            ("Radiofrequência", "Tratamento estético facial", 60, 200.00, IMAGENS_SERVICOS["spa"]),
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
        "site": None,
        "foto_capa": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=800",
        "logo": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=150",
        "servicos": [
            ("Massagem Relaxante", "Massagem com óleos essenciais", 60, 90.00, IMAGENS_SERVICOS["massagem"]),
            ("Massagem Tailandesa", "Técnica tailandesa", 90, 130.00, IMAGENS_SERVICOS["massagem"]),
            ("Quick Massage", "Massagem rápida de 30min", 30, 50.00, IMAGENS_SERVICOS["massagem"]),
            ("Pedras Quentes", "Massagem com pedras vulcânicas", 80, 120.00, IMAGENS_SERVICOS["massagem"]),
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
        "site": "https://www.amigobicho.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=800",
        "logo": "https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=150",
        "servicos": [
            ("Banho e Tosa", "Banho e tosa completa", 90, 80.00, IMAGENS_SERVICOS["pet"]),
            ("Consulta Veterinária", "Consulta com veterinário", 30, 150.00, IMAGENS_SERVICOS["pet"]),
            ("Vacinação", "Vacinas anuais", 20, 100.00, IMAGENS_SERVICOS["pet"]),
            ("Hospedagem", "Hotel para pets", 480, 60.00, IMAGENS_SERVICOS["pet"]),
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
        "site": "https://www.corpoativo.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800",
        "logo": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=150",
        "servicos": [
            ("Avaliação Física", "Avaliação completa", 60, 100.00, IMAGENS_SERVICOS["academia"]),
            ("Personal Trainer", "Sessão de treino", 60, 80.00, IMAGENS_SERVICOS["academia"]),
            ("Nutrição", "Consulta nutricional", 45, 120.00, IMAGENS_SERVICOS["academia"]),
            ("Crossfit", "Aula de crossfit", 60, 90.00, IMAGENS_SERVICOS["academia"]),
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
        "site": None,
        "foto_capa": "https://images.unsplash.com/photo-1518611012118-696072aa03a1?w=800",
        "logo": "https://images.unsplash.com/photo-1518611012118-696072aa03a1?w=150",
        "servicos": [
            ("Pilates Solo", "Aula individual", 60, 90.00, IMAGENS_SERVICOS["pilates"]),
            ("Pilates Dupla", "Aula para 2 pessoas", 60, 60.00, IMAGENS_SERVICOS["pilates"]),
            ("Avaliação Postural", "Análise completa", 45, 80.00, IMAGENS_SERVICOS["pilates"]),
            ("Pilates Suspensão", "Aula com equipamentos", 60, 100.00, IMAGENS_SERVICOS["pilates"]),
        ],
        "agenda": [(0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
                   (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "09:00", "13:00")]
    },
    {
        "nome": "Estúdio de Tatuagem Ink",
        "email": "contato@ink.com",
        "telefone": "11988887777",
        "segmento": "Estética",
        "endereco": "Rua Augusta, 2000",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01405-000",
        "descricao": "Estúdio de tatuagem e body piercing com artistas renomados.",
        "site": "https://www.inktattoo.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=800",
        "logo": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=150",
        "servicos": [
            ("Tatuagem Pequena", "Até 10cm", 60, 200.00, IMAGENS_SERVICOS["tatuagem"]),
            ("Tatuagem Média", "10-20cm", 120, 400.00, IMAGENS_SERVICOS["tatuagem"]),
            ("Tatuagem Grande", "Acima de 20cm", 180, 600.00, IMAGENS_SERVICOS["tatuagem"]),
            ("Piercing", "Colocação de piercing", 30, 80.00, IMAGENS_SERVICOS["tatuagem"]),
        ],
        "agenda": [(0, "10:00", "20:00"), (1, "10:00", "20:00"), (2, "10:00", "20:00"),
                   (3, "10:00", "20:00"), (4, "10:00", "20:00"), (5, "10:00", "18:00")]
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
        
        # Inserir empresa com site
        cursor.execute("""
            INSERT INTO empresas (
                nome, email, senha_hash, telefone, segmento, 
                endereco, cidade, estado, cep, descricao, 
                site, foto_capa, logo, ativo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            empresa['nome'], empresa['email'], senha_hash, empresa['telefone'],
            empresa['segmento'], empresa['endereco'], empresa['cidade'],
            empresa['estado'], empresa['cep'], empresa['descricao'],
            empresa.get('site'), empresa['foto_capa'], empresa['logo'], True
        ))
        
        empresa_id = cursor.fetchone()[0]
        print(f"   ✅ Empresa ID: {empresa_id}")
        
        # Inserir serviços
        for nome, desc, duracao, preco, imagem in empresa['servicos']:
            cursor.execute("""
                INSERT INTO servicos (empresa_id, nome, descricao, duracao_minutos, preco, imagem, ativo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (empresa_id, nome, desc, duracao, preco, imagem, True))
        
        print(f"   ✅ {len(empresa['servicos'])} serviços criados")
        
        # Inserir agenda
        for dia, inicio, fim in empresa['agenda']:
            cursor.execute("""
                INSERT INTO agenda (empresa_id, dia_semana, hora_inicio, hora_fim, intervalo_inicio, intervalo_fim)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (empresa_id, dia, inicio, fim, "12:00", "13:00"))
        
        print(f"   ✅ {len(empresa['agenda'])} dias de agenda configurados")
    
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
    for emp in empresas_db:
        print(f"   http://localhost:3000/empresa/{emp[0]}")
    
    print(f"\n✨ Total de empresas inseridas: {len(empresas_db)}")
    print(f"📸 Cada serviço tem imagem personalizada!")
    print(f"🌐 Empresas com site cadastrado")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()