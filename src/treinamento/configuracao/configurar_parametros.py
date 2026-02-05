"""
Helper para criar e validar dicionários de configuração para experimentos PyCaret.
"""
from typing import Dict, List, Optional, Any
from config.config_gerais import PARAMS_PADRAO


def configurar_parametros(
    fold: int = 5,
    session_id: int = 42,
    normalize: bool = True,
    remove_outliers: bool = True,
    outliers_method: str = "iforest",
    pca: bool = False,
    pca_components: Optional[int] = None,
    use_gpu: bool = False,
    verbose: bool = False,
    html: bool = False,
    log_experiment: bool = False,
    experiment_name: Optional[str] = None,
    log_plots: bool = False,
    log_data: bool = False,
    **kwargs
) -> Dict[str, Any]:
    """
    Cria dicionário de parâmetros para configuração de experimento PyCaret.
    
    Combina valores padrão com parâmetros fornecidos, facilitando a criação
    de configurações consistentes para experimentos.
    
    Args:
        fold: Número de folds para validação cruzada
        session_id: Seed para reprodutibilidade
        normalize: Se deve normalizar features numéricas
        remove_outliers: Se deve remover outliers automaticamente
        outliers_method: Método de detecção de outliers ('iforest', 'ee', etc)
        pca: Se deve aplicar PCA para redução de dimensionalidade
        pca_components: Número de componentes PCA (None = automático)
        use_gpu: Se deve usar GPU para treinamento (requer configuração adequada)
        verbose: Se deve exibir logs detalhados
        html: Se deve gerar relatórios HTML
        log_experiment: Se deve registrar experimento (MLflow/ClearML)
        experiment_name: Nome do experimento para logging
        log_plots: Se deve registrar plots automaticamente
        log_data: Se deve registrar dados no experimento
        **kwargs: Parâmetros adicionais para PyCaret setup
        
    Returns:
        Dict com parâmetros de configuração prontos para PyCaret.setup()
        
    Examples:
        >>> # Configuração básica
        >>> params = configurar_parametros(fold=3, session_id=123)
        
        >>> # Configuração com PCA
        >>> params = configurar_parametros(
        ...     pca=True,
        ...     pca_components=10,
        ...     normalize=True
        ... )
        
        >>> # Configuração para logging
        >>> params = configurar_parametros(
        ...     log_experiment=True,
        ...     experiment_name="meu_experimento",
        ...     log_plots=True
        ... )
    """
    # Começa com parâmetros padrão
    params = PARAMS_PADRAO.copy()
    
    # Atualiza com valores fornecidos
    params.update({
        "fold": fold,
        "session_id": session_id,
        "normalize": normalize,
        "remove_outliers": remove_outliers,
        "outliers_method": outliers_method,
        "pca": pca,
        "use_gpu": use_gpu,
        "verbose": verbose,
        "html": html,
        "log_experiment": log_experiment,
    })
    
    # Adiciona parâmetros opcionais se fornecidos
    if pca_components is not None:
        params["pca_components"] = pca_components
    
    if experiment_name is not None:
        params["experiment_name"] = experiment_name
    
    if log_plots:
        params["log_plots"] = log_plots
    
    if log_data:
        params["log_data"] = log_data
    
    # Adiciona quaisquer parâmetros extras
    params.update(kwargs)
    
    return params


def validar_parametros(params: Dict[str, Any]) -> bool:
    """
    Valida se um dicionário de parâmetros possui as chaves obrigatórias.
    
    Args:
        params: Dicionário de parâmetros a validar
        
    Returns:
        True se parâmetros são válidos, False caso contrário
        
    Raises:
        ValueError: Se parâmetros obrigatórios estão ausentes
    """
    obrigatorios = ["data", "target"]
    
    faltantes = [k for k in obrigatorios if k not in params]
    
    if faltantes:
        raise ValueError(
            f"Parâmetros obrigatórios ausentes: {faltantes}. "
            f"Certifique-se de incluir 'data' (DataFrame) e 'target' (str)."
        )
    
    return True


def parametros_rapidos(
    preset: str = "default"
) -> Dict[str, Any]:
    """
    Retorna configurações pré-definidas para casos comuns.
    
    Args:
        preset: Nome do preset desejado
            - "default": Configuração padrão balanceada
            - "fast": Configuração rápida para prototipagem (fold=2)
            - "thorough": Configuração detalhada (fold=10, sem outliers)
            - "gpu": Configuração otimizada para GPU
            - "production": Configuração para produção (sem verbose/html)
            
    Returns:
        Dict com parâmetros configurados
        
    Examples:
        >>> # Teste rápido
        >>> params_fast = parametros_rapidos("fast")
        >>> exp.setup(**params_fast, data=df, target='label')
        
        >>> # Treinamento completo
        >>> params_prod = parametros_rapidos("production")
    """
    presets = {
        "default": configurar_parametros(),
        
        "fast": configurar_parametros(
            fold=2,
            remove_outliers=False,
            verbose=True,
        ),
        
        "thorough": configurar_parametros(
            fold=10,
            remove_outliers=True,
            normalize=True,
            pca=False,
        ),
        
        "gpu": configurar_parametros(
            use_gpu=True,
            normalize=True,
            fold=5,
        ),
        
        "production": configurar_parametros(
            fold=5,
            verbose=False,
            html=False,
            log_experiment=True,
            remove_outliers=True,
        ),
    }
    
    if preset not in presets:
        raise ValueError(
            f"Preset '{preset}' não encontrado. "
            f"Opções: {list(presets.keys())}"
        )
    
    return presets[preset]
