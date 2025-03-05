# Agente de Engenharia de Prompt - Academia Lendária

Este projeto implementa um agente inteligente para apoiar a equipe da Academia Lendária com conceitos de Engenharia de Prompt e boas práticas. A aplicação foi desenvolvida em Python e oferece duas opções de funcionamento:

1. **Modo LLM**: Utiliza um modelo de linguagem avançado via API para gerar respostas mais completas e contextuais.
2. **Modo Local**: Utiliza uma base de conhecimento local pré-definida (fallback para quando a API não está disponível).

A aplicação utiliza SQLite como banco de dados para armazenar interações, implementa um mecanismo de fallback inteligente, gera outputs estruturados com insights e permite validação externa das respostas.

## Funcionalidades

- **Integração com LLM**: Conecta-se a um modelo de linguagem avançado via API.
- **Base de Conhecimento**: Contém FAQs sobre Engenharia de Prompt e boas práticas.
- **Armazenamento de Interações**: Todas as interações são armazenadas em um banco de dados SQLite.
- **Mecanismo de Fallback**: Detecta quando o agente não tem uma resposta e retorna mensagem padrão.
- **Geração de Insights**: Identifica padrões e categorias nas perguntas dos usuários.
- **Validação Externa**: Interface para testar e validar as respostas do agente contra respostas esperadas.
- **Output Estruturado**: Gera respostas estruturadas com informações adicionais e insights.
- **Interface Web com Streamlit**: Interface gráfica elegante e interativa para facilitar o uso do agente.

## Estrutura do Projeto

- `prompt_agent.py`: Arquivo principal contendo a lógica do agente.
- `llm_service.py`: Serviço para comunicação com o modelo LLM.
- `database.py`: Gerencia a conexão e operações com SQLite.
- `knowledge_base.py`: Armazena a base de conhecimento (FAQs) para uso local.
- `validator.py`: Implementa as funções de validação externa.
- `config.yaml`: Arquivo de configuração com as credenciais e configurações do modelo LLM.
- `app.py`: Interface web com Streamlit para interagir com o agente.
- `setup_env.py`: Script Python para configurar o ambiente virtual.
- `setup.sh`: Script shell para configuração em Linux/Mac.
- `setup.bat`: Script batch para configuração em Windows.
- `requirements.txt`: Lista de dependências do projeto.
- `setup.py`: Configuração para instalação do pacote.
- `prompt_agent.db`: Banco de dados SQLite (criado automaticamente na primeira execução).

## Requisitos

- Python 3.6 ou superior
- SQLite3 (normalmente já vem com a instalação do Python)
- Acesso à Internet (para o modo LLM)
- Uma chave de API válida para o modelo de linguagem (configurada no arquivo config.yaml)
- Streamlit (para a interface web)

## Configuração do LLM

O arquivo `config.yaml` contém as configurações necessárias para conectar a aplicação a um modelo LLM:

```yaml
api_key:
  key: "sua-chave-api-aqui"
model:
  name: "gpt-4o"    # Outras opções: "gpt-3.5-turbo", "o3-mini", "o1-mini", "gpt-4o-mini"
  
agent:
  temperature: 0.7    # Controla a aleatoriedade das respostas (0.0 a 1.0)
  max_tokens: 1000    # Número máximo de tokens na resposta
  system_prompt: "..."  # Prompt de sistema para orientar o modelo
```

Edite este arquivo antes de executar a aplicação para configurar sua chave de API e preferências do modelo.

## Instalação

### Método 1: Usando os Scripts de Configuração (Recomendado)

#### Para Windows:

1. Clone o repositório ou faça o download dos arquivos:

```
git clone <url-do-repositorio>
cd agente-engenharia-prompt
```

2. Execute o script de configuração:

```
setup.bat
```

#### Para Linux/Mac:

1. Clone o repositório:

```
git clone <url-do-repositorio>
cd agente-engenharia-prompt
```

2. Dê permissão de execução e execute o script:

```
chmod +x setup.sh
./setup.sh
```

### Método 2: Usando o Script Python

1. Clone o repositório:

```
git clone <url-do-repositorio>
cd agente-engenharia-prompt
```

2. Execute o script de configuração do ambiente:

