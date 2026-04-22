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

# URLs de imagens para serviços
IMAGENS_SERVICOS = {
    "corte_masculino": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=400",
    "corte_feminino": "https://images.unsplash.com/photo-1562322140-8baeececf3df?w=400",
    "manicure": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400",
    "pedicure": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=400",
    "maquiagem": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=400",
    "maquiagem_noiva": "https://images.unsplash.com/photo-1512496015851-a90fb38f796f?w=400",
    "barba": "https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=400",
    "sobrancelha": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=400",
    "progressiva": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400",
    "massagem_relaxante": "https://images.unsplash.com/photo-1603398938378-e54eab446d4e?w=400",
    "acupuntura": "https://images.unsplash.com/photo-1512295767273-ac109ac3acfa?w=400",
    "pilates": "https://images.unsplash.com/photo-1518611012118-696072aa03a1?w=400",
    "yoga": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400",
    "drenagem": "https://images.unsplash.com/photo-1544396821-4dd40b938ad3?w=400",
    "rpg": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400",
    "dental_checkup": "https://images.unsplash.com/photo-1606811971618-4486d14f3f99?w=400",
    "clareamento": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=400",
    "implante": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=400",
    "ortodontia": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=400",
    "banho_tosa": "https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=400",
    "veterinario": "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?w=400",
    "personal_trainer": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400",
    "avaliacao_fisica": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400",
    "tatuagem": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400",
    "spa": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=400",
    "limpeza_pele": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400",
    "harmonizacao": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400",
    "tratamento_facial": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=400",
    "psicologia": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=400",
    "terapia_casal": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=400",
}

