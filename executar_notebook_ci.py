#!/usr/bin/env python3
"""
Script baseado no Notebook_executar_pipelines.ipynb
Executa exatamente o que funciona no notebook, INCLUINDO ClearML
"""

import sys
import os
import pandas as pd
from utils.io.io_local import load_dataframe
from utils.processamento.pipeline_processamento import pipeline_processamento
from pipelines.pipeline_treinamento_antigo import pipeline_treinamento

# CARREGAR CREDENCIAIS CLEARML DO .env
from dotenv import load_dotenv
load_dotenv()

from clearml.automation import PipelineDecorator

def setup_directories_safe():
    """Configura diretórios necessários com tratamento de erros."""
    directories = ['modelos', 'api', 'logs']
    
    for dir_name in directories:
        try:
            os.makedirs(dir_name, mode=0o755, exist_ok=True)
            print(f"✅ Diretório {dir_name} configurado")
        except (PermissionError, OSError) as e:
            print(f"⚠️ Aviso: {dir_name} - {e}")

def main():
    try:
        print("🚀 Iniciando execução do pipeline MLOps...")
        
        # Configurar diretórios primeiro
        setup_directories_safe()
        
        print("🔄 Executando pipeline de processamento...")
        
        # 1. Carregar dados (célula 1 do notebook)
        df = load_dataframe('dados/2025.05.14_thermal_confort_santa_maria_brazil_.csv')
        print(f"✅ Dados carregados: {len(df)} registros")
        
        # 2. Configurar processamento (célula 9 do notebook - EXATO)
        
        substituicoes = {99:0,
                         'x':0,
                         'F':'f'
                         }
        
        type_dict = {
            'data': 'datetime64[ns]',     # Datas
            'hora': 'datetime64[ns]',     # Horários
            'idade': 'Int64',             # Idades como inteiros (com suporte a NaN)
            'sexo': 'string',             # Sexo como string (categórico)
            'peso': 'Int64',            # Peso como número contínuo
            'altura': 'float64',          # Altura como número contínuo
            'vestimenta': 'string',       # Tipo de vestimenta (categórico)
            'p1': 'Int64',                 # Variáveis numéricas inteiras (suporte a NaN)
            'p2': 'Int64',
            'p3': 'Int64',
            'p4': 'Int64',
            'p5': 'Int64',
            'p6': 'Int64',
            'p7': 'Int64',
            'p8': 'Int64',
            'tev': 'float64',             # Dados contínuos
            'utci': 'float64',
            'sst': 'float64',
            'ste': 'float64',
            'psti': 'float64',
            'wbgt': 'float64',
            'wci': 'float64',
            'tek': 'float64',
            'te': 'float64',
            'pst': 'float64',
            'tmedia': 'float64',
            'tmax': 'float64',
            'tmin': 'float64',
            'tu': 'float64',
            'ur': 'float64',              # Umidade relativa
            'ur_max': 'float64',          # Umidade relativa máxima
            'ur_min': 'float64',          # Umidade relativa mínima
            'rsolarmed': 'float64',       # Radiação solar média
            'rsolartot': 'float64',       # Radiação solar total
            'vel_vento': 'float64',       # Velocidade do vento
            'dir_vento': 'float64',       # Direção do vento
            'sd_dirvento': 'float64',     # Desvio padrão da direção do vento
            'vel_vento_max': 'float64',   # Velocidade máxima do vento
            'dir_max_vento': 'float64',   # Direção máxima do vento
            'chuva_tot': 'float64'        # Total de chuva
        }
        
        df_bruto = df.copy()
        
        # CONFIGURAR CLEARML MODO LOCAL (EXATO COMO NO NOTEBOOK)
        PipelineDecorator.run_locally()
        
        df_processado = pipeline_processamento(df_bruto,
                               type_dict=type_dict,
                               substituicoes=substituicoes)
        
        print(f"✅ Pipeline processamento concluído: {len(df_processado)} registros")
        
        # 3. Configurar treinamento (célula 11 do notebook - EXATO)
        coluna_alvo="sensacao_termica"
        atributos=["sensacao_termica","idade_anos","peso_kg","altura_cm","sexo_biologico",'temperatura_media_c','umidade_relativa_percent','radiacao_solar_media_wm2']

        params = {
             "data": df_processado[atributos],
             "target": coluna_alvo,
             "session_id": 42,
             "normalize": True,
             "fold": 5,
             "verbose": False,
             "html": False,
             "use_gpu": True,
             "log_experiment": False,
         }
        
        # CONFIGURAR CLEARML MODO LOCAL NOVAMENTE (EXATO COMO NO NOTEBOOK)
        PipelineDecorator.run_locally()
        
        # 4. Executar treinamento
        print("🔄 Executando pipeline de treinamento...")
        pipeline_treinamento(atributos, coluna_alvo, params)
        
        # 5. Copiar modelo para pasta da API com fallbacks robustos
        print("🔄 Configurando modelo para API...")
        import shutil
        import glob
        
        modelo_copiado = False
        
        # Lista de possíveis locais do modelo (em ordem de prioridade)
        possiveis_modelos = [
            "api/api.pkl",                    # Se já foi salvo lá
            "api.pkl",                        # Fallback do pipeline  
            "modelo_final.pkl",               # Nome alternativo
        ]
        
        # Adicionar modelos do diretório modelos/ se existir
        if os.path.exists("modelos"):
            modelos_dir = glob.glob("modelos/*.pkl")
            possiveis_modelos.extend(modelos_dir)
        
        # Adicionar qualquer .pkl na raiz
        pkls_raiz = glob.glob("*.pkl")
        possiveis_modelos.extend(pkls_raiz)
        
        # Remover duplicatas mantendo ordem
        possiveis_modelos = list(dict.fromkeys(possiveis_modelos))
        
        print(f"📋 Verificando modelos: {possiveis_modelos}")
        
        for modelo_path in possiveis_modelos:
            if os.path.exists(modelo_path):
                try:
                    # Tentar copiar para api/api.pkl
                    try:
                        os.makedirs("api", mode=0o755, exist_ok=True)
                        destino = "api/api.pkl"
                    except (PermissionError, OSError):
                        # Fallback: deixar na raiz como api.pkl
                        destino = "api.pkl"
                    
                    if modelo_path != destino:
                        shutil.copy2(modelo_path, destino)
                        print(f"✅ Modelo {modelo_path} copiado para {destino}")
                    else:
                        print(f"✅ Modelo já está em {destino}")
                    
                    modelo_copiado = True
                    break
                    
                except (PermissionError, OSError) as e:
                    print(f"⚠️ Erro ao copiar {modelo_path}: {e}")
                    continue
        
        if not modelo_copiado:
            print("❌ ERRO: Nenhum modelo foi encontrado ou pôde ser copiado!")
            print("📂 Conteúdo do diretório atual:")
            for item in os.listdir("."):
                if item.endswith(".pkl"):
                    print(f"   📄 {item}")
            raise FileNotFoundError("Modelo não encontrado para a API")
        
        print("🎉 Script executado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na execução: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)