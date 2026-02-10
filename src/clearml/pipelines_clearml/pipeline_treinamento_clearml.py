"""
Pipeline de Treinamento com Integração ClearML.

Este módulo integra o pipeline de treinamento local (src/pipelines/pipeline_treinamento_unified.py)
com rastreamento e versionamento ClearML.

Melhorias v1.0:
- Integração com PyCaret (classificação e regressão)
- Registro automático de métricas no ClearML
- Upload do modelo treinado
- Registro de artefatos (tabelas de comparação, plots)
- Genealogia completa: dados → features → modelo
"""
from pathlib import Path
from typing import Dict, Any, Optional, List, Literal
import pandas as pd
from config.logger_config import logger
from config.config_custom import NOME_PROJETO
from config.config_gerais import METRICAS_CLASSIFICACAO, METRICAS_REGRESSAO

# Importa pipeline local (lógica de treinamento)
from src.pipelines.pipeline_treinamento_unified import treinar_pipeline_completo

# Importa utilitários ClearML modularizados
from src.clearml.utils.verificador_clearml import obter_clearml_disponivel
from src.clearml.utils.operacoes_task import criar_task, obter_task_atual
from src.clearml.utils.integracao_artefatos import registrar_dataframe, registrar_metricas
from src.clearml.utils.credenciais_clearml import configurar_clearml_online

# Tipo literal
TipoProblema = Literal["classificacao", "regressao"]


