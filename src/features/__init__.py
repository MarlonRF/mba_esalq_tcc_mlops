"""
Módulo de features para processamento de dados.

Contém funções para:
- Codificação de variáveis categóricas
- Criação de features derivadas
- Normalização de dados numéricos
"""
from .codificacao import (
    aplicar_codificacao_rotulos,
    aplicar_dummy,
)
from .criacao_features import (
    calcular_valor_imc,
    imc_classe,
    calcular_heat_index,
    calcular_ponto_orvalho,
    calcular_tu_stull,
    adicionar_features_derivadas,
)
from .normalizacao import (
    pick_scaler,
    normalizar,
    SCALERS,
)

__all__ = [
    # Codificação
    "aplicar_codificacao_rotulos",
    "aplicar_dummy",
    # Features derivadas
    "calcular_valor_imc",
    "imc_classe",
    "calcular_heat_index",
    "calcular_ponto_orvalho",
    "calcular_tu_stull",
    "adicionar_features_derivadas",
    # Normalização
    "pick_scaler",
    "normalizar",
    "SCALERS",
]
