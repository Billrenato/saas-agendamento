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

# Lista de empresas com atendentes
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
        "atendentes": [
            {"nome": "Ana Silva", "email": "ana@belezatotal.com", "telefone": "11988888888", "servicos_indices": [0, 1, 2]},
            {"nome": "Maria Santos", "email": "maria@belezatotal.com", "telefone": "11977777777", "servicos_indices": [1, 2, 3, 4]},
            {"nome": "Carla Oliveira", "email": "carla@belezatotal.com", "telefone": "11966666666", "servicos_indices": [0, 3, 4]},
        ],
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
        "atendentes": [
            {"nome": "João Silva", "email": "joao@barbeariajoao.com", "telefone": "11988880000", "servicos_indices": [0, 1, 2]},
            {"nome": "Carlos Souza", "email": "carlos@barbeariajoao.com", "telefone": "11977770000", "servicos_indices": [0, 1, 3]},
            {"nome": "Roberto Lima", "email": "roberto@barbeariajoao.com", "telefone": "11966660000", "servicos_indices": [2, 3]},
        ],
        "servicos": [
            ("Corte Masculino", "Corte tradicional e moderno", 30, 40.00, IMAGENS_SERVICOS["corte"]),
            ("Barba", "Barba completa com navalha", 30, 30.00, IMAGENS_SERVICOS["barba"]),
            ("Corte + Barba", "Pacote completo", 60, 65.00, IMAGENS_SERVICOS["corte"]),
            ("Hidratação Capilar", "Hidratação para barba e cabelo", 45, 50.00, IMAGENS_SERVICOS["corte"]),
        ],
        "agenda": [(0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
                   (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "08:00", "18:00")]
    },
]

def inserir_atendente_agenda(cursor, empresa_id, atendente_id, agenda_dias):
    """Insere agenda para um atendente específico"""
    for dia, inicio, fim in agenda_dias:
        cursor.execute("""
            INSERT INTO agenda (empresa_id, dia_semana, hora_inicio, hora_fim, intervalo_inicio, intervalo_fim, atendente_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (empresa_id, dia, inicio, fim, "12:00", "13:00", atendente_id))

try:
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("=" * 60)
    print("🚀 AGENDEI - INSERÇÃO DE EMPRESAS COM ATENDENTES")
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
        
        # Inserir serviços e guardar IDs
        servicos_ids = []
        for idx, (nome, desc, duracao, preco, imagem) in enumerate(empresa['servicos']):
            cursor.execute("""
                INSERT INTO servicos (empresa_id, nome, descricao, duracao_minutos, preco, imagem, ativo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (empresa_id, nome, desc, duracao, preco, imagem, True))
            servico_id = cursor.fetchone()[0]
            servicos_ids.append(servico_id)
        
        print(f"   ✅ {len(empresa['servicos'])} serviços criados")
        
        # Inserir atendentes e relacionamentos
        atendentes_ids = []
        if 'atendentes' in empresa:
            for atendente in empresa['atendentes']:
                cursor.execute("""
                    INSERT INTO atendentes (empresa_id, nome, email, telefone, ativo, ordem_exibicao)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (empresa_id, atendente['nome'], atendente['email'], atendente['telefone'], True, len(atendentes_ids)))
                atendente_id = cursor.fetchone()[0]
                atendentes_ids.append(atendente_id)
                
                # Vincular serviços ao atendente
                for servico_idx in atendente['servicos_indices']:
                    if servico_idx < len(servicos_ids):
                        cursor.execute("""
                            INSERT INTO atendente_servicos (atendente_id, servico_id)
                            VALUES (%s, %s)
                        """, (atendente_id, servicos_ids[servico_idx]))
                
                # Criar agenda para o atendente (usando os mesmos horários da empresa)
                inserir_atendente_agenda(cursor, empresa_id, atendente_id, empresa['agenda'])
            
            print(f"   ✅ {len(empresa['atendentes'])} atendentes criados com suas agendas")
        
        # Inserir agenda geral da empresa (sem atendente específico)
        for dia, inicio, fim in empresa['agenda']:
            cursor.execute("""
                INSERT INTO agenda (empresa_id, dia_semana, hora_inicio, hora_fim, intervalo_inicio, intervalo_fim, atendente_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (empresa_id, dia, inicio, fim, "12:00", "13:00", None))
        
        print(f"   ✅ {len(empresa['agenda'])} dias de agenda geral configurados")
    
    print("\n" + "=" * 60)
    print("✅ TODAS AS EMPRESAS FORAM INSERIDAS COM SUCESSO!")
    print("=" * 60)
    print(f"\n🔐 CREDENCIAIS (para todas as empresas):")
    print(f"   Senha: {SENHA_PADRAO}")
    
    print("\n📋 EMPRESAS CADASTRADAS:")
    print("-" * 60)
    
    cursor.execute("""
        SELECT id, nome, email, telefone, segmento, 
               (SELECT COUNT(*) FROM atendentes WHERE empresa_id = empresas.id) as qtd_atendentes,
               (SELECT COUNT(*) FROM servicos WHERE empresa_id = empresas.id) as qtd_servicos
        FROM empresas ORDER BY id
    """)
    empresas_db = cursor.fetchall()
    
    for emp in empresas_db:
        print(f"\n   🏢 ID: {emp[0]} | {emp[1]}")
        print(f"      📧 {emp[2]}")
        print(f"      📞 {emp[3]}")
        print(f"      🏷️  {emp[4]}")
        print(f"      👥 Atendentes: {emp[5]} | ✂️ Serviços: {emp[6]}")
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
    print(f"👥 Empresas com atendentes e agendas individuais!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()