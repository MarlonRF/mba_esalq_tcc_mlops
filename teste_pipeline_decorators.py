"""
Teste do Pipeline Completo com Decorators
==========================================

Script independente para testar o pipeline_completo_decorators.py
sem problemas de cache do notebook.
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.clearml.pipeline_completo_decorators import executar_pipeline

# Caminho do arquivo CSV
CAMINHO_DADOS = "dados/2025.05.14_thermal_confort_santa_maria_brazil_.csv"

if __name__ == "__main__":
    print("="*80)
    print("TESTE PIPELINE COMPLETO COM @PipelineDecorator")
    print("="*80)
    print(f"\nArquivo CSV: {CAMINHO_DADOS}")
    print("Modo: Execucao LOCAL (com tracking ClearML)\n")
    print("="*80)
    
    # Executar pipeline
    resultado = executar_pipeline(
        caminho_csv=CAMINHO_DADOS,
        run_locally=True
    )
    
    # Exibir resultado
    print("\n" + "="*80)
    print("RESULTADO FINAL")
    print("="*80)
    
    if resultado:
        print(f"\n✓ Pipeline concluido com sucesso!")
        print(f"\nDatasets criados:")
        for key, value in resultado.items():
            if 'dataset' in key:
                print(f"  - {key}: {value}")
        
        print(f"\nModelo:")
        if 'model' in resultado:
            print(f"  - ID: {resultado['model']}")
        
        print(f"\nMetricas:")
        if 'metricas' in resultado:
            for metric, value in resultado['metricas'].items():
                print(f"  - {metric}: {value:.4f}")
    else:
        print("\n✗ Pipeline falhou")
    
    print("\n" + "="*80)
