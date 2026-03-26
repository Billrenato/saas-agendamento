# inserir_dados.py
import psycopg2
import bcrypt

# Gerar hash da senha
senha = "senha123"
senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"Hash gerado: {senha_hash}")

try:
    # Usar saas_user em vez de postgres
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="saas_agendamento",
        user="saas_user",
        password="senha123"
    )
    
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("✅ Conectado como saas_user")
    print("🔄 Inserindo dados...")
    
    # Inserir empresa
    cursor.execute("""
        INSERT INTO empresas (nome, email, senha_hash, telefone)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, ("Salão Beleza Total", "contato@belezatotal.com", senha_hash, "11999999999"))
    
    empresa_id = cursor.fetchone()[0]
    print(f"✅ Empresa criada (ID: {empresa_id})")
    
    # Inserir serviços
    servicos = [
        ("Corte de Cabelo", "Corte masculino e feminino", 30, 50.00),
        ("Manicure", "Cuidados para as mãos", 45, 35.00),
        ("Pedicure", "Cuidados para os pés", 45, 40.00),
        ("Maquiagem", "Maquiagem profissional", 60, 80.00),
    ]
    
    for nome, desc, duracao, preco in servicos:
        cursor.execute("""
            INSERT INTO servicos (empresa_id, nome, descricao, duracao_minutos, preco)
            VALUES (%s, %s, %s, %s, %s)
        """, (empresa_id, nome, desc, duracao, preco))
    
    print(f"✅ {len(servicos)} serviços criados")
    
    # Inserir agenda
    agenda = [
        (0, "09:00", "18:00"),
        (1, "09:00", "18:00"),
        (2, "09:00", "18:00"),
        (3, "09:00", "18:00"),
        (4, "09:00", "18:00"),
        (5, "09:00", "14:00"),
    ]
    
    for dia, inicio, fim in agenda:
        cursor.execute("""
            INSERT INTO agenda (empresa_id, dia_semana, hora_inicio, hora_fim)
            VALUES (%s, %s, %s, %s)
        """, (empresa_id, dia, inicio, fim))
    
    print(f"✅ {len(agenda)} dias de agenda configurados")
    
    print("\n" + "="*50)
    print("✅ DADOS INSERIDOS COM SUCESSO!")
    print("="*50)
    print(f"\n📝 CREDENCIAIS:")
    print(f"   Email: contato@belezatotal.com")
    print(f"   Senha: senha123")
    print(f"   Empresa ID: {empresa_id}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erro: {e}")