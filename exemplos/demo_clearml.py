"""
Script de demonstração do módulo ClearML.

Demonstra o uso dos 3 pipelines ClearML:
- pipeline_processamento_clearml
- pipeline_treinamento_clearml  
- pipeline_completo_clearml

Execute este arquivo para ver exemplos de uso.
"""
import pandas as pd
from pathlib import Path

# Configuração
from config.logger_config import logger
from config import config_gerais as config

# Módulo ClearML
from src.integracao_clearml import (
    # Configuração
    configure_local_execution,
    
    # Pipelines
    pipeline_processamento_clearml,
    pipeline_treinamento_clearml,
    pipeline_completo_clearml,
    
    # Standalone
    executar_pipeline_processamento_clearml_standalone,
    executar_pipeline_treinamento_clearml_standalone,
    executar_pipeline_completo_clearml_standalone,
    
    # Utilitários
    verificar_disponibilidade,
    obter_resumo_configuracao,
)


def exemplo_1_verificar_clearml():
    """Exemplo 1: Verificar disponibilidade e configuração do ClearML."""
    print("\n" + "=" * 80)
    print("EXEMPLO 1: Verificar ClearML")
    print("=" * 80)
    
    # Verifica se ClearML está disponível
    disponivel = verificar_disponibilidade()
    print(f"ClearML disponível: {disponivel}")
    
    # Obtém resumo de configuração
    resumo = obter_resumo_configuracao()
    print(f"\nConfiguração:\n{resumo}")


def exemplo_2_pipeline_processamento():
    """Exemplo 2: Executar pipeline de processamento localmente."""
    print("\n" + "=" * 80)
    print("EXEMPLO 2: Pipeline de Processamento")
    print("=" * 80)
    
    # Configura para execução local (sem envio para servidor ClearML)
    configure_local_execution()
    
    # Carrega dados brutos
    caminho_dados = Path(config.CAMINHO_DADOS_ENTRADA)
    if not caminho_dados.exists():
        print(f"Arquivo não encontrado: {caminho_dados}")
        return
    
    df_bruto = pd.read_csv(caminho_dados)
    print(f"Dados carregados: {df_bruto.shape}")
    
    # Executa pipeline de processamento
    df_processado = pipeline_processamento_clearml(df_bruto)
    print(f"Dados processados: {df_processado.shape}")
    
    return df_processado


def exemplo_3_pipeline_treinamento(df_processado: pd.DataFrame):
    """Exemplo 3: Executar pipeline de treinamento."""
    print("\n" + "=" * 80)
    print("EXEMPLO 3: Pipeline de Treinamento")
    print("=" * 80)
    
    # Configura para execução local
    configure_local_execution()
    
    # Executa pipeline de treinamento
    resultado = pipeline_treinamento_clearml(
        df=df_processado,
        coluna_alvo="target",
        tipo_problema="classificacao",
        n_select=2,  # Seleciona 2 melhores modelos
        otimizar_melhor=False,  # Sem otimização para demo rápido
        salvar_modelo_final=False,  # Não salva para demo
    )
    
    print(f"\nMelhor modelo: {type(resultado['melhor_modelo']).__name__}")
    print(f"Métricas: {resultado['metricas']}")
    
    return resultado


def exemplo_4_pipeline_completo():
    """Exemplo 4: Executar pipeline completo end-to-end."""
    print("\n" + "=" * 80)
    print("EXEMPLO 4: Pipeline Completo End-to-End")
    print("=" * 80)
    
    # Configura para execução local
    configure_local_execution()
    
    # Carrega dados brutos
    caminho_dados = Path(config.CAMINHO_DADOS_ENTRADA)
    if not caminho_dados.exists():
        print(f"Arquivo não encontrado: {caminho_dados}")
        return
    
    df_bruto = pd.read_csv(caminho_dados)
    print(f"Dados carregados: {df_bruto.shape}")
    
    # Executa pipeline completo
    resultado = pipeline_completo_clearml(
        df_bruto=df_bruto,
        coluna_alvo="target",
        tipo_problema="classificacao",
        realizar_engenharia_features=True,
        dividir_treino_teste=True,
        test_size=0.2,
        otimizar_melhor=False,  # Sem otimização para demo rápido
        validacao_final=True,
        salvar_modelo=False,  # Não salva para demo
        n_select=2,
    )
    
    print(f"\nMelhor modelo: {type(resultado['modelo_final']).__name__}")
    print(f"Métricas CV: {resultado['metricas_cv']}")
    if 'metricas_teste' in resultado:
        print(f"Métricas Teste: {resultado['metricas_teste']}")
    
    return resultado


