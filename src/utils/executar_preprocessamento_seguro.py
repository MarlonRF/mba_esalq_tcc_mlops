"""
Executa função de preprocessamento de forma segura considerando o contexto ClearML.
"""
from typing import Optional
import pandas as pd


def executar_preprocessamento_seguro(
    funcao_preprocessamento,
    dataframe_entrada: pd.DataFrame,
    configuracao: Optional[dict],
):
    """
    Executa função de preprocessamento de forma segura considerando o contexto ClearML.

    Verifica se existe uma tarefa ClearML ativa e chama a função apropriada:
    - Se há tarefa ativa: chama a função decorada normalmente
    - Se não há tarefa: chama a função original (__wrapped__) se disponível

    Args:
        funcao_preprocessamento: Função de preprocessamento a ser executada
        dataframe_entrada (pd.DataFrame): DataFrame com dados a serem processados
        configuracao (Optional[dict]): Dicionário de configuração do preprocessamento

    Returns:
        pd.DataFrame: DataFrame processado pela função
    """
    try:
        # Tenta importar ClearML e verificar se há tarefa ativa
        from clearml import Task

        tarefa_clearml_ativa = Task.current_task() is not None
    except Exception:
        # Se ClearML não está disponível, considera como não ativo
        tarefa_clearml_ativa = False

    # Decide qual versão da função chamar
    if not tarefa_clearml_ativa and hasattr(funcao_preprocessamento, "__wrapped__"):
        # Chama função original (sem decorator ClearML)
        return funcao_preprocessamento.__wrapped__(dataframe_entrada, configuracao)
    else:
        # Chama função decorada normalmente
        return funcao_preprocessamento(dataframe_entrada, configuracao)
