from setuptools import setup, find_packages

setup(
    name="prompt_agent",
    version="0.1.0",
    description="Um agente inteligente para apoiar equipes com conceitos de Engenharia de Prompt",
    author="Academia Lendária",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "openai>=1.0.0",  # SDK oficial da OpenAI para interagir com os modelos
        "pyyaml>=6.0",    # Para leitura de arquivos de configuração YAML
        "python-dotenv>=1.0.0",  # Para gerenciar variáveis de ambiente (opcional)
        "streamlit>=1.30.0"  # Para a interface web interativa
    ],
) 