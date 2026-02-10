"""
Carregador de credenciais ClearML do arquivo .env

Carrega e configura credenciais do ClearML a partir do arquivo .env
"""
import os
from pathlib import Path
from config.logger_config import logger

def carregar_credenciais_clearml() -> bool:
    """
    Carrega credenciais do ClearML do arquivo .env e configura ambiente.
    
    Returns:
        bool: True se credenciais foram carregadas com sucesso
    """
    # Procurar arquivo .env na raiz do projeto
    # Subir 3 níveis: src/clearml/utils -> src/clearml -> src -> raiz
    env_path = Path(__file__).parent.parent.parent.parent / '.env'
    
    if not env_path.exists():
        logger.warning(f"Arquivo .env não encontrado em: {env_path}")
        return False
    
    # Ler arquivo .env
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        credenciais = {}
        for linha in linhas:
            linha = linha.strip()
            if linha and not linha.startswith('#') and '=' in linha:
                chave, valor = linha.split('=', 1)
                credenciais[chave.strip()] = valor.strip()
        
        # Verificar credenciais obrigatórias
        chaves_necessarias = [
            'CLEARML_WEB_HOST',
            'CLEARML_API_HOST',
            'CLEARML_FILES_HOST',
            'CLEARML_API_ACCESS_KEY',
            'CLEARML_API_SECRET_KEY'
        ]
        
        faltando = [c for c in chaves_necessarias if c not in credenciais]
        if faltando:
            logger.error(f"Credenciais faltando no .env: {faltando}")
            return False
        
        # Configurar variáveis de ambiente
        for chave, valor in credenciais.items():
            os.environ[chave] = valor
        
        logger.info("✓ Credenciais ClearML carregadas do .env")
        logger.info(f"  API Host: {credenciais['CLEARML_API_HOST']}")
        logger.info(f"  Web Host: {credenciais['CLEARML_WEB_HOST']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao carregar credenciais do .env: {e}")
        return False


def configurar_clearml_online() -> bool:
    """
    Configura ClearML para uso online (servidor remoto).
    
    Returns:
        bool: True se configuração foi bem-sucedida
    """
    if not carregar_credenciais_clearml():
        return False
    
    try:
        from clearml import Task
        
        # Tentar configurar credenciais programaticamente
        Task.set_credentials(
            api_host=os.environ.get('CLEARML_API_HOST'),
            web_host=os.environ.get('CLEARML_WEB_HOST'),
            files_host=os.environ.get('CLEARML_FILES_HOST'),
            key=os.environ.get('CLEARML_API_ACCESS_KEY'),
            secret=os.environ.get('CLEARML_API_SECRET_KEY')
        )
        
        logger.info("✓ ClearML configurado para uso ONLINE")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao configurar ClearML: {e}")
        return False
