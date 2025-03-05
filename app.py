import streamlit as st
import yaml
import json
import os
from prompt_agent import PromptAgent

# Configuração da página Streamlit
st.set_page_config(
    page_title="Agente de Engenharia de Prompt - Academia Lendária",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para carregar as configurações
def load_config():
    if os.path.exists("config.yaml"):
        with open("config.yaml", 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    return {}

# Verifica se há uma chave API configurada
def is_api_key_configured():
    config = load_config()
    return bool(config.get('api_key', {}).get('key'))

# Inicialização da sessão
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
    
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
if 'agent' not in st.session_state:
    st.session_state.agent = None
    
if 'use_llm' not in st.session_state:
    # Por padrão, usa o LLM se a configuração estiver disponível
    st.session_state.use_llm = is_api_key_configured()

# Função para inicializar ou reiniciar o agente
def initialize_agent():
    if st.session_state.agent:
        st.session_state.agent.close()
    
    st.session_state.agent = PromptAgent(use_llm=st.session_state.use_llm)
    st.session_state.conversation_started = True
    st.session_state.messages = []

# Sidebar com configurações
with st.sidebar:
    st.title("Configurações")
    
    # Opção para alternar entre LLM e base local
    use_llm = st.checkbox("Usar LLM", value=st.session_state.use_llm)
    
    if use_llm != st.session_state.use_llm:
        st.session_state.use_llm = use_llm
        if st.session_state.conversation_started:
            initialize_agent()
    
    # Botões de ação
    if st.button("Limpar Conversa"):
        if st.session_state.agent:
            st.session_state.agent.clear_conversation()
        st.session_state.messages = []
    
    if st.button("Executar Testes"):
        if not st.session_state.agent:
            initialize_agent()
        
        with st.spinner("Executando testes..."):
            results = st.session_state.agent.validator.run_all_tests(st.session_state.agent)
            
        st.write("### Resultados dos Testes")
        st.write(results["message"])
        st.write(f"Taxa de Precisão: {results['accuracy_rate']:.1f}%")
        
        # Exibe detalhes dos testes
        with st.expander("Ver detalhes dos testes"):
            for i, test in enumerate(results["results"], 1):
                status = "✅" if test["is_valid"] else "❌"
                st.write(f"{status} **Teste {i}:** {test['question']}")
                if not test["is_valid"]:
                    st.write(f"- Esperado: {test['expected_response'][:100]}...")
                    st.write(f"- Recebido: {test['actual_response'][:100]}...")
    
    # Exibe o status do LLM
    st.write("---")
    if st.session_state.use_llm:
        st.success("📡 Modo LLM ativo")
    else:
        st.info("📚 Usando base de conhecimento local")
    
    st.write("---")
    st.write("### Sobre")
    st.write("Agente de Engenharia de Prompt da Academia Lendária")
    st.write("Versão 1.0")

# Título principal
st.title("🤖 Agente de Engenharia de Prompt")
st.write("Tire suas dúvidas sobre Engenharia de Prompt e melhores práticas")

# Inicializa o agente se necessário
if not st.session_state.conversation_started:
    initialize_agent()

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        # Se for uma mensagem do agente e tiver insights, mostra-os
        if message.get("insights") and message["role"] == "assistant":
            with st.expander("Ver insights"):
                st.json(message["insights"])

# Input para nova mensagem
if prompt := st.chat_input("Digite sua pergunta ou 'histórico' para ver conversas anteriores"):
    # Adiciona a mensagem do usuário ao chat
    with st.chat_message("user"):
        st.write(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Comandos especiais
    if prompt.lower() == 'histórico':
        # Obtém o histórico de conversas do banco de dados
        history = st.session_state.agent.get_conversation_history()
        
        with st.chat_message("assistant"):
            st.write("### Histórico de Conversas")
            for msg in history:
                role = "Usuário" if msg["role"] == "user" else "Agente"
                st.write(f"**{role}** ({msg['timestamp']}): {msg['content']}")
                
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Histórico de conversas exibido acima."
        })
    else:
        # Processa a pergunta normal
        with st.spinner("Pensando..."):
            response, found = st.session_state.agent.get_response(prompt)
            
            # Obtém insights da última interação
            last_interaction = st.session_state.agent.get_structured_output()
            insights = {}
            if last_interaction.get("recent_interactions"):
                insights = last_interaction["recent_interactions"][0].get("insights", {})
        
        # Exibe a resposta
        with st.chat_message("assistant"):
            st.write(response)
            
            # Exibe informações adicionais conforme disponível
            if not st.session_state.use_llm and found:
                st.info("Informação encontrada na base de conhecimento local")
            
        # Adiciona a resposta do assistente ao histórico da sessão
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "insights": insights
        })

# Rodapé
st.write("---")
st.write("Digite suas perguntas sobre Engenharia de Prompt no campo acima.")
st.write("Use 'histórico' para ver conversas anteriores armazenadas no banco de dados.") 