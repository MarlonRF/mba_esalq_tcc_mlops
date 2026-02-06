"""
Pipeline UNIFICADO de treinamento: setup → compare → tune → finalize → save.
Suporta tanto CLASSIFICAÇÃO quanto REGRESSÃO através de um único pipeline configurável.
"""
from typing import Any, Dict, List, Optional, Tuple, Literal
import pandas as pd

from config.logger_config import logger
from config.config_gerais import METRICAS_CLASSIFICACAO, METRICAS_REGRESSAO
from src.treinamento.configuracao import criar_experimento
from src.treinamento.treino import treinar_modelo_base, otimizar_modelo, finalizar_modelo
from src.treinamento.avaliacao import classificar_metricas
from src.treinamento.persistencia import salvar_modelo

# Tipo literal para validação
TipoProblema = Literal["classificacao", "regressao"]


def treinar_pipeline_completo(
    dados: pd.DataFrame,
    coluna_alvo: str,
    tipo_problema: TipoProblema,
    params_setup: Optional[Dict] = None,
    n_modelos_comparar: int = 3,
    modelos_incluir: Optional[List[str]] = None,
    modelos_excluir: Optional[List[str]] = None,
    metrica_ordenacao: Optional[str] = None,
    otimizar_hiperparametros: bool = True,
    n_iter_otimizacao: int = 10,
    finalizar: bool = True,
    salvar_modelo_final: bool = True,
    nome_modelo: str = "modelo_final",
    pasta_modelos: str = "modelos",
) -> Dict[str, Any]:
    """
    Executa pipeline completo de treinamento (CLASSIFICAÇÃO ou REGRESSÃO).
    
    Este é o wrapper de mais alto nível que orquestra todas as etapas:
    1. Setup do experimento
    2. Comparação de modelos
    3. Seleção dos melhores
    4. Otimização de hiperparâmetros (opcional)
    5. Finalização (treino em dataset completo)
    6. Salvamento do modelo
    
    Args:
        dados: DataFrame com dados de treinamento
        coluna_alvo: Nome da coluna target
        tipo_problema: 'classificacao' ou 'regressao'
        params_setup: Parâmetros para PyCaret.setup (usa padrão se None)
        n_modelos_comparar: Quantos modelos selecionar na comparação inicial
        modelos_incluir: Lista de IDs de modelos para incluir (None = todos)
        modelos_excluir: Lista de IDs de modelos para excluir
        metrica_ordenacao: Métrica para ordenar/selecionar modelos (None = usa padrão do tipo)
        otimizar_hiperparametros: Se deve otimizar hiperparâmetros
        n_iter_otimizacao: Número de iterações para otimização
        finalizar: Se deve finalizar modelo (treinar em dataset completo)
        salvar_modelo_final: Se deve salvar modelo em disco
        nome_modelo: Nome base para arquivo do modelo
        pasta_modelos: Pasta para salvar modelos
        
    Returns:
        Dict contendo:
            - experimento: Experiment configurado (Classification ou Regression)
            - modelos_base: Lista de modelos da comparação inicial
            - tabela_comparacao: DataFrame com métricas de todos modelos
            - melhor_modelo: Modelo final (otimizado se aplicável)
            - metricas_melhor: Métricas do melhor modelo
            - modelo_otimizado: Modelo após otimização (se aplicável)
            - modelo_finalizado: Modelo após finalização (se aplicável)
            - caminho_modelo: Caminho do modelo salvo (se aplicável)
            - tipo_problema: Tipo de problema usado
            
    Examples:
        >>> # CLASSIFICAÇÃO - Uso básico
        >>> resultado = treinar_pipeline_completo(
        ...     dados=df_treino,
        ...     coluna_alvo='classe',
        ...     tipo_problema='classificacao'
        ... )
        
        >>> # REGRESSÃO - Customizado
        >>> resultado = treinar_pipeline_completo(
        ...     dados=df_treino,
        ...     coluna_alvo='preco',
        ...     tipo_problema='regressao',
        ...     modelos_incluir=['rf', 'lr', 'gbr'],
        ...     otimizar_hiperparametros=False,
        ...     n_modelos_comparar=1
        ... )
        
        >>> # Para produção - otimiza e salva
        >>> resultado = treinar_pipeline_completo(
        ...     dados=df_treino,
        ...     coluna_alvo='target',
        ...     tipo_problema='classificacao',
        ...     otimizar_hiperparametros=True,
        ...     n_iter_otimizacao=20,
        ...     finalizar=True,
        ...     salvar_modelo_final=True,
        ...     nome_modelo='modelo_producao_v1'
        ... )
    """
    # Valida tipo de problema
    if tipo_problema not in ["classificacao", "regressao"]:
        raise ValueError(f"tipo_problema deve ser 'classificacao' ou 'regressao', recebido: {tipo_problema}")
    
    # Define métricas e padrões baseado no tipo de problema
    if tipo_problema == "classificacao":
        metricas = METRICAS_CLASSIFICACAO
        metrica_padrao = "Accuracy"
        tipo_display = "CLASSIFICAÇÃO"
    else:  # regressao
        metricas = METRICAS_REGRESSAO
        metrica_padrao = "R2"
        tipo_display = "REGRESSÃO"
    
    # Usa métrica padrão se não especificada
    if metrica_ordenacao is None:
        metrica_ordenacao = metrica_padrao
    
    logger.info("="*60)
    logger.info(f"Iniciando pipeline completo de treinamento de {tipo_display}")
    logger.info("="*60)
    
    resultado = {"tipo_problema": tipo_problema}
    
    # ETAPA 1: Setup do experimento
    logger.info(f"ETAPA 1: Configurando experimento PyCaret ({tipo_display})...")
    exp = criar_experimento(
        dados=dados,
        coluna_alvo=coluna_alvo,
        tipo_problema=tipo_problema,
        params=params_setup
    )
    resultado["experimento"] = exp
    logger.info(f"✓ Experimento de {tipo_problema} configurado")
    
    # ETAPA 2: Comparação de modelos
    logger.info(f"\nETAPA 2: Comparando modelos (selecionando top {n_modelos_comparar})...")
    modelos_base, tabela_comparacao = treinar_modelo_base(
        exp=exp,
        tipo_problema=tipo_problema,
        n_select=n_modelos_comparar,
        include=modelos_incluir,
        exclude=modelos_excluir,
        sort=metrica_ordenacao
    )
    resultado["modelos_base"] = modelos_base
    resultado["tabela_comparacao"] = tabela_comparacao
    
    # Classifica modelos por múltiplas métricas
    tabela_classificada = classificar_metricas(
        tabela_comparacao,
        metricas
    )
    resultado["tabela_classificada"] = tabela_classificada
    
    logger.info(f"✓ {len(modelos_base)} modelo(s) selecionado(s)")
    logger.info(f"  Melhor modelo: {tabela_comparacao.index[0]}")
    logger.info(f"  {metrica_ordenacao}: {tabela_comparacao[metrica_ordenacao].iloc[0]:.4f}")
    
    # Seleciona o melhor modelo
    melhor_modelo = modelos_base[0]
    resultado["melhor_modelo"] = melhor_modelo
    
    # ETAPA 3: Otimização de hiperparâmetros (opcional)
    if otimizar_hiperparametros:
        logger.info(f"\nETAPA 3: Otimizando hiperparâmetros ({n_iter_otimizacao} iterações)...")
        modelo_otimizado, metricas_otimizacao = otimizar_modelo(
            exp=exp,
            tipo_problema=tipo_problema,
            modelo=melhor_modelo,
            optimize=metrica_ordenacao,
            n_iter=n_iter_otimizacao
        )
        resultado["modelo_otimizado"] = modelo_otimizado
        resultado["metricas_otimizacao"] = metricas_otimizacao
        
        # Atualiza melhor modelo para a versão otimizada
        melhor_modelo = modelo_otimizado
        resultado["melhor_modelo"] = modelo_otimizado
        
        logger.info("✓ Hiperparâmetros otimizados")
        logger.info(f"  {metrica_ordenacao} após otimização: {metricas_otimizacao[metrica_ordenacao].iloc[0]:.4f}")
    else:
        logger.info("\nETAPA 3: Otimização de hiperparâmetros PULADA")
    
    # ETAPA 4: Finalização (treina em dataset completo)
    if finalizar:
        logger.info("\nETAPA 4: Finalizando modelo (treinamento em dataset completo)...")
        modelo_finalizado = finalizar_modelo(
            exp=exp,
            tipo_problema=tipo_problema,
            modelo=melhor_modelo
        )
        resultado["modelo_finalizado"] = modelo_finalizado
        
        # Atualiza melhor modelo para versão finalizada
        melhor_modelo = modelo_finalizado
        resultado["melhor_modelo"] = modelo_finalizado
        
        logger.info("✓ Modelo finalizado")
    else:
        logger.info("\nETAPA 4: Finalização PULADA")
    
    # ETAPA 5: Salvamento do modelo
    if salvar_modelo_final:
        logger.info(f"\nETAPA 5: Salvando modelo em '{pasta_modelos}/{nome_modelo}.pkl'...")
        caminho_salvo = salvar_modelo(
            exp=exp,
            modelo=melhor_modelo,
            nome_modelo=nome_modelo,
            pasta_destino=pasta_modelos
        )
        resultado["caminho_modelo"] = caminho_salvo
        logger.info(f"✓ Modelo salvo: {caminho_salvo}")
    else:
        logger.info("\nETAPA 5: Salvamento PULADO")
    
    # Extrai métricas finais do melhor modelo
    resultado["metricas_melhor"] = tabela_comparacao.iloc[0].to_dict()
    
    logger.info("\n" + "="*60)
    logger.info(f"Pipeline de {tipo_display} completo FINALIZADO com sucesso!")
    logger.info("="*60)
    
    return resultado