# Lista de 10 empresas completas (telefones apenas com números - 11 dígitos)
empresas = [
    {
        "nome": "Salão Beleza Total",
        "email": "contato@belezatotal.com",
        "telefone": "11999999999",  # Apenas números, 11 dígitos
        "segmento": "Beleza",
        "endereco": "Av. Paulista, 1000, Bela Vista",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01310100",
        "descricao": "⭐ Salão completo com 10 anos de experiência. Oferecemos os melhores serviços de beleza com qualidade e preço justo. Ambiente climatizado, profissionais certificados e produtos de primeira linha.",
        "horario_funcionamento": "Segunda a Sexta: 09h às 20h | Sábado: 09h às 18h | Domingo: 10h às 14h",
        "site": "https://www.belezatotal.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1560066984-138dad7b1350?w=1200",
        "logo": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=200",
        "whatsapp_adicional": "11988889999",
        "atendentes": [
            {"nome": "Ana Silva", "email": "ana@belezatotal.com", "telefone": "11988888888", "servicos_indices": [0, 1, 2, 4], "foto": "https://randomuser.me/api/portraits/women/1.jpg"},
            {"nome": "Maria Santos", "email": "maria@belezatotal.com", "telefone": "11977777777", "servicos_indices": [1, 2, 3, 5, 7], "foto": "https://randomuser.me/api/portraits/women/2.jpg"},
            {"nome": "Carla Oliveira", "email": "carla@belezatotal.com", "telefone": "11966666666", "servicos_indices": [0, 3, 4, 6, 8], "foto": "https://randomuser.me/api/portraits/women/3.jpg"},
        ],
        "servicos": [
            ("💇‍♀️ Corte Feminino", "Corte moderno com técnicas atualizadas", 45, 70.00, IMAGENS_SERVICOS["corte_feminino"]),
            ("💇‍♂️ Corte Masculino", "Corte tradicional e moderno", 30, 50.00, IMAGENS_SERVICOS["corte_masculino"]),
            ("💅 Manicure", "Cuidados completos para as mãos", 45, 40.00, IMAGENS_SERVICOS["manicure"]),
            ("🦶 Pedicure", "Cuidados completos para os pés", 45, 45.00, IMAGENS_SERVICOS["pedicure"]),
            ("💄 Maquiagem", "Maquiagem profissional para todas as ocasiões", 60, 90.00, IMAGENS_SERVICOS["maquiagem"]),
            ("👰 Maquiagem Noiva", "Pacote completo para noivas", 120, 250.00, IMAGENS_SERVICOS["maquiagem_noiva"]),
            ("✍️ Sobrancelha", "Design e henna", 30, 35.00, IMAGENS_SERVICOS["sobrancelha"]),
            ("✨ Progressiva", "Escova progressiva definitiva", 180, 200.00, IMAGENS_SERVICOS["progressiva"]),
            ("💆‍♀️ Tratamento Capilar", "Hidratação e reconstrução", 60, 80.00, IMAGENS_SERVICOS["corte_feminino"]),
        ],
        "agenda": [(1, "09:00", "20:00"), (2, "09:00", "20:00"), (3, "09:00", "20:00"),
                   (4, "09:00", "20:00"), (5, "09:00", "20:00"), (6, "09:00", "18:00"), (0, "10:00", "14:00")]
    },
    {
        "nome": "Barbearia do João",
        "email": "contato@barbeariajoao.com",
        "telefone": "11988888888",
        "segmento": "Barbearia",
        "endereco": "Rua Augusta, 500, Consolação",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01305000",
        "descricao": "✂️ Barbearia tradicional com serviços premium. Ambiente masculino e descontraído com cerveja gelada, sinuca e futebol ao vivo.",
        "horario_funcionamento": "Segunda a Sexta: 09h às 21h | Sábado: 09h às 20h | Domingo: 10h às 16h",
        "site": "https://www.barbeariajoao.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1599351431202-1e0f013789b5?w=1200",
        "logo": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=200",
        "whatsapp_adicional": "11977778888",
        "atendentes": [
            {"nome": "João Silva", "email": "joao@barbeariajoao.com", "telefone": "11988880000", "servicos_indices": [0, 1, 2], "foto": "https://randomuser.me/api/portraits/men/1.jpg"},
            {"nome": "Carlos Souza", "email": "carlos@barbeariajoao.com", "telefone": "11977770000", "servicos_indices": [0, 1, 3], "foto": "https://randomuser.me/api/portraits/men/2.jpg"},
            {"nome": "Roberto Lima", "email": "roberto@barbeariajoao.com", "telefone": "11966660000", "servicos_indices": [2, 3], "foto": "https://randomuser.me/api/portraits/men/3.jpg"},
            {"nome": "Paulo Mendes", "email": "paulo@barbeariajoao.com", "telefone": "11955550000", "servicos_indices": [0, 1, 2, 3], "foto": "https://randomuser.me/api/portraits/men/4.jpg"},
        ],
        "servicos": [
            ("✂️ Corte Social", "Corte tradicional e moderno com finalização", 30, 45.00, IMAGENS_SERVICOS["corte_masculino"]),
            ("🧔 Barba Completa", "Barba com navalha, toalha quente", 30, 35.00, IMAGENS_SERVICOS["barba"]),
            ("✨ Corte + Barba", "Pacote completo com benefícios", 60, 75.00, IMAGENS_SERVICOS["corte_masculino"]),
            ("💎 Degustação", "Corte, barba, sobrancelha", 90, 120.00, IMAGENS_SERVICOS["barba"]),
        ],
        "agenda": [(1, "09:00", "21:00"), (2, "09:00", "21:00"), (3, "09:00", "21:00"),
                   (4, "09:00", "21:00"), (5, "09:00", "21:00"), (6, "09:00", "20:00"), (0, "10:00", "16:00")]
    },
    {
        "nome": "Espaço Saúde e Vida",
        "email": "contato@saudevida.com",
        "telefone": "11977777777",
        "segmento": "Saúde",
        "endereco": "Rua Oscar Freire, 1500, Jardins",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01426001",
        "descricao": "🏥 Clínica multidisciplinar com fisioterapia, pilates e massoterapia.",
        "horario_funcionamento": "Segunda a Sexta: 08h às 20h | Sábado: 08h às 16h",
        "site": "https://www.saudevida.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=1200",
        "logo": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=200",
        "whatsapp_adicional": "11966667777",
        "atendentes": [
            {"nome": "Dra. Patrícia Lima", "email": "patricia@saudevida.com", "telefone": "11988881111", "servicos_indices": [0, 1], "foto": "https://randomuser.me/api/portraits/women/4.jpg"},
            {"nome": "Dr. Ricardo Alves", "email": "ricardo@saudevida.com", "telefone": "11977772222", "servicos_indices": [2, 3], "foto": "https://randomuser.me/api/portraits/men/5.jpg"},
            {"nome": "Fernanda Costa", "email": "fernanda@saudevida.com", "telefone": "11966663333", "servicos_indices": [4, 5], "foto": "https://randomuser.me/api/portraits/women/5.jpg"},
        ],
        "servicos": [
            ("💆 Massagem Relaxante", "Técnica suave para aliviar tensões", 60, 120.00, IMAGENS_SERVICOS["massagem_relaxante"]),
            ("🔬 Acupuntura", "Tratamento tradicional chinês", 45, 100.00, IMAGENS_SERVICOS["acupuntura"]),
            ("🏋️ Pilates", "Aulas individuais ou em grupo", 50, 80.00, IMAGENS_SERVICOS["pilates"]),
            ("🧘 Yoga", "Aulas para todos os níveis", 60, 70.00, IMAGENS_SERVICOS["yoga"]),
            ("💧 Drenagem Linfática", "Tratamento pós-cirúrgico", 60, 150.00, IMAGENS_SERVICOS["drenagem"]),
            ("🔧 RPG", "Reeducação postural global", 45, 110.00, IMAGENS_SERVICOS["rpg"]),
        ],
        "agenda": [(1, "08:00", "20:00"), (2, "08:00", "20:00"), (3, "08:00", "20:00"),
                   (4, "08:00", "20:00"), (5, "08:00", "20:00"), (6, "08:00", "16:00")]
    },
    {
        "nome": "Clínica Odonto Sorriso",
        "email": "contato@odontosorriso.com",
        "telefone": "11966666666",
        "segmento": "Odontologia",
        "endereco": "Av. Brigadeiro Faria Lima, 2000, Pinheiros",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01451001",
        "descricao": "🦷 Clínica odontológica de última geração com equipamentos modernos.",
        "horario_funcionamento": "Segunda a Sexta: 09h às 19h | Sábado: 09h às 14h",
        "site": "https://www.odontosorriso.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1606811971618-4486d14f3f99?w=1200",
        "logo": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=200",
        "whatsapp_adicional": "11955556666",
        "atendentes": [
            {"nome": "Dra. Amanda Rocha", "email": "amanda@odontosorriso.com", "telefone": "11988882444", "servicos_indices": [0, 1, 2], "foto": "https://randomuser.me/api/portraits/women/6.jpg"},
            {"nome": "Dr. Bruno Santos", "email": "bruno@odontosorriso.com", "telefone": "11977773555", "servicos_indices": [1, 2, 3], "foto": "https://randomuser.me/api/portraits/men/6.jpg"},
        ],
        "servicos": [
            ("🦷 Limpeza e Check-up", "Prevenção e diagnóstico", 40, 150.00, IMAGENS_SERVICOS["dental_checkup"]),
            ("✨ Clareamento Dental", "Clareamento a laser", 60, 800.00, IMAGENS_SERVICOS["clareamento"]),
            ("🦷 Implantes", "Implantes dentários", 90, 2500.00, IMAGENS_SERVICOS["implante"]),
            ("🔧 Aparelho Ortodôntico", "Aparelhos fixos", 45, 200.00, IMAGENS_SERVICOS["ortodontia"]),
        ],
        "agenda": [(1, "09:00", "19:00"), (2, "09:00", "19:00"), (3, "09:00", "19:00"),
                   (4, "09:00", "19:00"), (5, "09:00", "19:00"), (6, "09:00", "14:00")]
    },
    {
        "nome": "Pet Shop Amigo Fiel",
        "email": "contato@amigofiel.com",
        "telefone": "11955555555",
        "segmento": "Pet",
        "endereco": "Rua Cardeal Arcoverde, 1000, Pinheiros",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "05407003",
        "descricao": "🐾 O melhor para seu pet! Banho, tosa e veterinário.",
        "horario_funcionamento": "Segunda a Sábado: 09h às 19h | Domingo: 10h às 14h",
        "site": "https://www.amigofiel.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=1200",
        "logo": "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?w=200",
        "whatsapp_adicional": "11944445555",
        "atendentes": [
            {"nome": "Mariana Costa", "email": "mariana@amigofiel.com", "telefone": "11988883777", "servicos_indices": [0, 1], "foto": "https://randomuser.me/api/portraits/women/7.jpg"},
            {"nome": "Rafael Silva", "email": "rafael@amigofiel.com", "telefone": "11977774888", "servicos_indices": [0, 2], "foto": "https://randomuser.me/api/portraits/men/7.jpg"},
        ],
        "servicos": [
            ("🐕 Banho e Tosa", "Banho, tosa e cuidados", 60, 80.00, IMAGENS_SERVICOS["banho_tosa"]),
            ("🏥 Consulta Veterinária", "Consulta clínica geral", 30, 120.00, IMAGENS_SERVICOS["veterinario"]),
            ("🎾 Day Care", "Dia inteiro de diversão", 480, 60.00, IMAGENS_SERVICOS["veterinario"]),
        ],
        "agenda": [(1, "09:00", "19:00"), (2, "09:00", "19:00"), (3, "09:00", "19:00"),
                   (4, "09:00", "19:00"), (5, "09:00", "19:00"), (6, "09:00", "18:00"), (0, "10:00", "14:00")]
    },
    {
        "nome": "Academia Fit Power",
        "email": "contato@fitpower.com",
        "telefone": "11944444444",
        "segmento": "Academia",
        "endereco": "Av. Santo Amaro, 3000, Brooklin",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "04571010",
        "descricao": "💪 Academia completa com estrutura de ponta.",
        "horario_funcionamento": "Segunda a Sexta: 06h às 23h | Sábado: 06h às 22h | Domingo: 08h às 18h",
        "site": "https://www.fitpower.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1200",
        "logo": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=200",
        "whatsapp_adicional": "11933334444",
        "atendentes": [
            {"nome": "Prof. André Lima", "email": "andre@fitpower.com", "telefone": "11988884111", "servicos_indices": [0, 1], "foto": "https://randomuser.me/api/portraits/men/8.jpg"},
            {"nome": "Profa. Carla Souza", "email": "carla@fitpower.com", "telefone": "11977775222", "servicos_indices": [0, 2], "foto": "https://randomuser.me/api/portraits/women/8.jpg"},
        ],
        "servicos": [
            ("💪 Personal Trainer", "Treino individualizado", 60, 90.00, IMAGENS_SERVICOS["personal_trainer"]),
            ("📊 Avaliação Física", "Avaliação completa", 45, 80.00, IMAGENS_SERVICOS["avaliacao_fisica"]),
            ("🏃‍♂️ Aula Experimental", "Aula teste gratuita", 60, 0.00, IMAGENS_SERVICOS["personal_trainer"]),
        ],
        "agenda": [(1, "06:00", "23:00"), (2, "06:00", "23:00"), (3, "06:00", "23:00"),
                   (4, "06:00", "23:00"), (5, "06:00", "23:00"), (6, "06:00", "22:00"), (0, "08:00", "18:00")]
    },
    {
        "nome": "Studio Tatoo Art",
        "email": "contato@tattooart.com",
        "telefone": "11933333333",
        "segmento": "Tatuagem",
        "endereco": "Rua Augusta, 2500, Cerqueira César",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01413100",
        "descricao": "🎨 Estúdio de tatuagem e piercings com artistas renomados.",
        "horario_funcionamento": "Segunda a Sábado: 10h às 20h",
        "site": "https://www.tattooart.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=1200",
        "logo": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=200",
        "whatsapp_adicional": "11922223333",
        "atendentes": [
            {"nome": "Mike Tattoo", "email": "mike@tattooart.com", "telefone": "11988885444", "servicos_indices": [0], "foto": "https://randomuser.me/api/portraits/men/9.jpg"},
            {"nome": "Ana Art", "email": "ana@tattooart.com", "telefone": "11977776555", "servicos_indices": [0, 1], "foto": "https://randomuser.me/api/portraits/women/9.jpg"},
        ],
        "servicos": [
            ("🎨 Tatuagem", "Tatuagens personalizadas", 120, 300.00, IMAGENS_SERVICOS["tatuagem"]),
            ("🔘 Piercing", "Piercings profissionais", 30, 100.00, IMAGENS_SERVICOS["tatuagem"]),
        ],
        "agenda": [(1, "10:00", "20:00"), (2, "10:00", "20:00"), (3, "10:00", "20:00"),
                   (4, "10:00", "20:00"), (5, "10:00", "20:00"), (6, "10:00", "18:00")]
    },
    {
        "nome": "SPA Zen Relax",
        "email": "contato@zenrelax.com",
        "telefone": "11922222222",
        "segmento": "SPA",
        "endereco": "Alameda Santos, 1500, Jardins",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01419001",
        "descricao": "🧘‍♀️ SPA de dia completo com tratamentos exclusivos.",
        "horario_funcionamento": "Todos os dias: 10h às 20h",
        "site": "https://www.zenrelax.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=1200",
        "logo": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=200",
        "whatsapp_adicional": "11911112222",
        "atendentes": [
            {"nome": "Luciana Flores", "email": "luciana@zenrelax.com", "telefone": "11988886777", "servicos_indices": [0, 1], "foto": "https://randomuser.me/api/portraits/women/10.jpg"},
            {"nome": "Juliana Paz", "email": "juliana@zenrelax.com", "telefone": "11977778888", "servicos_indices": [0, 2], "foto": "https://randomuser.me/api/portraits/women/11.jpg"},
        ],
        "servicos": [
            ("💆‍♀️ Massagem com Pedras", "Terapia com pedras quentes", 90, 180.00, IMAGENS_SERVICOS["spa"]),
            ("🌿 Day Use SPA", "Dia completo no SPA", 360, 350.00, IMAGENS_SERVICOS["spa"]),
            ("💐 Tratamento de Casal", "Massagem para casais", 120, 400.00, IMAGENS_SERVICOS["spa"]),
        ],
        "agenda": [(1, "10:00", "20:00"), (2, "10:00", "20:00"), (3, "10:00", "20:00"),
                   (4, "10:00", "20:00"), (5, "10:00", "20:00"), (6, "10:00", "20:00"), (0, "10:00", "18:00")]
    },
    {
        "nome": "Clínica de Estética Face & Body",
        "email": "contato@facebody.com",
        "telefone": "11911111111",
        "segmento": "Estética",
        "endereco": "Rua Haddock Lobo, 1000, Cerqueira César",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01414001",
        "descricao": "✨ Clínica de estética avançada com tecnologia de ponta.",
        "horario_funcionamento": "Segunda a Sexta: 09h às 19h | Sábado: 09h às 14h",
        "site": "https://www.facebody.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=1200",
        "logo": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=200",
        "whatsapp_adicional": "11900001111",
        "atendentes": [
            {"nome": "Dra. Renata Lima", "email": "renata@facebody.com", "telefone": "11988887999", "servicos_indices": [0, 1], "foto": "https://randomuser.me/api/portraits/women/12.jpg"},
            {"nome": "Dra. Beatriz Rocha", "email": "beatriz@facebody.com", "telefone": "11977778000", "servicos_indices": [0, 2], "foto": "https://randomuser.me/api/portraits/women/13.jpg"},
        ],
        "servicos": [
            ("💆‍♀️ Limpeza de Pele", "Limpeza profunda", 60, 150.00, IMAGENS_SERVICOS["limpeza_pele"]),
            ("💉 Harmonização Facial", "Preenchimento e botox", 90, 1200.00, IMAGENS_SERVICOS["harmonizacao"]),
            ("✨ Tratamento Facial", "Peeling e radiofrequência", 45, 200.00, IMAGENS_SERVICOS["tratamento_facial"]),
        ],
        "agenda": [(1, "09:00", "19:00"), (2, "09:00", "19:00"), (3, "09:00", "19:00"),
                   (4, "09:00", "19:00"), (5, "09:00", "19:00"), (6, "09:00", "14:00")]
    },
    {
        "nome": "Psicólogos Online",
        "email": "contato@psicologosonline.com",
        "telefone": "11900000000",
        "segmento": "Psicologia",
        "endereco": "Av. Faria Lima, 3000, Itaim Bibi",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "04538132",
        "descricao": "🧠 Atendimento psicológico online e presencial.",
        "horario_funcionamento": "Segunda a Sexta: 08h às 20h | Sábado: 09h às 14h",
        "site": "https://www.psicologosonline.com.br",
        "foto_capa": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1200",
        "logo": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=200",
        "whatsapp_adicional": "11988880000",
        "atendentes": [
            {"nome": "Dra. Fernanda Melo", "email": "fernanda@psicologosonline.com", "telefone": "11988881234", "servicos_indices": [0, 1], "foto": "https://randomuser.me/api/portraits/women/14.jpg"},
            {"nome": "Dr. Ricardo Pontes", "email": "ricardo@psicologosonline.com", "telefone": "11977775678", "servicos_indices": [0, 2], "foto": "https://randomuser.me/api/portraits/men/10.jpg"},
        ],
        "servicos": [
            ("🧠 Psicoterapia Individual", "Sessão individual", 50, 150.00, IMAGENS_SERVICOS["psicologia"]),
            ("💑 Terapia de Casal", "Sessões para casais", 60, 200.00, IMAGENS_SERVICOS["terapia_casal"]),
            ("👨‍👩‍👧 Terapia Familiar", "Sessões para família", 90, 250.00, IMAGENS_SERVICOS["psicologia"]),
        ],
        "agenda": [(1, "08:00", "20:00"), (2, "08:00", "20:00"), (3, "08:00", "20:00"),
                   (4, "08:00", "20:00"), (5, "08:00", "20:00"), (6, "09:00", "14:00")]
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
    
    print("=" * 80)
    print("🚀 AGENDEI - INSERÇÃO DE 10 EMPRESAS COMPLETAS")
    print("=" * 80)
    print("✅ Conectado ao banco de dados")
    print(f"📊 Total de empresas a inserir: {len(empresas)}")
    print("🔄 Iniciando inserção...")
    print("-" * 80)
    
    for i, empresa in enumerate(empresas, 1):
        print(f"\n📌 [{i}/{len(empresas)}] Inserindo: {empresa['nome']}")
        print(f"   🏷️  Segmento: {empresa['segmento']}")
        
        # Inserir empresa
        cursor.execute("""
            INSERT INTO empresas (
                nome, email, senha_hash, telefone, segmento, 
                endereco, cidade, estado, cep, descricao, 
                horario_funcionamento, site, foto_capa, logo, 
                whatsapp_adicional, ativo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            empresa['nome'], empresa['email'], senha_hash, empresa['telefone'],
            empresa['segmento'], empresa['endereco'], empresa['cidade'],
            empresa['estado'], empresa['cep'], empresa['descricao'],
            empresa['horario_funcionamento'], empresa.get('site'), empresa['foto_capa'], 
            empresa['logo'], empresa.get('whatsapp_adicional'), True
        ))
        
        empresa_id = cursor.fetchone()[0]
        print(f"   ✅ Empresa ID: {empresa_id}")
        
        # Inserir serviços
        servicos_ids = []
        for idx, (nome, desc, duracao, preco, imagem) in enumerate(empresa['servicos']):
            cursor.execute("""
                INSERT INTO servicos (empresa_id, nome, descricao, duracao_minutos, preco, imagem, ativo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (empresa_id, nome, desc, duracao, preco, imagem, True))
            servico_id = cursor.fetchone()[0]
            servicos_ids.append(servico_id)
            print(f"      ✂️ {nome} - R$ {preco:.2f}")
        
        print(f"   ✅ {len(empresa['servicos'])} serviços criados")
        
        # Inserir atendentes
        atendentes_ids = []
        if 'atendentes' in empresa:
            for idx, atendente in enumerate(empresa['atendentes']):
                cursor.execute("""
                    INSERT INTO atendentes (empresa_id, nome, email, telefone, foto, ativo, ordem_exibicao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    empresa_id, atendente['nome'], atendente['email'], 
                    atendente['telefone'], atendente.get('foto'), True, idx
                ))
                atendente_id = cursor.fetchone()[0]
                atendentes_ids.append(atendente_id)
                
                # Vincular serviços ao atendente
                for servico_idx in atendente['servicos_indices']:
                    if servico_idx < len(servicos_ids):
                        cursor.execute("""
                            INSERT INTO atendente_servicos (atendente_id, servico_id)
                            VALUES (%s, %s)
                        """, (atendente_id, servicos_ids[servico_idx]))
                
                # Criar agenda para o atendente
                inserir_atendente_agenda(cursor, empresa_id, atendente_id, empresa['agenda'])
            
            print(f"   ✅ {len(empresa['atendentes'])} atendentes criados")
        
        # Inserir agenda geral da empresa
        for dia, inicio, fim in empresa['agenda']:
            cursor.execute("""
                INSERT INTO agenda (empresa_id, dia_semana, hora_inicio, hora_fim, intervalo_inicio, intervalo_fim, atendente_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (empresa_id, dia, inicio, fim, "12:00", "13:00", None))
        
        print(f"   ✅ {len(empresa['agenda'])} dias de agenda configurados")
    
    print("\n" + "=" * 80)
    print("✅ TODAS AS 10 EMPRESAS FORAM INSERIDAS COM SUCESSO!")
    print("=" * 80)
    print(f"\n🔐 Senha padrão para todas as empresas: {SENHA_PADRAO}")
    
    print("\n📋 EMPRESAS CADASTRADAS:")
    print("-" * 80)
    
    cursor.execute("""
        SELECT id, nome, email, telefone, segmento, 
               (SELECT COUNT(*) FROM atendentes WHERE empresa_id = empresas.id) as qtd_atendentes,
               (SELECT COUNT(*) FROM servicos WHERE empresa_id = empresas.id) as qtd_servicos,
               cidade, estado
        FROM empresas ORDER BY id
    """)
    empresas_db = cursor.fetchall()
    
    for emp in empresas_db:
        print(f"\n   🏢 ID: {emp[0]} | {emp[1]}")
        print(f"      📧 {emp[2]}")
        print(f"      📞 {emp[3]}")
        print(f"      🏷️  {emp[4]}")
        print(f"      📍 {emp[7]}/{emp[8]}")
        print(f"      👥 Atendentes: {emp[5]} | ✂️ Serviços: {emp[6]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("🎯 LINKS PARA ACESSAR AS EMPRESAS:")
    print("=" * 80)
    for emp in empresas_db:
        print(f"   http://localhost:3000/empresa/{emp[0]} - {emp[1]}")
    
    print(f"\n✨ RESULTADOS:")
    print(f"   ✅ Empresas inseridas: {len(empresas_db)}")
    print(f"   ✅ Total de serviços: {sum(len(emp['servicos']) for emp in empresas)}")
    print(f"   ✅ Total de atendentes: {sum(len(emp.get('atendentes', [])) for emp in empresas)}")
    print(f"   📸 Todas as empresas e serviços com imagens!")
    print(f"   📞 Telefones no formato correto (11 dígitos apenas números)")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()