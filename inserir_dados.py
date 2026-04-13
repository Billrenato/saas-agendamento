import psycopg2
import bcrypt

# Configuração do banco
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "saas_agendamento",
    "user": "postgres",
    "password": "010203"  # ← Coloque sua senha
}

# Senha padrão para todas as empresas
SENHA_PADRAO = "senha123"
senha_hash = bcrypt.hashpw(SENHA_PADRAO.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Lista de empresas com dados completos
empresas = [
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
        ],
        "agenda": [
            (0, "09:00", "18:00"), (1, "09:00", "18:00"), (2, "09:00", "18:00"),
            (3, "09:00", "18:00"), (4, "09:00", "18:00"), (5, "09:00", "14:00")
        ]
    },
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
        ],
        "agenda": [
            (0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
            (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "08:00", "18:00")
        ]
    },
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
        ],
        "agenda": [
            (0, "08:00", "18:00"), (1, "08:00", "18:00"), (2, "08:00", "18:00"),
            (3, "08:00", "18:00"), (4, "08:00", "18:00"), (5, "08:00", "12:00")
        ]
    },
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
        "agenda": [
            (0, "09:00", "19:00"), (1, "09:00", "19:00"), (2, "09:00", "19:00"),
            (3, "09:00", "19:00"), (4, "09:00", "19:00"), (5, "09:00", "15:00")
        ]
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
        ],
        "agenda": [
            (0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
            (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "08:00", "16:00")
        ]
    }
]

try:
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("✅ Conectado ao banco de dados")
    print("🔄 Inserindo empresas...")
    print("="*50)
    
    for i, empresa in enumerate(empresas, 1):
        print(f"\n📌 Inserindo empresa {i}: {empresa['nome']}")
        
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
        print(f"   ✅ Empresa criada (ID: {empresa_id})")
        
        # Inserir serviços
        for nome, desc, duracao, preco in empresa['servicos']:
            cursor.execute("""
                INSERT INTO servicos (empresa_id, nome, descricao, duracao_minutos, preco)
                VALUES (%s, %s, %s, %s, %s)
            """, (empresa_id, nome, desc, duracao, preco))
        
        print(f"   ✅ {len(empresa['servicos'])} serviços criados")
        
        # Inserir agenda
        for dia, inicio, fim in empresa['agenda']:
            cursor.execute("""
                INSERT INTO agenda (empresa_id, dia_semana, hora_inicio, hora_fim)
                VALUES (%s, %s, %s, %s)
            """, (empresa_id, dia, inicio, fim))
        
        print(f"   ✅ {len(empresa['agenda'])} dias de agenda configurados")
    
    print("\n" + "="*50)
    print("✅ TODAS AS EMPRESAS FORAM INSERIDAS COM SUCESSO!")
    print("="*50)
    print(f"\n📝 CREDENCIAIS (para todas as empresas):")
    print(f"   Senha: {SENHA_PADRAO}")
    print("\n📋 EMPRESAS CADASTRADAS:")
    
    cursor.execute("SELECT id, nome, email, telefone, segmento FROM empresas ORDER BY id")
    empresas_db = cursor.fetchall()
    
    for emp in empresas_db:
        print(f"\n   ID: {emp[0]} | {emp[1]}")
        print(f"   Email: {emp[2]}")
        print(f"   Telefone: {emp[3]}")
        print(f"   Segmento: {emp[4]}")
        print(f"   Link: http://localhost:3000/empresa/{emp[0]}")
    
    cursor.close()
    conn.close()
    
    print("\n🎯 Para testar, acesse:")
    for emp in empresas_db:
        print(f"   http://localhost:3000/empresa/{emp[0]}")
    
except Exception as e:
    print(f"❌ Erro: {e}")