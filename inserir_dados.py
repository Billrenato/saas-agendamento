import psycopg2
import bcrypt
from datetime import datetime

# Configuração do banco
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "saas_agendamento",
    "user": "postgres",
    "password": "@nota1000"  # ← Coloque sua senha do PostgreSQL
}

# Senha padrão para todas as empresas
SENHA_PADRAO = "senha123"
senha_hash = bcrypt.hashpw(SENHA_PADRAO.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# URLs de imagens para serviços
IMAGENS_SERVICOS = {
    "corte": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=400",
    "manicure": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400",
    "pedicure": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=400",
    "maquiagem": "https://images.unsplash.com/photo-1512496015851-a90fb38f796f?w=400",
    "barba": "https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=400",
    "massagem": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=400",
    "limpeza": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400",
    "pilates": "https://images.unsplash.com/photo-1518611012118-696072aa03a1?w=400",
}

# Lista de empresas com dados completos - 25+ empresas
empresas = [
    # BELEZA (6 empresas)
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
            ("Corte de Cabelo", "Corte masculino e feminino com acabamento profissional", 30, 50.00, IMAGENS_SERVICOS["corte"]),
            ("Manicure", "Cuidados completos para as mãos", 45, 35.00, IMAGENS_SERVICOS["manicure"]),
            ("Pedicure", "Cuidados completos para os pés", 45, 40.00, IMAGENS_SERVICOS["pedicure"]),
            ("Maquiagem", "Maquiagem profissional para todas as ocasiões", 60, 80.00, IMAGENS_SERVICOS["maquiagem"]),
            ("Penteado", "Penteados para festas e eventos", 45, 60.00, IMAGENS_SERVICOS["corte"]),
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
            ("Corte Feminino", "Corte moderno e personalizado", 45, 70.00, IMAGENS_SERVICOS["corte"]),
            ("Coloração", "Tintura e mechas", 90, 120.00, IMAGENS_SERVICOS["corte"]),
            ("Escova", "Escova modeladora", 30, 45.00, IMAGENS_SERVICOS["corte"]),
            ("Hidratação", "Hidratação profunda", 60, 80.00, IMAGENS_SERVICOS["corte"]),
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
            ("Depilação", "Depilação com cera", 45, 50.00, IMAGENS_SERVICOS["manicure"]),
            ("Sobrancelha", "Design de sobrancelhas", 30, 35.00, IMAGENS_SERVICOS["maquiagem"]),
            ("Maquiagem", "Maquiagem completa", 60, 90.00, IMAGENS_SERVICOS["maquiagem"]),
        ],
        "agenda": [(0, "10:00", "19:00"), (1, "10:00", "19:00"), (2, "10:00", "19:00"),
                   (3, "10:00", "19:00"), (4, "10:00", "19:00"), (5, "10:00", "15:00")]
    },
    {
        "nome": "Cabelo & Estilo",
        "email": "contato@cabeloestilo.com",
        "telefone": "11966665555",
        "segmento": "Beleza",
        "endereco": "Rua Treze de Maio, 100",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01323-001",
        "descricao": "Salão de beleza focado em cortes modernos e coloração.",
        "foto_capa": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800",
        "logo": "https://images.unsplash.com/photo-1562322140-8baeececf3df?w=150",
        "servicos": [
            ("Corte Moderno", "Corte tendência", 45, 65.00, IMAGENS_SERVICOS["corte"]),
            ("Mechas", "Mechas californianas", 120, 180.00, IMAGENS_SERVICOS["corte"]),
            ("Progressiva", "Escova progressiva", 90, 150.00, IMAGENS_SERVICOS["corte"]),
        ],
        "agenda": [(0, "09:00", "19:00"), (1, "09:00", "19:00"), (2, "09:00", "19:00"),
                   (3, "09:00", "19:00"), (4, "09:00", "19:00"), (5, "09:00", "15:00")]
    },
    {
        "nome": "Studio Black Beauty",
        "email": "contato@blackbeauty.com",
        "telefone": "11955554444",
        "segmento": "Beleza",
        "endereco": "Rua Augusta, 800",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01304-001",
        "descricao": "Especialistas em cabelos cacheados e crespos.",
        "foto_capa": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=800",
        "logo": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=150",
        "servicos": [
            ("Fitagem", "Definição de cachos", 60, 80.00, IMAGENS_SERVICOS["corte"]),
            ("Hidratação", "Hidratação capilar", 45, 60.00, IMAGENS_SERVICOS["corte"]),
            ("Transição", "Corte para transição", 60, 90.00, IMAGENS_SERVICOS["corte"]),
        ],
        "agenda": [(0, "10:00", "20:00"), (1, "10:00", "20:00"), (2, "10:00", "20:00"),
                   (3, "10:00", "20:00"), (4, "10:00", "20:00"), (5, "10:00", "16:00")]
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
        "descricao": "Studio especializado em maquiagem profissional.",
        "foto_capa": "https://images.unsplash.com/photo-1512496015851-a90fb38f796f?w=800",
        "logo": "https://images.unsplash.com/photo-1512496015851-a90fb38f796f?w=150",
        "servicos": [
            ("Maquiagem Social", "Maquiagem para eventos", 60, 100.00, IMAGENS_SERVICOS["maquiagem"]),
            ("Maquiagem Noiva", "Maquiagem para casamento", 90, 200.00, IMAGENS_SERVICOS["maquiagem"]),
            ("Curso", "Curso de auto maquiagem", 120, 250.00, IMAGENS_SERVICOS["maquiagem"]),
        ],
        "agenda": [(0, "08:00", "18:00"), (1, "08:00", "18:00"), (2, "08:00", "18:00"),
                   (3, "08:00", "18:00"), (4, "08:00", "18:00"), (5, "08:00", "14:00")]
    },

    # BARBEARIA (4 empresas)
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
            ("Corte Masculino", "Corte tradicional e moderno", 30, 40.00, IMAGENS_SERVICOS["corte"]),
            ("Barba", "Barba completa com navalha", 30, 30.00, IMAGENS_SERVICOS["barba"]),
            ("Corte + Barba", "Pacote completo", 60, 65.00, IMAGENS_SERVICOS["corte"]),
            ("Pezinho", "Hidratação e corte", 20, 20.00, IMAGENS_SERVICOS["corte"]),
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
            ("Corte Premium", "Corte com toalha quente", 45, 60.00, IMAGENS_SERVICOS["corte"]),
            ("Barba Premium", "Barba com toalha quente", 45, 50.00, IMAGENS_SERVICOS["barba"]),
            ("Combo Master", "Corte + Barba + Hidratação", 90, 100.00, IMAGENS_SERVICOS["corte"]),
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
            ("Corte Degradê", "Corte com degradê", 30, 45.00, IMAGENS_SERVICOS["corte"]),
            ("Design de Barba", "Desenho e alinhamento", 20, 25.00, IMAGENS_SERVICOS["barba"]),
            ("Combo Moderno", "Corte + Barba + Sobrancelha", 60, 70.00, IMAGENS_SERVICOS["corte"]),
        ],
        "agenda": [(0, "10:00", "22:00"), (1, "10:00", "22:00"), (2, "10:00", "22:00"),
                   (3, "10:00", "22:00"), (4, "10:00", "22:00"), (5, "10:00", "18:00")]
    },
    {
        "nome": "Barbearia Imperial",
        "email": "contato@imperial.com",
        "telefone": "11933332222",
        "segmento": "Barbearia",
        "endereco": "Rua da Consolação, 1000",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01302-001",
        "descricao": "Barbearia com ambiente luxuoso e serviços exclusivos.",
        "foto_capa": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=800",
        "logo": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=150",
        "servicos": [
            ("Corte Executivo", "Corte com bebida inclusa", 45, 80.00, IMAGENS_SERVICOS["corte"]),
            ("Barba Completa", "Barba com massagem", 45, 70.00, IMAGENS_SERVICOS["barba"]),
            ("Pacote VIP", "Corte + Barba + Hidratação + Bebida", 90, 150.00, IMAGENS_SERVICOS["corte"]),
        ],
        "agenda": [(0, "08:00", "22:00"), (1, "08:00", "22:00"), (2, "08:00", "22:00"),
                   (3, "08:00", "22:00"), (4, "08:00", "22:00"), (5, "09:00", "20:00")]
    },

    # SAÚDE E ODONTOLOGIA (5 empresas)
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
            ("Limpeza", "Limpeza e profilaxia", 60, 150.00, IMAGENS_SERVICOS["limpeza"]),
            ("Restauração", "Tratamento de cáries", 45, 200.00, IMAGENS_SERVICOS["limpeza"]),
            ("Clareamento", "Clareamento dental", 60, 300.00, IMAGENS_SERVICOS["limpeza"]),
            ("Canal", "Tratamento de canal", 90, 500.00, IMAGENS_SERVICOS["limpeza"]),
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
            ("Clínico Geral", "Consulta médica", 30, 200.00, IMAGENS_SERVICOS["limpeza"]),
            ("Cardiologia", "Consulta cardiológica", 45, 300.00, IMAGENS_SERVICOS["limpeza"]),
            ("Dermatologia", "Consulta dermatológica", 30, 250.00, IMAGENS_SERVICOS["limpeza"]),
            ("Exames", "Coleta de exames", 20, 100.00, IMAGENS_SERVICOS["limpeza"]),
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
            ("Fisioterapia", "Sessão de fisioterapia", 60, 120.00, IMAGENS_SERVICOS["massagem"]),
            ("Acupuntura", "Sessão de acupuntura", 45, 100.00, IMAGENS_SERVICOS["massagem"]),
            ("Massagem Terapêutica", "Massagem relaxante", 60, 90.00, IMAGENS_SERVICOS["massagem"]),
        ],
        "agenda": [(0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
                   (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "08:00", "14:00")]
    },
    {
        "nome": "Centro Médico Paulista",
        "email": "contato@cmp.com",
        "telefone": "11922221111",
        "segmento": "Saúde",
        "endereco": "Av. Paulista, 2000",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01310-200",
        "descricao": "Centro médico com diversas especialidades.",
        "foto_capa": "https://images.unsplash.com/photo-1519494029142-80d6f4530deb?w=800",
        "logo": "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?w=150",
        "servicos": [
            ("Pediatria", "Consulta pediátrica", 30, 180.00, IMAGENS_SERVICOS["limpeza"]),
            ("Ginecologia", "Consulta ginecológica", 30, 200.00, IMAGENS_SERVICOS["limpeza"]),
            ("Oftalmologia", "Consulta oftalmológica", 30, 150.00, IMAGENS_SERVICOS["limpeza"]),
        ],
        "agenda": [(0, "08:00", "18:00"), (1, "08:00", "18:00"), (2, "08:00", "18:00"),
                   (3, "08:00", "18:00"), (4, "08:00", "18:00"), (5, "08:00", "13:00")]
    },
    {
        "nome": "Psicologia & Bem-estar",
        "email": "contato@psicologia.com",
        "telefone": "11911110000",
        "segmento": "Saúde",
        "endereco": "Rua Pamplona, 500",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01405-001",
        "descricao": "Consultório de psicologia e terapia.",
        "foto_capa": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?w=800",
        "logo": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?w=150",
        "servicos": [
            ("Terapia Individual", "Sessão de terapia", 50, 150.00, IMAGENS_SERVICOS["massagem"]),
            ("Terapia de Casal", "Sessão para casais", 60, 200.00, IMAGENS_SERVICOS["massagem"]),
            ("Avaliação", "Avaliação psicológica", 60, 180.00, IMAGENS_SERVICOS["massagem"]),
        ],
        "agenda": [(0, "09:00", "20:00"), (1, "09:00", "20:00"), (2, "09:00", "20:00"),
                   (3, "09:00", "20:00"), (4, "09:00", "20:00"), (5, "09:00", "14:00")]
    },

    # ESTÉTICA E BEM-ESTAR (6 empresas)
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
            ("Design de Sobrancelhas", "Design com henna", 30, 45.00, IMAGENS_SERVICOS["maquiagem"]),
            ("Alongamento de Cílios", "Cílios fio a fio", 90, 120.00, IMAGENS_SERVICOS["maquiagem"]),
            ("Depilação", "Cera quente e fria", 45, 60.00, IMAGENS_SERVICOS["manicure"]),
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
            ("Limpeza de Pele", "Limpeza profunda", 60, 120.00, IMAGENS_SERVICOS["limpeza"]),
            ("Massagem Relaxante", "Massagem terapêutica", 60, 100.00, IMAGENS_SERVICOS["massagem"]),
            ("Drenagem Linfática", "Drenagem modeladora", 60, 110.00, IMAGENS_SERVICOS["massagem"]),
            ("Tratamento para Acne", "Protocolo completo", 45, 150.00, IMAGENS_SERVICOS["limpeza"]),
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
            ("Massagem Relaxante", "Massagem com óleos essenciais", 60, 90.00, IMAGENS_SERVICOS["massagem"]),
            ("Massagem Tailandesa", "Técnica tailandesa", 90, 130.00, IMAGENS_SERVICOS["massagem"]),
            ("Quick Massage", "Massagem rápida de 30min", 30, 50.00, IMAGENS_SERVICOS["massagem"]),
        ],
        "agenda": [(0, "10:00", "20:00"), (1, "10:00", "20:00"), (2, "10:00", "20:00"),
                   (3, "10:00", "20:00"), (4, "10:00", "20:00"), (5, "10:00", "18:00")]
    },
    {
        "nome": "Clínica de Estética Derma",
        "email": "contato@derma.com",
        "telefone": "11999998888",
        "segmento": "Estética",
        "endereco": "Rua Funchal, 400",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "04551-001",
        "descricao": "Clínica de estética avançada com equipamentos de última geração.",
        "foto_capa": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=800",
        "logo": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=150",
        "servicos": [
            ("Laser", "Depilação a laser", 60, 150.00, IMAGENS_SERVICOS["limpeza"]),
            ("Preenchimento", "Preenchimento labial", 45, 350.00, IMAGENS_SERVICOS["limpeza"]),
            ("Botox", "Toxina botulínica", 45, 400.00, IMAGENS_SERVICOS["limpeza"]),
        ],
        "agenda": [(0, "09:00", "19:00"), (1, "09:00", "19:00"), (2, "09:00", "19:00"),
                   (3, "09:00", "19:00"), (4, "09:00", "19:00"), (5, "09:00", "15:00")]
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
        "descricao": "Estúdio de tatuagem e body piercing.",
        "foto_capa": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=800",
        "logo": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=150",
        "servicos": [
            ("Tatuagem Pequena", "Até 10cm", 60, 200.00, IMAGENS_SERVICOS["maquiagem"]),
            ("Tatuagem Média", "10-20cm", 120, 400.00, IMAGENS_SERVICOS["maquiagem"]),
            ("Tatuagem Grande", "Acima de 20cm", 180, 600.00, IMAGENS_SERVICOS["maquiagem"]),
        ],
        "agenda": [(0, "10:00", "20:00"), (1, "10:00", "20:00"), (2, "10:00", "20:00"),
                   (3, "10:00", "20:00"), (4, "10:00", "20:00"), (5, "10:00", "18:00")]
    },
    {
        "nome": "Day Spa Serena",
        "email": "contato@serena.com",
        "telefone": "11977776666",
        "segmento": "Bem-estar",
        "endereco": "Av. Jurubatuba, 1000",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "04960-000",
        "descricao": "Day spa com pacotes de relaxamento e tratamentos exclusivos.",
        "foto_capa": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=800",
        "logo": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=150",
        "servicos": [
            ("Dia de Spa", "Pacote completo com massagem e tratamentos", 240, 500.00, IMAGENS_SERVICOS["massagem"]),
            ("Ofurô", "Banho de ofurô com sais", 60, 150.00, IMAGENS_SERVICOS["massagem"]),
            ("Massagem com Pedras", "Massagem terapêutica com pedras quentes", 90, 200.00, IMAGENS_SERVICOS["massagem"]),
        ],
        "agenda": [(0, "09:00", "19:00"), (1, "09:00", "19:00"), (2, "09:00", "19:00"),
                   (3, "09:00", "19:00"), (4, "09:00", "19:00"), (5, "09:00", "17:00")]
    },

    # OUTROS (4 empresas)
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
            ("Banho e Tosa", "Banho e tosa completa", 90, 80.00, IMAGENS_SERVICOS["corte"]),
            ("Consulta Veterinária", "Consulta com veterinário", 30, 150.00, IMAGENS_SERVICOS["limpeza"]),
            ("Vacinação", "Vacinas anuais", 20, 100.00, IMAGENS_SERVICOS["limpeza"]),
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
            ("Avaliação Física", "Avaliação completa", 60, 100.00, IMAGENS_SERVICOS["pilates"]),
            ("Personal Trainer", "Sessão de treino", 60, 80.00, IMAGENS_SERVICOS["pilates"]),
            ("Nutrição", "Consulta nutricional", 45, 120.00, IMAGENS_SERVICOS["pilates"]),
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
            ("Pilates Solo", "Aula individual", 60, 90.00, IMAGENS_SERVICOS["pilates"]),
            ("Pilates Dupla", "Aula para 2 pessoas", 60, 60.00, IMAGENS_SERVICOS["pilates"]),
            ("Avaliação Postural", "Análise completa", 45, 80.00, IMAGENS_SERVICOS["pilates"]),
        ],
        "agenda": [(0, "08:00", "20:00"), (1, "08:00", "20:00"), (2, "08:00", "20:00"),
                   (3, "08:00", "20:00"), (4, "08:00", "20:00"), (5, "09:00", "13:00")]
    },
    {
        "nome": "Auto Center Rápido",
        "email": "contato@autocenter.com",
        "telefone": "11966665555",
        "segmento": "Outros",
        "endereco": "Av. dos Autonomistas, 1000",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "06020-001",
        "descricao": "Oficina mecânica com serviços rápidos e garantia.",
        "foto_capa": "https://images.unsplash.com/photo-1486006920555-cce1f1866ea6?w=800",
        "logo": "https://images.unsplash.com/photo-1486006920555-cce1f1866ea6?w=150",
        "servicos": [
            ("Troca de Óleo", "Troca de óleo e filtros", 30, 80.00, IMAGENS_SERVICOS["corte"]),
            ("Revisão", "Revisão completa", 120, 300.00, IMAGENS_SERVICOS["corte"]),
            ("Alinhamento", "Alinhamento e balanceamento", 45, 100.00, IMAGENS_SERVICOS["corte"]),
        ],
        "agenda": [(0, "08:00", "18:00"), (1, "08:00", "18:00"), (2, "08:00", "18:00"),
                   (3, "08:00", "18:00"), (4, "08:00", "18:00"), (5, "08:00", "13:00")]
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
        
        # Inserir serviços (com imagem)
        for nome, desc, duracao, preco, imagem in empresa['servicos']:
            cursor.execute("""
                INSERT INTO servicos (empresa_id, nome, descricao, duracao_minutos, preco, imagem, ativo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (empresa_id, nome, desc, duracao, preco, imagem, True))
        
        print(f"   ✅ {len(empresa['servicos'])} serviços com imagens")
        
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
    for emp in empresas_db[:15]:  # Mostra os 15 primeiros
        print(f"   http://localhost:3000/empresa/{emp[0]}")
    
    if len(empresas_db) > 15:
        print(f"   ... e mais {len(empresas_db) - 15} empresas")
    
    print(f"\n✨ Total de empresas inseridas: {len(empresas_db)}")
    print(f"📸 Cada serviço agora tem imagem personalizada!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()