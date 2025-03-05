#!/usr/bin/env python3
"""
Script para configurar um ambiente virtual para o Agente de Prompt.
Este script:
1. Cria um ambiente virtual (venv)
2. Ativa o ambiente virtual
3. Instala as dependências necessárias
4. Configura o ambiente para execução
"""

import os
import sys
import subprocess
import platform

def create_venv():
    """Cria um ambiente virtual Python."""
    print("Criando ambiente virtual...")
    
    venv_dir = "venv"
    
    # Verifica se o ambiente virtual já existe
    if os.path.exists(venv_dir):
        print(f"O ambiente virtual '{venv_dir}' já existe.")
        return venv_dir
    
    # Cria o ambiente virtual
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
        print(f"Ambiente virtual '{venv_dir}' criado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar ambiente virtual: {e}")
        sys.exit(1)
    
    return venv_dir

def get_activation_command(venv_dir):
    """Retorna o comando para ativar o ambiente virtual de acordo com o sistema operacional."""
    if platform.system() == "Windows":
        return f"{venv_dir}\\Scripts\\activate"
    else:  # Linux/Mac
        return f"source {venv_dir}/bin/activate"

def install_dependencies(venv_dir):
    """Instala as dependências no ambiente virtual."""
    print("Instalando dependências...")
    
    # Define os caminhos de executáveis com base no sistema operacional
    if platform.system() == "Windows":
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:  # Linux/Mac
        python_exe = os.path.join(venv_dir, "bin", "python")
        pip_exe = os.path.join(venv_dir, "bin", "pip")
    
    try:
        # Usamos python -m pip para evitar problemas de atualização do pip
        # Atualiza pip
        print("Atualizando pip...")
        subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], 
                     check=False)  # Não exigimos que seja bem-sucedido
        
        # Instala dependências do requirements.txt se existir
        if os.path.exists("requirements.txt"):
            print("Instalando dependências do requirements.txt...")
            subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True)
        
        # Instala o pacote em modo de desenvolvimento
        print("Instalando o pacote em modo de desenvolvimento...")
        subprocess.run([python_exe, "-m", "pip", "install", "-e", "."], 
                     check=True)
        
        print("Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar dependências: {e}")
        sys.exit(1)

def main():
    """Função principal para configurar o ambiente."""
    print("=== Configurando ambiente para o Agente de Engenharia de Prompt ===")
    
    # Cria o ambiente virtual
    venv_dir = create_venv()
    
    # Instala as dependências
    install_dependencies(venv_dir)
    
    # Imprime instruções de ativação
    activation_cmd = get_activation_command(venv_dir)
    
    print("\n=== Configuração completa! ===")
    print("\nPara ativar o ambiente virtual, execute:")
    print(f"\n    {activation_cmd}")
    print("\nEm seguida, para executar o agente:")
    print("\n    python prompt_agent.py")
    
if __name__ == "__main__":
    main() 