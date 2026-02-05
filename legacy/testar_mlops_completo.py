#!/usr/bin/env python3
"""
Script de validação completa da solução MLOps.
Testa todo o fluxo: geração do modelo + API + predições.
"""

import os
import sys
import time
import subprocess
import json
from pathlib import Path
import requests
from threading import Thread
import signal

def testar_pipeline_completo():
    """
    Testa o pipeline completo de MLOps.
    """
    print("🚀 Iniciando teste completo da solução MLOps...")
    
    # 1. Executar pipeline de geração do modelo
    print("\n📊 Passo 1: Executando pipelines para gerar modelo...")
    resultado = subprocess.run([
        sys.executable, "executar_pipelines_ci.py"
    ], capture_output=True, text=True, cwd=Path(__file__).parent)
    
    if resultado.returncode != 0:
        print(f"❌ Erro na execução do pipeline:")
        print(resultado.stderr)
        return False
    
    print("✅ Pipeline executado com sucesso")
    
    # 2. Verificar se modelo foi gerado diretamente na pasta api/
    print("\n🔍 Passo 2: Verificando se modelo foi gerado...")
    if not os.path.exists("api/api.pkl"):
        print("❌ Modelo api/api.pkl não foi encontrado")
        return False
    
    print("✅ Modelo api/api.pkl encontrado (salvo diretamente na pasta correta)")
    
    # 3. Iniciar API em background
    print("\n🌐 Passo 3: Iniciando API...")
    api_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app:app", 
        "--host", "127.0.0.1", "--port", "8080"
    ], cwd="api", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Aguardar API ficar pronta
    print("⏳ Aguardando API ficar pronta...")
    for i in range(30):
        try:
            response = requests.get("http://127.0.0.1:8080/", timeout=1)
            if response.status_code == 200:
                print(f"✅ API está respondendo após {i+1}s")
                break
        except:
            time.sleep(1)
    else:
        print("❌ API não respondeu em 30s")
        api_process.terminate()
        return False
    
    try:
        # 4. Testar health check
        print("\n🏥 Passo 4: Testando health check...")
        response = requests.get("http://127.0.0.1:8080/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code != 200:
            print("❌ Health check falhou")
            return False
        
        print("✅ Health check passou")
        
        # 5. Testar predição
        print("\n🧪 Passo 5: Testando predição...")
        dados_teste = {
            "idade": 30,
            "peso": 70.0,
            "altura": 175.0,
            "sexo": "m",
            "temperatura_media": 25.0,
            "umidade_relativa": 60.0,
            "radiacao_solar_media": 400.0
        }
        
        response = requests.post(
            "http://127.0.0.1:8080/predict",
            json=dados_teste,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"Predição: {json.dumps(resultado, indent=2)}")
            print("✅ Predição executada com sucesso")
        else:
            print(f"❌ Erro na predição: {response.text}")
            return False
        
        print("\n🎉 Todos os testes passaram! Solução MLOps funcionando corretamente!")
        return True
        
    finally:
        # 6. Parar API
        print("\n🛑 Parando API...")
        api_process.terminate()
        api_process.wait()
        print("✅ API parada")

if __name__ == "__main__":
    try:
        # Instalar requests se não estiver disponível
        try:
            import requests
        except ImportError:
            print("📦 Instalando requests...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            import requests
        
        sucesso = testar_pipeline_completo()
        
        if sucesso:
            print("\n🏆 TESTE COMPLETO: SUCESSO!")
            print("📋 Resumo:")
            print("  ✅ Pipeline de dados funcionando")
            print("  ✅ Modelo gerado com PyCaret")
            print("  ✅ API FastAPI funcionando")
            print("  ✅ Predições sendo executadas")
            print("  ✅ Solução MLOps completa")
        else:
            print("\n💥 TESTE COMPLETO: FALHOU!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro inesperado: {str(e)}")
        sys.exit(1)