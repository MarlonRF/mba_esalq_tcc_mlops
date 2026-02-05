#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar diretórios necessários com permissões adequadas.
Usado principalmente em ambientes CI/CD onde podem haver restrições de permissão.
"""

import os
import stat
import tempfile


def setup_directories():
    """Cria diretórios necessários com permissões adequadas."""
    directories = [
        'modelos',
        'api', 
        'logs',
        'graficos',
        'dados'
    ]
    
    success_count = 0
    
    for dir_name in directories:
        try:
            # Tenta criar o diretório com permissões adequadas
            os.makedirs(dir_name, mode=0o755, exist_ok=True)
            
            # Verifica e ajusta permissões se necessário
            current_mode = os.stat(dir_name).st_mode
            if not (current_mode & stat.S_IWUSR):
                os.chmod(dir_name, 0o750)
                
            print(f" Diretório {dir_name} criado/verificado com sucesso")
            success_count += 1
            
        except (PermissionError, OSError) as e:
            print(f" Não foi possível configurar {dir_name}: {e}")
            print(f" Isso pode causar problemas ao salvar arquivos neste diretório")
    
    print(f"\n Resultado: {success_count}/{len(directories)} diretórios configurados com sucesso")
    
    # Verifica se pelo menos api/ foi criado (essencial)
    if 'api' not in [d for d in directories if os.path.exists(d) and os.access(d, os.W_OK)]:
        print(" AVISO: Diretório 'api' não está acessível para escrita!")
        print("   Modelos serão salvos na raiz do projeto como fallback")
    
    return success_count == len(directories)


def check_write_permissions():
    """Verifica permissões de escrita nos diretórios principais."""
    print("\nVerificando permissões de escrita...")
    
    test_dirs = ['modelos', 'api', '.']  # Inclui diretório atual como fallback
    writable_dirs = []
    
    for dir_name in test_dirs:
        if os.path.exists(dir_name):
            try:
                # Tenta criar um arquivo temporário para testar escrita
                test_file = os.path.join(dir_name, '.write_test')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                writable_dirs.append(dir_name)
                print(f"{dir_name}/ - escrita OK")
            except (PermissionError, OSError):
                print(f"{dir_name}/ - sem permissão de escrita")
        else:
            print(f"{dir_name}/ - diretório não existe")
    
    if not writable_dirs:
        print("ERRO CRÍTICO: Nenhum diretório disponível para escrita!")
        return False
    
    print(f"\nDiretórios disponíveis para escrita: {', '.join(writable_dirs)}")
    return True


def main():
    """Função principal do script."""
    print("Configurando diretórios para pipeline MLOps...")
    print("=" * 50)
    
    # Configura diretórios
    dirs_ok = setup_directories()
    
    # Verifica permissões
    write_ok = check_write_permissions()
    
    print("\n" + "=" * 50)
    if dirs_ok and write_ok:
        print("Configuração concluída com sucesso!")
        exit(0)
    else:
        print("Configuração concluída com avisos")
    
        exit(0)  # Não falha o CI/CD, apenas avisa


if __name__ == "__main__":
    main()