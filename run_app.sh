#!/bin/bash

echo "Iniciando o Agente de Engenharia de Prompt com interface Streamlit..."
echo

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Ambiente virtual não encontrado. Executando configuração..."
    python3 setup_env.py
else
    echo "Ambiente virtual encontrado."
fi

# Ativa o ambiente virtual e executa o aplicativo
echo "Ativando ambiente virtual..."
source venv/bin/activate

echo
echo "Iniciando a aplicação Streamlit..."
echo "Pressione Ctrl+C para encerrar."
echo

# Executa o script Python que inicia o Streamlit em vez do comando streamlit direto
python streamlit_run.py

# Desativa o ambiente virtual ao encerrar
deactivate
echo "Aplicação encerrada." 