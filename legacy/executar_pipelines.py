#!/usr/bin/env python3
"""
Script de execução dos pipelines baseado no notebook funcional.
Rep        # 6. Verificação do modelo gerado
        print("🔍 Verificando modelo gerado...")
        
        # Procura pelo modelo mais recente na pasta modelos
        import glob
        modelos_encontrados = glob.glob("modelos/*.pkl")
        
        if modelos_encontrados:
            modelo_mais_recente = max(modelos_encontrados, key=os.path.getctime)
            print(f"✅ Modelo encontrado: {modelo_mais_recente}")
            
            # Cria diretório api se não existir
            os.makedirs('api', exist_ok=True)
            
            # Copia diretamente para a pasta api/
            import shutil
            shutil.copy2(modelo_mais_recente, "api/api.pkl")
            print("✅ Modelo copiado para api/api.pkl")
        else:
            print("⚠️ Nenhum modelo encontrado na pasta modelos")
            return Falsestado e aprovado.
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.insert(0, str(Path(__file__).parent))

def executar_pipelines_completos():
    """
    Executa a sequência completa seguindo o padrão do notebook.
    """
    print("🚀 Iniciando execução dos pipelines...")
    
    try:
        # 1. Importações (igual ao notebook)
        print("� Importando módulos...")
        from utils.io.io_local import load_dataframe
        from utils.processamento.pipeline_processamento import pipeline_processamento
        from legacy.pipeline_treinamento_antigo import pipeline_treinamento
        from clearml.automation import PipelineDecorator
        
        # Configura ClearML para execução local (evita conexão remota)
        PipelineDecorator.run_locally()
        print("✅ ClearML configurado para execução local")
        
        # 2. Carregamento dos dados
        print("📊 Carregando dados...")
        arquivo_dados = "dados/2025.05.14_thermal_confort_santa_maria_brazil_.csv"
        if not os.path.exists(arquivo_dados):
            raise FileNotFoundError(f"Arquivo de dados não encontrado: {arquivo_dados}")
        
        df = load_dataframe(arquivo_dados)
        print(f"✅ Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
        
        # 3. Configurações (igual ao notebook)
        print("⚙️ Configurando parâmetros...")
        substituicoes = {99: 0, 'x': 0, 'F': 'f'}
        
        type_dict = {
            'data': 'datetime64[ns]',
            'hora': 'datetime64[ns]',
            'idade': 'Int64',
            'sexo': 'string',
            'peso': 'Int64',
            'altura': 'float64',
            'vestimenta': 'string',
            'p1': 'Int64', 'p2': 'Int64', 'p3': 'Int64', 'p4': 'Int64',
            'p5': 'Int64', 'p6': 'Int64', 'p7': 'Int64', 'p8': 'Int64',
            'tev': 'float64', 'utci': 'float64', 'sst': 'float64',
            'ste': 'float64', 'psti': 'float64', 'wbgt': 'float64',
            'wci': 'float64', 'tek': 'float64', 'te': 'float64',
            'pst': 'float64', 'tmedia': 'float64', 'tmax': 'float64',
            'tmin': 'float64', 'tu': 'float64', 'ur': 'float64',
            'ur_max': 'float64', 'ur_min': 'float64', 'rsolarmed': 'float64',
            'rsolartot': 'float64', 'vel_vento': 'float64', 'dir_vento': 'float64',
            'sd_dirvento': 'float64', 'vel_vento_max': 'float64',
            'dir_max_vento': 'float64', 'chuva_tot': 'float64'
        }
        
        # 4. Pipeline de processamento (igual ao notebook)
        print("⚙️ Executando pipeline de processamento...")
        df_bruto = df.copy()
        df_processado = pipeline_processamento(df_bruto,
                                            type_dict=type_dict,
                                            substituicoes=substituicoes)
        print(f"✅ Processamento concluído: {df_processado.shape}")
        
        # 5. Pipeline de treinamento (igual ao notebook)
        print("🤖 Executando pipeline de treinamento...")
        coluna_alvo = "sensacao_termica"
        atributos = ["sensacao_termica", "idade_anos", "peso_kg", "altura_cm", 
                    "sexo_biologico", 'temperatura_media_c', 'umidade_relativa_percent', 
                    'radiacao_solar_media_wm2']
        
        params = {
            "data": df_processado[atributos],
            "target": coluna_alvo,
            "session_id": 42,
            "normalize": True,
            "fold": 5,
            "verbose": False,
            "html": False,
            "use_gpu": False,  # False para CI/CD
            "log_experiment": False,
        }
        
        # Executa o pipeline de treinamento
        pipeline_treinamento(atributos, coluna_alvo, params)
        print("✅ Pipeline de treinamento concluído")
        
        # 6. Verificação do modelo gerado
        print("� Verificando modelo gerado...")
        
        # Procura pelo modelo mais recente na pasta modelos
        import glob
        modelos_encontrados = glob.glob("modelos/*.pkl")
        
        if modelos_encontrados:
            modelo_mais_recente = max(modelos_encontrados, key=os.path.getctime)
            print(f"✅ Modelo encontrado: {modelo_mais_recente}")
            
            # Copia para api.pkl para a API funcionar
            import shutil
            shutil.copy2(modelo_mais_recente, "api.pkl")
            print("✅ Modelo copiado para api.pkl")
        else:
            print("⚠️ Nenhum modelo encontrado na pasta modelos")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na execução dos pipelines: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = executar_pipelines_completos()
    
    if sucesso:
        print("\n🎉 Pipelines executados com sucesso!")
        print("📁 Modelo api/api.pkl gerado e pronto para uso na API")
    else:
        print("\n💥 Falha na execução dos pipelines")
        sys.exit(1)