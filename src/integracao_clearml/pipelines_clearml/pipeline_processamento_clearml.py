"""
Pipeline de Processamento com Integração ClearML.

Este módulo integra o pipeline de processamento local (src/pipelines/pipeline_processamento.py)
com rastreamento e versionamento ClearML.

Melhorias v2.0:
- Usa load_dataframe() de src/utils/io para carregamento robusto
- Detecção automática de delimitador (CSV, TSV, etc.)
- Suporta múltiplos formatos (CSV, Excel, Parquet, Feather, Pickle)
- Tratamento robusto de erros em linhas malformadas
- Resolução inteligente de caminhos (relativo, absoluto, URLs)
- Métricas de entrada/saída registradas no ClearML
"""
from pathlib import Path
from typing import Dict, Any, Optional
from config.logger_config import logger
from config.config_custom import NOME_PROJETO

# Importa utilitário de I/O robusto (src/utils/io)
# - Detecção automática de delimitador
# - Suporta CSV, Excel, Parquet, Feather, Pickle
# - Trata erros de linhas malformadas
from src.utils.io import load_dataframe

# Importa pipeline local (lógica de processamento)
from src.pipelines.pipeline_processamento import executar_pipeline_processamento

# Importa utilitários ClearML modularizados
from src.integracao_clearml.utils.verificador_clearml import obter_clearml_disponivel
from src.integracao_clearml.utils.operacoes_task import criar_task, obter_task_atual
from src.integracao_clearml.utils.operacoes_dataset import criar_dataset
from src.integracao_clearml.utils.integracao_artefatos import registrar_dataframe, registrar_metricas
from src.integracao_clearml.utils.credenciais_clearml import configurar_clearml_online


