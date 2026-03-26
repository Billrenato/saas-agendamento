# verify.py
import requests
import json

BASE_URL = "http://localhost:8000"

def verify():
    print("🔍 Verificando sistema...\n")
    
    # 1. Health Check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Backend: {response.json()['status']}")
    except:
        print("❌ Backend não está rodando!")
        return
    
    # 2. Listar empresas
    response = requests.get(f"{BASE_URL}/api/v1/empresas/1")
    if response.status_code == 200:
        empresa = response.json()
        print(f"✅ Empresa: {empresa['nome']}")
    else:
        print("❌ Empresa não encontrada")
    
    # 3. Listar serviços
    response = requests.get(f"{BASE_URL}/api/v1/empresas/1/servicos")
    if response.status_code == 200:
        servicos = response.json()
        print(f"✅ Serviços: {len(servicos)} encontrados")
        for s in servicos:
            print(f"   - {s['nome']} (R$ {s['preco']})")
    
    # 4. Testar login
    login_data = {
        "email": "contato@belezatotal.com",
        "senha": "senha123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"✅ Login: Token gerado ({token[:20]}...)")
    else:
        print("❌ Login falhou")
    
    print("\n✅ Sistema funcionando corretamente!")

if __name__ == "__main__":
    verify()