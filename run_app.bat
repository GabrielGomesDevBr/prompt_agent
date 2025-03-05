@echo off
echo Iniciando o Agente de Engenharia de Prompt com interface Streamlit...
echo.

REM Verifica se o ambiente virtual existe
if not exist "venv" (
    echo Ambiente virtual nao encontrado. Executando configuracao...
    python setup_env.py
) else (
    echo Ambiente virtual encontrado.
)

REM Ativa o ambiente virtual e executa o aplicativo
echo Ativando ambiente virtual...
call venv\Scripts\activate

echo.
echo Iniciando a aplicacao Streamlit...
echo Pressione Ctrl+C para encerrar.
echo.

REM Executa o script Python que inicia o Streamlit em vez do comando streamlit direto
python streamlit_run.py

REM Desativa o ambiente virtual ao encerrar
call deactivate
echo Aplicacao encerrada. 