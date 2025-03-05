"""
Script auxiliar para iniciar a aplicação Streamlit.
Usado como contorno quando o comando streamlit não está disponível diretamente.
"""
import sys
import subprocess
import os
import time

def is_package_installed(package_name):
    """Verifica se um pacote está instalado."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_streamlit():
    """Instala o Streamlit se não estiver disponível."""
    print("Instalando Streamlit...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    print("Streamlit instalado com sucesso!")

def main():
    """Inicia a aplicação Streamlit."""
    # Verifica se o Streamlit está instalado
    if not is_package_installed("streamlit"):
        install_streamlit()
    
    # Define o caminho para o script app.py
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    
    # Executa o Streamlit como um processo separado
    print(f"Iniciando aplicação Streamlit: {app_path}")
    
    # Usando o método mais confiável para iniciar o Streamlit
    cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--browser.gatherUsageStats=false"]
    
    # Inicia o processo e não espera por ele (ele continuará rodando em segundo plano)
    if os.name == 'nt':  # Windows
        # No Windows, usamos CREATE_NEW_PROCESS_GROUP para evitar que Ctrl+C afete o processo filho
        process = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:  # Unix/Linux/Mac
        # Em sistemas Unix, iniciamos o processo em um novo grupo de processos
        process = subprocess.Popen(cmd, preexec_fn=os.setpgrp)
    
    # Imprime mensagem informando o uso do serviço LLM
    print("Usando serviço LLM para responder perguntas.")
    print("A aplicação Streamlit foi iniciada. Você pode acessá-la em http://localhost:8501")
    print("O processo continuará em execução em segundo plano.")
    print("Para encerrá-lo, feche o navegador e termine o processo manualmente.")
    
    # Aguarda alguns segundos para garantir que o Streamlit inicie corretamente
    time.sleep(3)

if __name__ == "__main__":
    main() 