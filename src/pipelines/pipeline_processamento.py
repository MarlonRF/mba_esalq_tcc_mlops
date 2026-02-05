"""
Pipeline de processamento base - apenas limpeza, conversão e imputação.

Não inclui engenharia de features (codificação, normalização, derivadas).
Para features, use pipeline_features.py
"""
import pandas as pd
from typing import Dict, List, Optional

from config import config_custom as config
from ..processamento.limpeza import (
    aplicar_substituicoes,
    converter_colunas_float,
    converter_colunas_int,
    converter_colunas_categoricas,
)
from ..processamento.temporal import (
    converter_colunas_temporais,
    garantir_agrupamento_temporal,
)
from ..processamento.imputacao import (
    imputar_numericos,
    imputar_categoricos,
    imputar_por_coluna,
    imputar_media_movel_interpolada,
)


def executar_pipeline_processamento(
    df: pd.DataFrame,
    substituicoes: Optional[Dict] = None,
    coluna_data: Optional[str] = None,
    coluna_hora: Optional[str] = None,
    colunas_float: Optional[List[str]] = None,
    colunas_int: Optional[List[str]] = None,
    colunas_categoricas: Optional[List[str]] = None,
    metodo_imputacao_numerica: Optional[str] = None,
    metodo_imputacao_categorica: Optional[str] = None,
    valor_constante_categorica: Optional[str] = None,
    config_imputacao_customizada: Optional[Dict[str, str]] = None,
    criar_agrupamento_temporal: bool = True,
    nome_coluna_agrupamento: str = "mes-ano",
) -> pd.DataFrame:
    """
    Executa o pipeline de processamento base (sem engenharia de features).
    
    Inclui:
    - Limpeza (substituições)
    - Conversões de tipo (temporal, float, int, categórica)
    - Imputação (numérica e categórica)
    - Criação de agrupamento temporal (opcional)
    
    NÃO inclui:
    - Codificação categórica
    - Normalização
    - Features derivadas
    
    Args:
        df: DataFrame a ser processado
        substituicoes: Dicionário de substituições para limpeza (usa config se None)
        coluna_data: Nome da coluna de data (usa config se None)
        coluna_hora: Nome da coluna de hora (usa config se None)
        colunas_float: Lista de colunas para converter para float (usa config se None)
        colunas_int: Lista de colunas para converter para int (usa config se None)
        colunas_categoricas: Lista de colunas categóricas (usa config se None)
        metodo_imputacao_numerica: Método de imputação numérica global (usa config se None)
        metodo_imputacao_categorica: Método de imputação categórica global (usa config se None)
        valor_constante_categorica: Valor constante para imputação (usa config se None)
        config_imputacao_customizada: Dicionário {coluna: método} para imputação específica
            Exemplo: {'idade': 'median', 'sexo': 'mode', 'peso': 'mean', 'altura': 0}
            Se fornecido, tem prioridade sobre métodos globais
        criar_agrupamento_temporal: Se deve criar coluna de agrupamento temporal
        nome_coluna_agrupamento: Nome da coluna de agrupamento temporal
        
    Returns:
        DataFrame processado (sem features de engenharia)
    """
    # Usar configurações do config se não fornecidas
    substituicoes = substituicoes or config.SUBSTITUICOES_LIMPEZA
    coluna_data = coluna_data or config.COLUNA_DATA
    coluna_hora = coluna_hora or config.COLUNA_HORA
    colunas_float = colunas_float or config.COLUNAS_PONTO_FLUTUANTE
    colunas_int = colunas_int or config.COLUNAS_NUMEROS_INTEIROS
    colunas_categoricas = colunas_categoricas or config.COLUNAS_CATEGORICAS
    metodo_imputacao_numerica = metodo_imputacao_numerica or config.METODO_IMPUTACAO_NUM
    metodo_imputacao_categorica = metodo_imputacao_categorica or config.METODO_IMPUTACAO_CAT
    valor_constante_categorica = valor_constante_categorica or config.VALOR_CONST_CATEGORICA
    
    # Copiar DataFrame para não modificar original
    df_proc = df.copy()
    
    # Padronizar nomes de colunas
    df_proc.columns = [c.lower().strip().replace(" ", "_") for c in df_proc.columns]
    
    print("🔄 Iniciando pipeline de processamento BASE...")
    
    # ETAPA 1: Limpeza - Substituições
    print("  1️⃣ Aplicando substituições de limpeza...")
    df_proc = aplicar_substituicoes(df_proc, substituicoes)
    
    # ETAPA 2: Conversões de Tipo
    print("  2️⃣ Convertendo tipos de dados...")
    df_proc = converter_colunas_temporais(df_proc, coluna_data, coluna_hora)
    df_proc = converter_colunas_float(df_proc, colunas_float)
    df_proc = converter_colunas_int(df_proc, colunas_int)
    df_proc = converter_colunas_categoricas(df_proc, colunas_categoricas)
    
    # ETAPA 3: Imputação
    print("  3️⃣ Imputando valores faltantes...")
    
    if config_imputacao_customizada:
        # Separar configurações especiais (média móvel) das normais
        config_normal = {}
        colunas_media_movel = []
        
        for coluna, metodo in config_imputacao_customizada.items():
            if metodo == "rolling_mean_48":
                colunas_media_movel.append(coluna)
            else:
                config_normal[coluna] = metodo
        
        # Aplicar imputação normal
        if config_normal:
            df_proc = imputar_por_coluna(
                df_proc,
                config_normal,
                metodo_padrao=metodo_imputacao_numerica
            )
        
        # Aplicar média móvel + interpolação para séries temporais
        for coluna in colunas_media_movel:
            if coluna in df_proc.columns:
                df_proc = imputar_media_movel_interpolada(
                    df_proc,
                    coluna,
                    window=48,
                    metodo_interpolacao="linear"
                )
    else:
        # Usa métodos globais (antigo comportamento)
        df_proc = imputar_numericos(df_proc, metodo_imputacao_numerica)
        df_proc = imputar_categoricos(
            df_proc, 
            metodo_imputacao_categorica, 
            valor_constante_categorica
        )
    
    # ETAPA 4: Features Temporais (agrupamento)
    if criar_agrupamento_temporal:
        print("  4️⃣ Criando agrupamento temporal...")
        df_proc = garantir_agrupamento_temporal(
            df_proc, 
            coluna_data, 
            coluna_hora, 
            nome_coluna_agrupamento
        )
    
    print(f"✅ Pipeline BASE concluído! Shape final: {df_proc.shape}")
    
    return df_proc


__all__ = ['executar_pipeline_processamento']
