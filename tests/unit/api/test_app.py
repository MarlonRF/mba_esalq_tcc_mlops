"""
Testes para a API FastAPI de conforto térmico.

Testa endpoints, validação de dados e integração com o modelo.
"""

import json

import pytest
from fastapi.testclient import TestClient


class TestAPIConfortoTermico:
    """Testes para API de predição de conforto térmico"""

    @pytest.fixture(scope="class")
    def client(self):
        """Fixture para cliente de teste da API"""
        # Garantir que existe um modelo para teste
        import os
        import sys
        if not os.path.exists("api.pkl"):
            # Se não existir, cria modelo simples
            import subprocess
            # Usar caminho completo do Python para segurança
            python_executable = sys.executable
            try:
                subprocess.run([python_executable, "criar_modelo_teste.py"], 
                             check=True, capture_output=True, text=True, timeout=60)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                print(f"Erro ao criar modelo de teste: {e}")
                # Continua sem modelo para teste básico da API
        
        from api.app import app
        return TestClient(app)

    @pytest.mark.api
    def test_health_check(self, client):
        """Testa endpoint de health check"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert data["message"] == "Thermal Comfort API is running!"

    @pytest.mark.api
    def test_predicao_dados_validos(self, client):
        """Testa predição com dados válidos"""
        dados_teste = {
            "idade_anos": 30,
            "peso_kg": 70.0,
            "altura_cm": 175,
            "sexo_biologico": "m",
            "temperatura_media_c": 25.0,
            "umidade_relativa_percent": 60.0,
            "radiacao_solar_media_wm2": 400.0,
        }

        response = client.post("/predict", json=dados_teste)
        assert response.status_code == 200

        data = response.json()
        assert "prediction" in data

        # Verifica se predição é uma string válida
        assert isinstance(data["prediction"], str)
        assert len(data["prediction"]) > 0

    @pytest.mark.api
    def test_predicao_dados_invalidos(self, client):
        """Testa predição com dados inválidos"""
        # Dados com campos faltando
        dados_incompletos = {
            "idade_anos": 30,
            "peso_kg": 70.0,
            # Faltam outros campos obrigatórios
        }

        response = client.post("/predict", json=dados_incompletos)
        assert response.status_code == 422  # Unprocessable Entity

    @pytest.mark.api
    def test_predicao_valores_extremos(self, client):
        """Testa predição com valores nos extremos"""
        dados_extremos = {
            "idade_anos": 18,  # Mínimo
            "peso_kg": 40.0,  # Baixo
            "altura_cm": 150,  # Baixo
            "sexo_biologico": "f",
            "temperatura_media_c": 45.0,  # Alto
            "umidade_relativa_percent": 95.0,  # Alto
            "radiacao_solar_media_wm2": 1000.0,  # Alto
        }

        response = client.post("/predict", json=dados_extremos)
        # Deve processar mesmo com valores extremos
        assert response.status_code == 200

        data = response.json()
        assert "prediction" in data

    @pytest.mark.api
    def test_predicao_tipos_incorretos(self, client):
        """Testa predição com tipos de dados incorretos"""
        dados_tipos_errados = {
            "idade_anos": "trinta",  # String ao invés de int
            "peso_kg": 70.0,
            "altura_cm": 175,
            "sexo_biologico": "m",
            "temperatura_media_c": 25.0,
            "umidade_relativa_percent": 60.0,
            "radiacao_solar_media_wm2": 400.0,
        }

        response = client.post("/predict", json=dados_tipos_errados)
        assert response.status_code == 422  # Validation error

    @pytest.mark.api
    def test_endpoint_inexistente(self, client):
        """Testa acesso a endpoint que não existe"""
        response = client.get("/endpoint_que_nao_existe")
        assert response.status_code == 404

    @pytest.mark.api
    def test_metodo_nao_permitido(self, client):
        """Testa método HTTP não permitido"""
        # GET no endpoint que só aceita POST
        response = client.get("/predict")
        assert response.status_code == 405  # Method Not Allowed
