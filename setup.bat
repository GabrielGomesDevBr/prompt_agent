@echo off
REM Script para configurar o ambiente do Agente de Engenharia de Prompt em sistemas Windows

echo === Configurando ambiente para o Agente de Engenharia de Prompt ===

REM Verifica se o Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Erro: Python nao esta instalado. Por favor, instale o Python antes de continuar.
    exit /b 1
)

REM Cria o ambiente virtual
echo Criando ambiente virtual...
if exist venv (
    echo O ambiente virtual 'venv' ja existe.
) else (
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Erro ao criar o ambiente virtual.
        exit /b 1
    )
    echo Ambiente virtual criado com sucesso!
)

REM Ativa o ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Erro ao ativar o ambiente virtual.
    exit /b 1
)

REM Atualiza o pip (usando python -m pip para evitar problemas)
echo Atualizando pip...
python -m pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 (
    echo Atualização do pip falhou, mas continuaremos com a instalação.
)

REM Instala as dependências
echo Instalando dependencias...
if exist requirements.txt (
    python -m pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Erro ao instalar as dependencias.
        exit /b 1
    )
)

REM Instala o pacote em modo de desenvolvimento
echo Instalando o pacote em modo de desenvolvimento...
python -m pip install -e .
if %ERRORLEVEL% NEQ 0 (
    echo Erro ao instalar o pacote.
    exit /b 1
)

echo === Configuracao concluida com sucesso! ===
echo.
echo Para ativar o ambiente virtual, execute:
echo     venv\Scripts\activate.bat
echo.
echo Para executar o agente, apos ativar o ambiente, execute:
echo     python prompt_agent.py
echo.
echo Ou, para fazer tudo de uma vez, execute:
echo     venv\Scripts\activate.bat ^&^& python prompt_agent.py 