def treinar_rapido(
    dados: pd.DataFrame,
    coluna_alvo: str,
    tipo_problema: TipoProblema,
    modelo: str = "auto",
    salvar: bool = False,
    params_setup: Optional[Dict[str, Any]] = None,
) -> Tuple[Any, Any]:
    """
    Atalho para treinamento rápido sem otimização.
    
    Útil para prototipagem e testes rápidos. Treina apenas um modelo
    específico (ou seleciona automaticamente o melhor) sem otimização.
    
    Args:
        dados: DataFrame de treinamento
        coluna_alvo: Nome da coluna target
        tipo_problema: 'classificacao' ou 'regressao'
        modelo: ID do modelo ('rf', 'lr', 'dt', etc) ou 'auto' para melhor
        salvar: Se deve salvar o modelo
        params_setup: Parâmetros para setup do PyCaret (opcional)
        
    Returns:
        Tupla (experimento, modelo_treinado)
        
    Examples:
        >>> # Treina Random Forest de classificação rapidamente
        >>> exp, modelo = treinar_rapido(df, 'classe', 'classificacao', modelo='rf')
        
        >>> # Deixa PyCaret escolher o melhor para regressão
        >>> exp, modelo = treinar_rapido(df, 'preco', 'regressao', modelo='auto')
    """
    tipo_display = "CLASSIFICAÇÃO" if tipo_problema == "classificacao" else "REGRESSÃO"
    logger.info(f"Treinamento rápido de {tipo_display} - modelo: {modelo}")
    
    # Usa params_setup fornecido ou defaults rápidos
    if params_setup is None:
        params_rapidos = {
            "fold": 2,
            "remove_outliers": False,
            "verbose": False,
        }
    else:
        params_rapidos = params_setup
    
    resultado = treinar_pipeline_completo(
        dados=dados,
        coluna_alvo=coluna_alvo,
        tipo_problema=tipo_problema,
        params_setup=params_rapidos,
        n_modelos_comparar=1,
        modelos_incluir=None if modelo == "auto" else [modelo],
        otimizar_hiperparametros=False,
        finalizar=False,
        salvar_modelo_final=salvar,
    )
    
    return resultado["experimento"], resultado["melhor_modelo"]


__all__ = [
    'treinar_pipeline_completo',
    'treinar_rapido',
    'TipoProblema',
]
