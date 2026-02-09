#!/usr/bin/env python3
"""
Script baseado EXATAMENTE no notebook funcional.
Copia célula por célula sem inventar moda.
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.insert(0, str(Path(__file__).parent))

def executar_pipeline_notebook():
    """
    Executa exatamente como no notebook - células 1, 8, 10
    """
    print(">> Executando pipeline baseado no notebook...")
    
    try:
        # Célula 1: Carregamento dos dados
        print(">> Carregando dados (célula 1)...")
        from utils.io.io_local import load_dataframe
        
        df = load_dataframe('dados/2025.05.14_thermal_confort_santa_maria_brazil_.csv')
        print(f"✅ Dados carregados: {df.shape}")
        
        # Célula 8: Pipeline de processamento  
        print(">> Pipeline processamento (célula 8)...")
        from utils.processamento.pipeline_processamento import pipeline_processamento
        
        substituicoes = {99: 0, 'x': 0, 'F': 'f'}
        
        type_dict = {
            'data': 'datetime64[ns]', 'hora': 'datetime64[ns]', 'idade': 'Int64',
            'sexo': 'string', 'peso': 'Int64', 'altura': 'float64', 'vestimenta': 'string',
            'p1': 'Int64', 'p2': 'Int64', 'p3': 'Int64', 'p4': 'Int64',
            'p5': 'Int64', 'p6': 'Int64', 'p7': 'Int64', 'p8': 'Int64',
            'tev': 'float64', 'utci': 'float64', 'sst': 'float64', 'ste': 'float64',
            'psti': 'float64', 'wbgt': 'float64', 'wci': 'float64', 'tek': 'float64',
            'te': 'float64', 'pst': 'float64', 'tmedia': 'float64', 'tmax': 'float64',
            'tmin': 'float64', 'tu': 'float64', 'ur': 'float64', 'ur_max': 'float64',
            'ur_min': 'float64', 'rsolarmed': 'float64', 'rsolartot': 'float64',
            'vel_vento': 'float64', 'dir_vento': 'float64', 'sd_dirvento': 'float64',
            'vel_vento_max': 'float64', 'dir_max_vento': 'float64', 'chuva_tot': 'float64'
        }
        
        df_bruto = df.copy()
        from clearml.automation import PipelineDecorator
        PipelineDecorator.run_locally()
        
        df_processado = pipeline_processamento(df_bruto, type_dict=type_dict, substituicoes=substituicoes)
        print(f"✅ Processamento concluído: {df_processado.shape}")
        
        # Célula 10: Pipeline de treinamento (EXATAMENTE como no notebook)
        print(">> Pipeline treinamento (célula 10)...")
        from legacy.pipeline_treinamento_antigo import pipeline_treinamento
        
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
        
        PipelineDecorator.run_locally()
        pipeline_treinamento(atributos, coluna_alvo, params)
        print("✅ Treinamento concluído")
        
        # Copiar modelo gerado para api/
        print(">> Copiando modelo para API...")
        import glob
        modelos = glob.glob("modelos/*.pkl")
        if modelos:
            modelo_mais_recente = max(modelos, key=os.path.getctime)
            os.makedirs('api', exist_ok=True)
            import shutil
            shutil.copy2(modelo_mais_recente, "api/api.pkl")
            print(f"✅ Modelo {modelo_mais_recente} copiado para api/api.pkl")
        else:
            print("❌ Nenhum modelo encontrado!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = executar_pipeline_notebook()
    
    if sucesso:
        print("\n🎉 Pipeline do notebook executado com sucesso!")
        print("📁 Modelo api/api.pkl pronto para uso")
    else:
        print("\n💥 Pipeline falhou")
        sys.exit(1)