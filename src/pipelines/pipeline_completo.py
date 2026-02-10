"""
Pipeline completo com duas formas de execução:
- processamento + features
- processamento + features + treinamento
"""
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple

from .pipeline_processamento import executar_pipeline_processamento
from .pipeline_features import executar_pipeline_features
from .pipeline_treinamento_unified import treinar_pipeline_completo


def executar_pipeline_completo(
    df: pd.DataFrame,
    # Parâmetros de processamento
    substituicoes: Optional[Dict] = None,
    coluna_data: Optional[str] = None,
    coluna_hora: Optional[str] = None,
    colunas_float: Optional[List[str]] = None,
    colunas_int: Optional[List[str]] = None,
    colunas_categoricas: Optional[List[str]] = None,
    metodo_imputacao_numerica: Optional[str] = None,
    metodo_imputacao_categorica: Optional[str] = None,
    valor_constante_categorica: Optional[str] = None,
    criar_agrupamento_temporal: bool = True,
    nome_coluna_agrupamento: str = "mes-ano",
    # Parâmetros de features
    aplicar_codificacao: bool = True,
    metodo_codificacao: str = "label",
    sufixo_codificacao: str = "_cod",
    aplicar_normalizacao: bool = True,
    colunas_normalizar: Optional[List[str]] = None,
    metodo_normalizacao: str = "standard",
    agrupamento_normalizacao: Optional[str] = "mes-ano",
    sufixo_normalizacao: str = "_norm",
    criar_features_derivadas: bool = False,
    tipos_features_derivadas: Optional[List[str]] = None,
) -> Tuple[pd.DataFrame, Dict]:
    """
    Executa pipeline completo: processamento base + engenharia de features.
    
    Args:
        df: DataFrame original
        ... (mesmos parâmetros dos pipelines individuais)
        
    Returns:
        Tupla (df_completo, artefatos) onde artefatos contém todos os mapeamentos
    """
    print("=" * 60)
    print("🚀 PIPELINE COMPLETO: Processamento + Features")
    print("=" * 60)
    
    # FASE 1: Processamento Base
    df_processado = executar_pipeline_processamento(
        df,
        substituicoes=substituicoes,
        coluna_data=coluna_data,
        coluna_hora=coluna_hora,
        colunas_float=colunas_float,
        colunas_int=colunas_int,
        colunas_categoricas=colunas_categoricas,
        metodo_imputacao_numerica=metodo_imputacao_numerica,
        metodo_imputacao_categorica=metodo_imputacao_categorica,
        valor_constante_categorica=valor_constante_categorica,
        criar_agrupamento_temporal=criar_agrupamento_temporal,
        nome_coluna_agrupamento=nome_coluna_agrupamento,
    )
    
    print()  # Linha em branco
    
    # FASE 2: Engenharia de Features
    df_final, artefatos = executar_pipeline_features(
        df_processado,
        colunas_categoricas=colunas_categoricas,
        aplicar_codificacao=aplicar_codificacao,
        metodo_codificacao=metodo_codificacao,
        sufixo_codificacao=sufixo_codificacao,
        aplicar_normalizacao=aplicar_normalizacao,
        colunas_normalizar=colunas_normalizar,
        metodo_normalizacao=metodo_normalizacao,
        agrupamento_normalizacao=agrupamento_normalizacao,
        sufixo_normalizacao=sufixo_normalizacao,
        criar_features_derivadas=criar_features_derivadas,
        tipos_features_derivadas=tipos_features_derivadas,
    )
    
    print("=" * 60)
    print(f"✅ PIPELINE COMPLETO FINALIZADO!")
    print(f"   Shape original: {df.shape}")
    print(f"   Shape final: {df_final.shape}")
    print(f"   Artefatos: {list(artefatos.keys())}")
    print("=" * 60)
    
    return df_final, artefatos


def executar_pipeline_completo_ml(
    dados: pd.DataFrame,
    coluna_alvo: str,
    tipo_problema: str,
    # parâmetros do processamento/features
    substituicoes: Optional[Dict] = None,
    coluna_data: Optional[str] = None,
    coluna_hora: Optional[str] = None,
    colunas_float: Optional[List[str]] = None,
    colunas_int: Optional[List[str]] = None,
    colunas_categoricas: Optional[List[str]] = None,
    metodo_imputacao_numerica: Optional[str] = None,
    metodo_imputacao_categorica: Optional[str] = None,
    valor_constante_categorica: Optional[str] = None,
    criar_agrupamento_temporal: bool = True,
    nome_coluna_agrupamento: str = "mes-ano",
    aplicar_codificacao: bool = True,
    metodo_codificacao: str = "label",
    sufixo_codificacao: str = "_cod",
    aplicar_normalizacao: bool = True,
    colunas_normalizar: Optional[List[str]] = None,
    metodo_normalizacao: str = "standard",
    agrupamento_normalizacao: Optional[str] = "mes-ano",
    sufixo_normalizacao: str = "_norm",
    criar_features_derivadas: bool = False,
    tipos_features_derivadas: Optional[List[str]] = None,
    # parâmetros do treinamento
    params_setup: Optional[Dict[str, Any]] = None,
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
    """Executa pipeline fim a fim: processamento, features e treinamento."""
    df_final, artefatos = executar_pipeline_completo(
        dados,
        substituicoes=substituicoes,
        coluna_data=coluna_data,
        coluna_hora=coluna_hora,
        colunas_float=colunas_float,
        colunas_int=colunas_int,
        colunas_categoricas=colunas_categoricas,
        metodo_imputacao_numerica=metodo_imputacao_numerica,
        metodo_imputacao_categorica=metodo_imputacao_categorica,
        valor_constante_categorica=valor_constante_categorica,
        criar_agrupamento_temporal=criar_agrupamento_temporal,
        nome_coluna_agrupamento=nome_coluna_agrupamento,
        aplicar_codificacao=aplicar_codificacao,
        metodo_codificacao=metodo_codificacao,
        sufixo_codificacao=sufixo_codificacao,
        aplicar_normalizacao=aplicar_normalizacao,
        colunas_normalizar=colunas_normalizar,
        metodo_normalizacao=metodo_normalizacao,
        agrupamento_normalizacao=agrupamento_normalizacao,
        sufixo_normalizacao=sufixo_normalizacao,
        criar_features_derivadas=criar_features_derivadas,
        tipos_features_derivadas=tipos_features_derivadas,
    )

    resultado_treino = treinar_pipeline_completo(
        dados=df_final,
        coluna_alvo=coluna_alvo,
        tipo_problema=tipo_problema,
        params_setup=params_setup,
        n_modelos_comparar=n_modelos_comparar,
        modelos_incluir=modelos_incluir,
        modelos_excluir=modelos_excluir,
        metrica_ordenacao=metrica_ordenacao,
        otimizar_hiperparametros=otimizar_hiperparametros,
        n_iter_otimizacao=n_iter_otimizacao,
        finalizar=finalizar,
        salvar_modelo_final=salvar_modelo_final,
        nome_modelo=nome_modelo,
        pasta_modelos=pasta_modelos,
    )
    resultado_treino["dados_processados"] = df_final
    resultado_treino["artefatos_features"] = artefatos
    return resultado_treino


__all__ = ['executar_pipeline_completo', 'executar_pipeline_completo_ml']