def executar_pipeline_treinamento_clearml(
    df_features: pd.DataFrame,
    coluna_alvo: str,
    tipo_problema: TipoProblema,
    dataset_features_id: Optional[str] = None,
    project_name: Optional[str] = None,
    offline_mode: bool = False,
    # Parâmetros do pipeline de treinamento
    params_setup: Optional[Dict] = None,
    n_modelos_comparar: int = 3,
    modelos_incluir: Optional[List[str]] = None,
    modelos_excluir: Optional[List[str]] = None,
    metrica_ordenacao: Optional[str] = None,
    otimizar_hiperparametros: bool = True,
    n_iter_otimizacao: int = 10,
    salvar_modelo_final: bool = True,
    nome_modelo: str = "modelo_conforto_termico",
    pasta_modelos: str = "modelos",
) -> Dict[str, Any]:
    """
    Executa pipeline de treinamento com rastreamento ClearML.
    
    Este pipeline:
    1. Recebe DataFrame com features
    2. Executa treinamento usando pipeline local (PyCaret)
    3. Registra métricas, modelo e artefatos no ClearML (se online)
    
    Args:
        df_features: DataFrame com features (saída do pipeline de features)
        coluna_alvo: Nome da coluna target
        tipo_problema: 'classificacao' ou 'regressao'
        dataset_features_id: ID do dataset de features (para rastreamento)
        project_name: Nome do projeto ClearML (usa NOME_PROJETO se None)
        offline_mode: Se True, executa sem ClearML (apenas treinamento)
        params_setup: Parâmetros para PyCaret.setup
        n_modelos_comparar: Quantos modelos comparar
        modelos_incluir: Lista de modelos para incluir
        modelos_excluir: Lista de modelos para excluir
        metrica_ordenacao: Métrica para ordenar modelos
        otimizar_hiperparametros: Se deve otimizar hiperparâmetros
        n_iter_otimizacao: Número de iterações de otimização
        salvar_modelo_final: Se deve salvar modelo em disco
        nome_modelo: Nome do modelo a salvar
        pasta_modelos: Pasta para salvar modelo
        
    Returns:
        dict com:
            - melhor_modelo: Modelo treinado
            - metricas_melhor: Dict com métricas do melhor modelo
            - tabela_comparacao: DataFrame com comparação de modelos
            - caminho_modelo: Path do modelo salvo (se salvo)
            - model_id: ID do modelo no ClearML (None se offline)
            - offline_mode: bool
            
    Example:
        >>> # Modo online (com ClearML)
        >>> resultado = executar_pipeline_treinamento_clearml(
        ...     df_features=df,
        ...     coluna_alvo='target',
        ...     tipo_problema='regressao',
        ...     offline_mode=False
        ... )
        
        >>> # Modo offline (sem ClearML)
        >>> resultado = executar_pipeline_treinamento_clearml(
        ...     df_features=df,
        ...     coluna_alvo='target',
        ...     tipo_problema='classificacao',
        ...     offline_mode=True
        ... )
    """
    
    # ========== CONFIGURAÇÃO INICIAL ==========
    project_name = project_name or NOME_PROJETO
    task = None
    model_id = None
    
    # ========== VERIFICAÇÃO CLEARML ==========
    if not offline_mode:
        logger.info("Modo ONLINE: Iniciando integração ClearML")
        
        # Carregar credenciais do .env
        configurar_clearml_online()
        
        # Verificar disponibilidade
        if not obter_clearml_disponivel():
            logger.warning("ClearML não disponível. Continuando em modo offline.")
            offline_mode = True
    else:
        logger.info("Modo OFFLINE: Executando sem ClearML")
    
    # ========== CRIAÇÃO DA TASK ==========
    if not offline_mode:
        task = criar_task(
            task_name="Pipeline_Treinamento",
            project_name=project_name,
            task_type="training"
        )
        
        if task:
            # Conectar configurações
            config = {
                "coluna_alvo": coluna_alvo,
                "tipo_problema": tipo_problema,
                "n_modelos_comparar": n_modelos_comparar,
                "otimizar_hiperparametros": otimizar_hiperparametros,
                "n_iter_otimizacao": n_iter_otimizacao,
            }
            
            if dataset_features_id:
                config["dataset_features_id"] = dataset_features_id
            
            task.connect_configuration(config)
            logger.info(f"✓ Task ClearML criada (ID: {task.id})")
    
    # ========== PIPELINE DE TREINAMENTO ==========
    logger.info("="*80)
    logger.info("PIPELINE DE TREINAMENTO")
    logger.info("="*80)
    
    logger.info(f"\n[1] Executando pipeline de treinamento local...")
    logger.info(f"    Shape entrada: {df_features.shape}")
    logger.info(f"    Coluna alvo: {coluna_alvo}")
    logger.info(f"    Tipo: {tipo_problema}")
    
    # Executa o pipeline local (toda a lógica está lá)
    resultado = treinar_pipeline_completo(
        dados=df_features,
        coluna_alvo=coluna_alvo,
        tipo_problema=tipo_problema,
        params_setup=params_setup,
        n_modelos_comparar=n_modelos_comparar,
        modelos_incluir=modelos_incluir,
        modelos_excluir=modelos_excluir,
        metrica_ordenacao=metrica_ordenacao,
        otimizar_hiperparametros=otimizar_hiperparametros,
        n_iter_otimizacao=n_iter_otimizacao,
        finalizar=True,
        salvar_modelo_final=salvar_modelo_final,
        nome_modelo=nome_modelo,
        pasta_modelos=pasta_modelos,
    )
    
    logger.info(f"✓ Treinamento concluído")
    
    # Extrair nome do melhor modelo
    melhor_modelo_nome = str(resultado['tabela_comparacao'].index[0])
    logger.info(f"  Melhor modelo: {melhor_modelo_nome}")
    
    # ========== REGISTRO DE ARTEFATOS ==========
    if task:
        logger.info("\n[2] Registrando artefatos no ClearML...")
        
        # Registrar métricas do melhor modelo
        metricas = resultado['metricas_melhor']
        registrar_metricas(metricas)
        
        # Registrar tabela de comparação como artefato
        registrar_dataframe(
            resultado['tabela_comparacao'],
            nome="comparacao_modelos",
            descricao="Tabela com comparação de todos os modelos testados"
        )
        
        logger.info("✓ Artefatos registrados")
        
        # ========== REGISTRO DO MODELO ==========
        logger.info("\n[3] Registrando modelo no ClearML...")
        
        try:
            from clearml import OutputModel
            
            output_model = OutputModel(
                task=task,
                name=f"modelo_{melhor_modelo_nome}_{nome_modelo}",
                framework="PyCaret"
            )
            
            # Labels do modelo
            output_model.update_labels({
                "tipo": tipo_problema,
                "coluna_alvo": coluna_alvo,
                "melhor_modelo": melhor_modelo_nome
            })
            
            # Configuração do modelo (métricas + info)
            output_model.update_design(config_dict={
                "metricas": {k: float(v) for k, v in metricas.items() if isinstance(v, (int, float))},
                "n_features": df_features.shape[1] - 1,
                "n_samples_treino": df_features.shape[0],
                "modelos_comparados": n_modelos_comparar,
                "otimizado": otimizar_hiperparametros,
            })
            
            # Upload do arquivo do modelo (se foi salvo)
            if resultado.get('caminho_modelo'):
                caminho_modelo = Path(resultado['caminho_modelo'])
                if caminho_modelo.exists():
                    output_model.update_weights(weights_filename=str(caminho_modelo))
                    logger.info(f"✓ Modelo registrado: {caminho_modelo}")
                    model_id = output_model.id
                else:
                    logger.warning(f"Arquivo do modelo não encontrado: {caminho_modelo}")
            
        except Exception as e:
            logger.error(f"Erro ao registrar modelo: {e}")
    
    # ========== FECHAMENTO DA TASK ==========
    # IMPORTANTE: Fechar task para permitir criação de novas tasks em sequência
    if task:
        logger.info("\n[4] Fechando task...")
        task.close()
        logger.info("✓ Task finalizada e pronta para próximo pipeline")
    
    # ========== RESULTADO ==========
    logger.info("\n" + "="*80)
    logger.info("PIPELINE DE TREINAMENTO CONCLUÍDO COM SUCESSO")
    logger.info("="*80)
    
    # Adicionar informações ClearML ao resultado
    resultado['model_id'] = model_id
    resultado['offline_mode'] = offline_mode
    resultado['tipo_problema'] = tipo_problema
    
    return resultado


if __name__ == "__main__":
    """
    Exemplo de execução direta do pipeline.
    """
    import sys
    from src.utils.io import load_dataframe
    
    # Exemplo de uso
    print("\n" + "="*80)
    print("EXECUÇÃO DIRETA DO PIPELINE DE TREINAMENTO")
    print("="*80)
    
    # Carregar dados de exemplo
    # (em produção, você receberia do pipeline de features)
    print("\n⚠️  Este script requer dados do pipeline de features")
    print("Execute os pipelines 1 e 2 primeiro, ou forneça um CSV com features")
    print("="*80)