def exemplo_5_pipeline_standalone_com_dataset():
    """Exemplo 5: Executar pipeline standalone com dataset do ClearML."""
    print("\n" + "=" * 80)
    print("EXEMPLO 5: Pipeline Standalone com ClearML Dataset")
    print("=" * 80)
    
    print("\nEste exemplo requer:")
    print("1. ClearML configurado (credenciais)")
    print("2. Dataset publicado no ClearML")
    print("\nPara executar:")
    print("  dataset_id = 'seu_dataset_id'")
    print("  resultado = executar_pipeline_completo_clearml_standalone(")
    print("      dataset_id=dataset_id,")
    print("      coluna_alvo='target',")
    print("      tipo_problema='classificacao'")
    print("  )")


def exemplo_6_uso_com_context_manager():
    """Exemplo 6: Uso com context manager ClearMLContext."""
    print("\n" + "=" * 80)
    print("EXEMPLO 6: Uso com Context Manager")
    print("=" * 80)
    
    from src.integracao_clearml import ClearMLContext
    
    # Context manager para gerenciamento automático de task
    with ClearMLContext(
        task_name="Demo_Context_Manager",
        project="conforto_termico",
        task_type="testing"
    ) as ctx:
        # Código dentro do contexto é rastreado automaticamente
        print("Task ClearML criada automaticamente")
        
        # Log de parâmetros
        ctx.log_parameters({"param1": 10, "param2": "teste"})
        
        # Log de métricas
        ctx.log_metric("demo", "valor", 0.95)
        
        # Executa algum processamento
        resultado = sum(range(1000))
        
        # Log de artefato
        ctx.log_artifact("resultado", resultado)
        
    print("Task finalizada automaticamente ao sair do contexto")


def main():
    """Função principal com menu de exemplos."""
    print("\n" + "=" * 80)
    print("DEMONSTRAÇÃO DO MÓDULO CLEARML")
    print("=" * 80)
    print("\nEste script demonstra o uso dos pipelines ClearML.")
    print("Os exemplos executam em modo LOCAL (sem envio para servidor).\n")
    
    # Exemplo 1: Verificar ClearML
    exemplo_1_verificar_clearml()
    
    # Menu de exemplos
    print("\n" + "=" * 80)
    print("EXEMPLOS DISPONÍVEIS:")
    print("=" * 80)
    print("2. Pipeline de Processamento")
    print("3. Pipeline de Treinamento")
    print("4. Pipeline Completo End-to-End")
    print("5. Pipeline Standalone com Dataset ClearML")
    print("6. Uso com Context Manager")
    print("=" * 80)
    
    # Para demo, executa apenas verificação
    # Para executar outros exemplos, descomente abaixo:
    
    # df_processado = exemplo_2_pipeline_processamento()
    # if df_processado is not None:
    #     exemplo_3_pipeline_treinamento(df_processado)
    
    # exemplo_4_pipeline_completo()
    # exemplo_5_pipeline_standalone_com_dataset()
    # exemplo_6_uso_com_context_manager()
    
    print("\n" + "=" * 80)
    print("DEMONSTRAÇÃO CONCLUÍDA")
    print("=" * 80)
    print("\nPara executar outros exemplos, edite este arquivo e descomente")
    print("as linhas correspondentes na função main().")
    print("\nDOCUMENTAÇÃO COMPLETA: src/integracao_clearml/README.MD")


if __name__ == "__main__":
    main()