```
python setup_env.py
```

3. Ative o ambiente virtual:

No Windows:
```
venv\Scripts\activate
```

No Linux/Mac:
```
source venv/bin/activate
```

### Método 3: Configuração Manual

1. Clone o repositório:

```
git clone <url-do-repositorio>
cd agente-engenharia-prompt
```

2. Crie e ative um ambiente virtual:

No Windows:
```
python -m venv venv
venv\Scripts\activate
```

No Linux/Mac:
```
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```
pip install -e .
```

## Uso

### Interface de Linha de Comando

Para iniciar o agente na linha de comando, execute:

```
python prompt_agent.py
```

### Interface Web com Streamlit

Para iniciar a interface web Streamlit, execute:

```
streamlit run app.py
```

Isso abrirá uma interface web interativa no seu navegador padrão, normalmente em http://localhost:8501.

### Comandos disponíveis:

Na versão de linha de comando:
- Digite sua pergunta sobre Engenharia de Prompt para obter uma resposta.
- Digite `histórico` para ver o histórico da conversa.
- Digite `testar` para executar testes de validação.
- Digite `limpar` para reiniciar a conversa.
- Digite `modo` para alternar entre o modo LLM e o modo de base de conhecimento local.
- Digite `sair` para encerrar o agente.

Na interface Streamlit:
- Use o campo de chat para digitar suas perguntas
- Use o sidebar para:
  - Alternar entre modos LLM e base local
  - Limpar a conversa
  - Executar testes de validação

## Funcionamento Interno

### Modo LLM vs. Modo Local

A aplicação pode operar em dois modos:

1. **Modo LLM**: Utiliza a API do modelo configurado para gerar respostas. Este modo oferece:
   - Respostas mais naturais e contextuais
   - Capacidade de lidar com perguntas complexas
   - Extração avançada de insights

2. **Modo Local**: Utiliza a base de conhecimento embutida. Este modo é utilizado:
   - Quando a API não está disponível ou falha
   - Como fallback automático em caso de erro
   - Quando o usuário prefere uma resposta mais rápida e determinística

Você pode alternar entre os modos digitando `modo` durante a execução do agente ou usando o checkbox na interface Streamlit.

### Prompt Interno

O agente é guiado por um prompt interno que define seu comportamento e características, configurado no arquivo `config.yaml`.

### Base de Dados

O banco de dados SQLite armazena:
- Pergunta do usuário
- Resposta gerada
- Data/hora da interação
- Padrões ou insights identificados

### Métricas de Validação

A aplicação implementa a métrica "Taxa de Respostas Precisas (%)" para medir a eficácia do agente, comparando respostas geradas com respostas corretas pré-definidas.

## Extensões Possíveis

1. **Integração com outros provedores de LLM**: Adicionar suporte para outros modelos e provedores.
2. **Expansão da Interface Web**: Adicionar mais recursos visuais e interativos à interface Streamlit.
3. **Expansão da Base de Conhecimento**: Implementar mecanismos para atualizar a base automaticamente.
4. **Aprendizado de Máquina**: Incorporar técnicas de ML para melhorar a detecção de intenções e respostas.

## Solução de Problemas

### Problemas com o LLM
- Se enfrentar problemas com a conexão à API, verifique sua chave de API no arquivo `config.yaml`.
- Use o toggle na interface ou o comando `modo` para alternar para o modo de base de conhecimento local em caso de problemas com a API.

### Problemas com Streamlit
- Se encontrar problemas ao iniciar a interface Streamlit, verifique se instalou todas as dependências corretamente.
- Se a página não carregar, verifique se não há outro serviço usando a porta 8501.

### Banco de Dados
- Se encontrar erros relacionados ao banco de dados, verifique se o SQLite está instalado corretamente.
- Para reiniciar o banco de dados, basta excluir o arquivo `prompt_agent.db` e executar o agente novamente.

### Ambiente Virtual
- Se encontrar problemas ao ativar o ambiente virtual, verifique se o Python está instalado corretamente.
- Em alguns sistemas, pode ser necessário usar `python3` em vez de `python`.
- Se o script de configuração falhar, tente criar o ambiente manualmente conforme as instruções no Método 3.

