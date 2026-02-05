"""
Pipeline de engenharia de features.

Aplica transformações de features em dados já processados:
- Codificação categórica (label, onehot)
- Normalização/padronização
- Features derivadas (IMC, heat index, etc.)

Use após executar pipeline_processamento.py
"""
import pandas as pd
from typing import Dict, List, Optional, Tuple

from config import config_custom as config
from ..features.codificacao import (
    aplicar_codificacao_rotulos,
    aplicar_dummy,
)
from ..features.normalizacao import normalizar
from ..features.criacao_features import adicionar_features_derivadas


def executar_pipeline_features(
    df: pd.DataFrame,
    colunas_categoricas: Optional[List[str]] = None,
    aplicar_codificacao: bool = True,
    metodo_codificacao: str = "label",
    sufixo_codificacao: str = "_cod",
    aplicar_normalizacao: bool = True,
    colunas_normalizar: Optional[Dict[str, str]] = None,
    metodo_normalizacao: str = "standard",
    agrupamento_normalizacao: Optional[str] = "mes-ano",
    sufixo_normalizacao: str = "_norm",
    criar_features_derivadas: bool = False,
    tipos_features_derivadas: Optional[List[str]] = None,
) -> Tuple[pd.DataFrame, Dict]:
    """
    Executa o pipeline de engenharia de features.
    
    Aplica transformações de features em dados já processados (limpos e imputados).
    
    Args:
        df: DataFrame processado (saída de pipeline_processamento)
        colunas_categoricas: Colunas para codificar (usa config se None)
        aplicar_codificacao: Se deve aplicar codificação categórica
        metodo_codificacao: Método de codificação ('label' ou 'onehot')
        sufixo_codificacao: Sufixo para colunas codificadas
        aplicar_normalizacao: Se deve aplicar normalização
        colunas_normalizar: Colunas para normalizar. Pode ser:
            - None: normaliza todas colunas numéricas
            - Dict[str, str]: normaliza cada coluna com método específico
              Ex: {'temperatura': 'standard', 'umidade': 'minmax'}
        metodo_normalizacao: Método padrão de normalização ('standard', 'minmax', 'robust')
        agrupamento_normalizacao: Coluna de agrupamento para normalização
        sufixo_normalizacao: Sufixo para colunas normalizadas
        criar_features_derivadas: Se deve criar features derivadas
        tipos_features_derivadas: Tipos de features derivadas (usa config se None)
        
    Returns:
        Tupla (df_features, artefatos) onde artefatos contém mapeamentos
    """
    # Usar configurações do config se não fornecidas
    colunas_categoricas = colunas_categoricas or config.COLUNAS_CATEGORICAS
    tipos_features_derivadas = tipos_features_derivadas or config.TIPOS_FEATURES_DERIVADAS
    
    # Copiar DataFrame para não modificar original
    df_feat = df.copy()
    
    # Artefatos para retornar
    artefatos = {}
    
    print("🎨 Iniciando pipeline de FEATURES...")
    
    # ETAPA 1: Features Derivadas (antes de codificação/normalização)
    if criar_features_derivadas:
        print(f"  1️⃣ Criando features derivadas ({len(tipos_features_derivadas)} tipos)...")
        df_feat = adicionar_features_derivadas(
            df_feat,
            tipos=tipos_features_derivadas
        )
    
    # ETAPA 2: Codificação Categórica
    if aplicar_codificacao and colunas_categoricas:
        print(f"  2️⃣ Aplicando codificação ({metodo_codificacao})...")
        cols_existentes = [c for c in colunas_categoricas if c in df_feat.columns]
        
        if metodo_codificacao == "label":
            df_feat, mapeamentos = aplicar_codificacao_rotulos(
                df_feat, 
                cols_existentes, 
                sufixo=sufixo_codificacao
            )
            artefatos['mapeamentos_codificacao'] = mapeamentos
        elif metodo_codificacao == "onehot":
            df_feat = aplicar_dummy(df_feat, cols_existentes)
            artefatos['colunas_onehot'] = [c for c in df_feat.columns if c not in df.columns]
    
    # ETAPA 3: Normalização
    if aplicar_normalizacao:
        print(f"  3️⃣ Aplicando normalização ({metodo_normalizacao})...")
        df_feat = normalizar(
            df_feat,
            colunas=colunas_normalizar,
            metodo=metodo_normalizacao,
            agrupamento=agrupamento_normalizacao,
            sufixo=sufixo_normalizacao,
        )
        colunas_norm = [c for c in df_feat.columns if c.endswith(sufixo_normalizacao)]
        artefatos['colunas_normalizadas'] = colunas_norm
    
    print(f"✅ Pipeline FEATURES concluído! Shape final: {df_feat.shape}")
    print(f"   Novas colunas criadas: {df_feat.shape[1] - df.shape[1]}")
    
    return df_feat, artefatos


__all__ = ['executar_pipeline_features']