def executar_pipeline_processamento_clearml(
    caminho_csv: str,
    project_name: Optional[str] = None,
    offline_mode: bool = False
) -> Dict[str, Any]:
    """
    Executa pipeline de processamento com rastreamento ClearML (VERSÃO SIMPLES).
    
    Este pipeline:
    1. Carrega dados do CSV
    2. Executa processamento usando pipeline local
    3. Registra resultado como dataset ClearML (se online)
    
    Args:
        caminho_csv: Caminho para o arquivo CSV de entrada
        project_name: Nome do projeto ClearML (usa NOME_PROJETO se None)
        offline_mode: Se True, executa sem ClearML (apenas processamento)
        
    Returns:
        dict com:
            - dados_processados: DataFrame processado
            - shape: (linhas, colunas)
            - dataset_id: ID do dataset ClearML (None se offline)
            
    Example:
        >>> # Modo online (com ClearML)
        >>> resultado = executar_pipeline_processamento_clearml(
        ...     "dados/arquivo.csv",
        ...     offline_mode=False
        ... )
        
        >>> # Modo offline (sem ClearML)
        >>> resultado = executar_pipeline_processamento_clearml(
        ...     "dados/arquivo.csv",
        ...     offline_mode=True
        ... )
    """
    proj = project_name or NOME_PROJETO
    task = None
    
    # ========== CONFIGURAÇÃO CLEARML ==========
    if not offline_mode and obter_clearml_disponivel():
        logger.info("Modo ONLINE: Iniciando integração ClearML")
        
        # Carregar credenciais do .env
        if not configurar_clearml_online():
            logger.warning("Não foi possível carregar credenciais. Continuando em modo offline.")
            offline_mode = True
        
        if not offline_mode:
            task = criar_task(
                task_name="Pipeline_Processamento",
                project_name=proj,
                task_type="data_processing",
                tags=["processamento", "pipeline"]
            )
        
        if task:
            # Conectar configuração de entrada
            task.connect_configuration({"caminho_csv": caminho_csv})
            logger.info(f"✓ Task ClearML criada (ID: {task.id})")
    else:
        if offline_mode:
            logger.info("Modo OFFLINE: Executando sem rastreamento ClearML")
        else:
            logger.warning("ClearML não disponível. Executando em modo offline.")
    
    # ========== EXECUÇÃO DO PIPELINE LOCAL ==========
    logger.info("="*80)
    logger.info("PIPELINE DE PROCESSAMENTO")
    logger.info("="*80)
    
    logger.info(f"\n[1] Carregando dados do CSV...")
    logger.info(f"    Arquivo: {caminho_csv}")
    
    # Carregar o DataFrame usando função robusta (detecta delimitadores, trata erros, etc.)
    df_raw = load_dataframe(caminho_csv)
    logger.info(f"    ✓ Dados carregados: {df_raw.shape}")
    logger.info(f"    Colunas: {len(df_raw.columns)}")
    
    logger.info(f"\n[2] Executando pipeline de processamento local...")
    
    # Executa o pipeline local (toda a lógica está lá)
    df_processado = executar_pipeline_processamento(df_raw)
    
    logger.info(f"✓ Processamento concluído")
    logger.info(f"  Shape final: {df_processado.shape}")
    
    # ========== REGISTRO DE ARTEFATOS ==========
    dataset_id = None
    
    if task:
        logger.info("\n[3] Registrando artefatos no ClearML...")
        
        # Registrar métricas de processamento
        metricas = {
            "linhas_entrada": df_raw.shape[0],
            "colunas_entrada": df_raw.shape[1],
            "linhas_saida": df_processado.shape[0],
            "colunas_saida": df_processado.shape[1],
            "nas_removidos": int(df_raw.isna().sum().sum() - df_processado.isna().sum().sum())
        }
        registrar_metricas(metricas)
        
        # Registrar DataFrame como artefato (sample para evitar overhead)
        registrar_dataframe(
            df_processado.head(100),
            nome="dados_processados_sample",
            descricao="Amostra dos dados após pipeline de processamento"
        )
        
        logger.info("✓ Artefatos registrados")
        
        # Criar dataset versionado
        logger.info("\n[4] Criando dataset ClearML...")
        dataset = criar_dataset(
            dataset_name="dados_processados",
            description="Dataset após pipeline de processamento",
            tags=["processamento", "limpo"]
        )
        
        if dataset:
            # Salvar DataFrame temporário para upload
            temp_path = Path("temp_dados_processados.parquet")
            df_processado.to_parquet(temp_path, index=False)
            
            dataset.add_files(str(temp_path))
            dataset.upload()
            dataset.finalize()
            
            dataset_id = dataset.id
            logger.info(f"✓ Dataset criado (ID: {dataset_id})")
            
            # Limpar arquivo temporário
            temp_path.unlink()
    
    # ========== FECHAMENTO DA TASK ==========
    # IMPORTANTE: Fechar task para permitir criação de novas tasks em sequência
    if task:
        logger.info("\n[5] Fechando task...")
        task.close()
        logger.info("✓ Task finalizada e pronta para próximo pipeline")
    
    # ========== RESULTADO ==========
    logger.info("\n" + "="*80)
    logger.info("PIPELINE CONCLUÍDO COM SUCESSO")
    logger.info("="*80)
    
    resultado = {
        "dados_processados": df_processado,
        "df_processado": df_processado,  # Alias para compatibilidade
        "shape": df_processado.shape,
        "dataset_id": dataset_id,
        "offline_mode": offline_mode,
        "nas_removidos": int(df_raw.isna().sum().sum() - df_processado.isna().sum().sum())
    }
    
    return resultado


if __name__ == "__main__":
    """
    Exemplo de execução direta do pipeline.
    """
    import sys
    
    # Configuração de exemplo
    caminho_exemplo = "dados/2025.05.14_thermal_confort_santa_maria_brazil_.csv"
    
    # Permite passar caminho via linha de comando
    if len(sys.argv) > 1:
        caminho_exemplo = sys.argv[1]
    
    # Permite passar modo offline via argumento
    offline = "--offline" in sys.argv
    
    print("\n" + "="*80)
    print("EXECUÇÃO DIRETA DO PIPELINE DE PROCESSAMENTO")
    print("="*80)
    print(f"Arquivo: {caminho_exemplo}")
    print(f"Modo: {'OFFLINE' if offline else 'ONLINE (ClearML)'}")
    print("="*80 + "\n")
    
    # Executar pipeline
    resultado = executar_pipeline_processamento_clearml(
        caminho_csv=caminho_exemplo,
        offline_mode=offline
    )
    
    # Exibir resultado
    print("\n" + "="*80)
    print("RESULTADO")
    print("="*80)
    print(f"Shape: {resultado['shape']}")
    print(f"Dataset ID: {resultado['dataset_id']}")
    print("="*80)
