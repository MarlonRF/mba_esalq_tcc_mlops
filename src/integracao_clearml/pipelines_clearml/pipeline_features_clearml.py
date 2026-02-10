"""
Pipeline de Engenharia de Features com Integração ClearML.

Este módulo integra o pipeline de features local (src/pipelines/pipeline_features.py)
com rastreamento e versionamento ClearML.

Versão Simples: Focado em executar o pipeline e registrar artefatos.
"""
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, List
import json
from config.logger_config import logger
from config.config_custom import NOME_PROJETO, COLUNAS_CATEGORICAS, TIPOS_FEATURES_DERIVADAS

# Importa pipeline local (lógica de features)
from src.pipelines.pipeline_features import executar_pipeline_features

# Importa utilitários ClearML modularizados
from src.integracao_clearml.utils.verificador_clearml import obter_clearml_disponivel
from src.integracao_clearml.utils.operacoes_task import criar_task, obter_task_atual
from src.integracao_clearml.utils.operacoes_dataset import criar_dataset
from src.integracao_clearml.utils.integracao_artefatos import (
    registrar_arquivo,
    registrar_dataframe,
    registrar_metricas,
)
from src.integracao_clearml.utils.credenciais_clearml import configurar_clearml_online


def executar_pipeline_features_clearml(
    df_processado: pd.DataFrame,
    dataset_processado_id: Optional[str] = None,
    project_name: Optional[str] = None,
    offline_mode: bool = False,
    # Parâmetros do pipeline local
    colunas_categoricas: Optional[List[str]] = None,
    aplicar_codificacao: bool = True,
    metodo_codificacao: str = "label",
    aplicar_normalizacao: bool = True,
    metodo_normalizacao: str = "standard",
    criar_features_derivadas: bool = True,
    tipos_features_derivadas: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Executa pipeline de features com rastreamento ClearML (VERSÃO SIMPLES).
    
    Este pipeline:
    1. Recebe DataFrame processado
    2. Executa engenharia de features usando pipeline local
    3. Registra resultado e artefatos como dataset ClearML (se online)
    
    Args:
        df_processado: DataFrame já processado (saída do pipeline de processamento)
        dataset_processado_id: ID do dataset processado (para rastreamento)
        project_name: Nome do projeto ClearML (usa NOME_PROJETO se None)
        offline_mode: Se True, executa sem ClearML (apenas features)
        colunas_categoricas: Colunas categóricas para codificar (usa config se None)
        aplicar_codificacao: Se deve aplicar codificação categórica
        metodo_codificacao: Método de codificação ('label' ou 'onehot')
        aplicar_normalizacao: Se deve aplicar normalização
        metodo_normalizacao: Método de normalização ('standard', 'minmax', 'robust')
        criar_features_derivadas: Se deve criar features derivadas (IMC, heat index, etc)
        tipos_features_derivadas: Tipos de features derivadas (usa config se None)
        
    Returns:
        dict com:
            - dados_features: DataFrame com features
            - artefatos: Dict com mapeamentos e metadados
            - shape: (linhas, colunas)
            - dataset_id: ID do dataset ClearML (None se offline)
            
    Example:
        >>> # Modo online (com ClearML)
        >>> resultado = executar_pipeline_features_clearml(
        ...     df_processado=df,
        ...     offline_mode=False
        ... )
        
        >>> # Modo offline (sem ClearML)
        >>> resultado = executar_pipeline_features_clearml(
        ...     df_processado=df,
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
                task_name="Pipeline_Features",
                project_name=proj,
                task_type="data_processing",
                tags=["features", "pipeline"]
            )
        
        if task:
            # Conectar configuração de entrada
            configuracao = {
                "dataset_processado_id": dataset_processado_id,
                "shape_entrada": df_processado.shape,
                "aplicar_codificacao": aplicar_codificacao,
                "metodo_codificacao": metodo_codificacao,
                "aplicar_normalizacao": aplicar_normalizacao,
                "metodo_normalizacao": metodo_normalizacao,
                "criar_features_derivadas": criar_features_derivadas,
            }
            task.connect_configuration(configuracao)
            logger.info(f"✓ Task ClearML criada (ID: {task.id})")
    else:
        if offline_mode:
            logger.info("Modo OFFLINE: Executando sem rastreamento ClearML")
        else:
            logger.warning("ClearML não disponível. Executando em modo offline.")
    
    # ========== EXECUÇÃO DO PIPELINE LOCAL ==========
    logger.info("="*80)
    logger.info("PIPELINE DE ENGENHARIA DE FEATURES")
    logger.info("="*80)
    
    logger.info(f"\n[1] Executando pipeline de features local...")
    logger.info(f"    Shape entrada: {df_processado.shape}")
    
    # Usar configurações padrão se não fornecidas
    colunas_categoricas = colunas_categoricas or COLUNAS_CATEGORICAS
    tipos_features_derivadas = tipos_features_derivadas or TIPOS_FEATURES_DERIVADAS
    
    # Executa o pipeline local (toda a lógica está lá)
    df_features, artefatos = executar_pipeline_features(
        df=df_processado,
        colunas_categoricas=colunas_categoricas,
        aplicar_codificacao=aplicar_codificacao,
        metodo_codificacao=metodo_codificacao,
        aplicar_normalizacao=aplicar_normalizacao,
        metodo_normalizacao=metodo_normalizacao,
        criar_features_derivadas=criar_features_derivadas,
        tipos_features_derivadas=tipos_features_derivadas,
    )
    
    logger.info(f"✓ Features criadas com sucesso")
    logger.info(f"  Shape final: {df_features.shape}")
    logger.info(f"  Novas colunas: {df_features.shape[1] - df_processado.shape[1]}")
    
    # ========== REGISTRO DE ARTEFATOS ==========
    dataset_id = None
    
    if task:
        logger.info("\n[2] Registrando artefatos no ClearML...")
        
        # Registrar DataFrame com features
        registrar_dataframe(
            df_features,
            nome="dados_features",
            descricao="Dados após engenharia de features"
        )
        
        # Registrar artefatos (mapeamentos, colunas criadas, etc)
        if artefatos:
            # Salvar artefatos como JSON temporário
            artefatos_serializaveis = {}
            for chave, valor in artefatos.items():
                if isinstance(valor, (dict, list)):
                    artefatos_serializaveis[chave] = valor
                else:
                    artefatos_serializaveis[chave] = str(valor)
            
            temp_artefatos = Path("temp_artefatos_features.json")
            with open(temp_artefatos, 'w', encoding='utf-8') as f:
                json.dump(artefatos_serializaveis, f, indent=2, ensure_ascii=False)
            
            registrar_arquivo(temp_artefatos, "artefatos_features")
            temp_artefatos.unlink()
            
            logger.info(f"  Artefatos registrados: {list(artefatos.keys())}")
        
        # Registrar métricas básicas
        metricas = {
            "linhas_features": df_features.shape[0],
            "colunas_features": df_features.shape[1],
            "novas_colunas": df_features.shape[1] - df_processado.shape[1],
            "colunas_entrada": df_processado.shape[1],
        }
        registrar_metricas(metricas)
        
        logger.info("✓ Artefatos registrados")
        
        # Criar dataset versionado
        logger.info("\n[3] Criando dataset ClearML...")
        dataset = criar_dataset(
            dataset_name="dados_features",
            description="Dataset após engenharia de features",
            tags=["features", "transformado"],
            parent_dataset_id=dataset_processado_id  # Vincula ao dataset anterior
        )
        
        if dataset:
            # Salvar DataFrame temporário para upload
            temp_path = Path("temp_dados_features.parquet")
            df_features.to_parquet(temp_path, index=False)
            
            dataset.add_files(str(temp_path))
            dataset.upload()
            dataset.finalize()
            
            dataset_id = dataset.id
            logger.info(f"✓ Dataset criado (ID: {dataset_id})")
            
            # Limpar arquivo temporário
            temp_path.unlink()
    
    # ========== RESULTADO ==========
    logger.info("\n" + "="*80)
    logger.info("PIPELINE DE FEATURES CONCLUÍDO COM SUCESSO")
    logger.info("="*80)
    
    resultado = {
        "dados_features": df_features,
        "artefatos": artefatos,
        "shape": df_features.shape,
        "dataset_id": dataset_id,
    }
    
    return resultado


if __name__ == "__main__":
    """
    Exemplo de execução direta do pipeline.
    """
    import sys
    
    print("\n" + "="*80)
    print("EXECUÇÃO DIRETA DO PIPELINE DE FEATURES")
    print("="*80)
    print("NOTA: Este pipeline requer dados processados como entrada.")
    print("Execute primeiro: pipeline_processamento_clearml.py")
    print("="*80 + "\n")
    
    # Para teste, criar dados sintéticos
    print("Criando dados sintéticos para demonstração...")
    
    df_exemplo = pd.DataFrame({
        'idade': [25, 30, 35, 40],
        'peso': [70, 80, 75, 85],
        'altura': [1.75, 1.80, 1.70, 1.85],
        'sexo': ['m', 'f', 'm', 'f'],
        'vestimenta': ['leve', 'media', 'leve', 'pesada'],
        'tmedia': [25.0, 30.0, 28.0, 22.0],
        'ur': [60.0, 70.0, 65.0, 55.0],
    })
    
    offline = "--offline" in sys.argv
    
    print(f"\nModo: {'OFFLINE' if offline else 'ONLINE (ClearML)'}\n")
    
    # Executar pipeline
    resultado = executar_pipeline_features_clearml(
        df_processado=df_exemplo,
        offline_mode=offline,
        criar_features_derivadas=True
    )
    
    # Exibir resultado
    print("\n" + "="*80)
    print("RESULTADO")
    print("="*80)
    print(f"Shape entrada: {df_exemplo.shape}")
    print(f"Shape saída: {resultado['shape']}")
    print(f"Novas colunas: {resultado['shape'][1] - df_exemplo.shape[1]}")
    print(f"Dataset ID: {resultado['dataset_id']}")
    print(f"Artefatos: {list(resultado['artefatos'].keys())}")
    print("="*80)
