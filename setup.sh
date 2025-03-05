#!/bin/bash
# Script para configurar o ambiente do Agente de Engenharia de Prompt em sistemas Linux/Mac

echo "=== Configurando ambiente para o Agente de Engenharia de Prompt ==="

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não está instalado. Por favor, instale o Python 3 antes de continuar."
    exit 1
fi

# Cria o ambiente virtual
echo "Criando ambiente virtual..."
if [ -d "venv" ]; then
    echo "O ambiente virtual 'venv' já existe."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Erro ao criar o ambiente virtual."
        exit 1
    fi
    echo "Ambiente virtual criado com sucesso!"
fi

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Erro ao ativar o ambiente virtual."
    exit 1
fi

# Atualiza o pip (usando python -m pip para evitar problemas)
echo "Atualizando pip..."
python -m pip install --upgrade pip || echo "Atualização do pip falhou, mas continuaremos com a instalação."

# Instala as dependências
echo "Instalando dependências..."
if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Erro ao instalar as dependências."
        exit 1
    fi
fi

# Instala o pacote em modo de desenvolvimento
echo "Instalando o pacote em modo de desenvolvimento..."
python -m pip install -e .
if [ $? -ne 0 ]; then
    echo "Erro ao instalar o pacote."
    exit 1
fi

echo "=== Configuração concluída com sucesso! ==="
echo
echo "Para ativar o ambiente virtual, execute:"
echo "    source venv/bin/activate"
echo
echo "Para executar o agente, após ativar o ambiente, execute:"
echo "    python prompt_agent.py"
echo
echo "Ou, para fazer tudo de uma vez, execute:"
echo "    source venv/bin/activate && python prompt_agent.py" 