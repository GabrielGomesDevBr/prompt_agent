import json
import re
import yaml
from datetime import datetime
from database import Database
from knowledge_base import KnowledgeBase
from validator import Validator
from llm_service import LLMService

class PromptAgent:
    """
    Agente inteligente para apoiar a equipe da Academia Lendária com conceitos
    de Engenharia de Prompt e boas práticas.
    """
    
    def __init__(self, config_path="config.yaml", use_llm=True):
        """
        Inicializa o agente com a base de conhecimento ou serviço LLM e conexão ao banco de dados.
        
        Args:
            config_path (str): Caminho para o arquivo de configuração
            use_llm (bool): Se True, usa o serviço LLM; se False, usa a base de conhecimento local
        """
        # Variáveis para armazenar dados dinâmicos
        self.conversation_context = []
        self.user_info = {}
        self.last_query = None
        self.last_response = None
        self.use_llm = use_llm
        
        # Carrega a configuração
        self.config = self._load_config(config_path)
        
        # Inicializa componentes
        self.db = Database(self.config.get('database', {}).get('path', 'prompt_agent.db'))
        self.validator = Validator()
        
        # Inicializa base de conhecimento ou serviço LLM com base na configuração
        if self.use_llm:
            self.llm_service = LLMService(config_path)
            print("Usando serviço LLM para responder perguntas.")
        else:
            self.kb = KnowledgeBase()
            print("Usando base de conhecimento local para responder perguntas.")
        
        # Prompt interno que guia o comportamento do agente
        self.internal_prompt = self.config.get('agent', {}).get('system_prompt', """
# Prompt do Agente de Suporte em Engenharia de Prompt

**Contexto:** Você é um agente inteligente criado para ajudar a equipe da Academia Lendária com conceitos de Engenharia de Prompt e boas práticas. Sua missão é responder perguntas de forma clara, armazenar interações para análise e aumentar a autonomia da equipe.

**Instruções:**
1. **Responda às perguntas com base na base de conhecimento:**
   - Forneça explicações simples e exemplos práticos para perguntas sobre Engenharia de Prompt ou boas práticas.
   - Exemplo: Se perguntarem "O que é um prompt?", responda: "Um prompt é uma instrução dada a uma IA para obter uma resposta específica."

2. **Armazene dados dinâmicos:**
   - Guarde a pergunta do usuário (`user_input`), o contexto da conversa (`context`) e a resposta gerada (`response`).

3. **Mecanismo de Fallback:**
   - Se a pergunta não estiver na base de conhecimento, retorne: "Desculpe, não sei responder isso. Posso ajudar com outra dúvida?"

4. **Gere insights:**
   - Identifique padrões nas perguntas (ex.: dúvidas frequentes) e registre para análise.
""")
    
    def _load_config(self, config_path):
        """
        Carrega a configuração do arquivo YAML.
        
        Args:
            config_path (str): Caminho para o arquivo de configuração
            
        Returns:
            dict: Configuração carregada
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            return config
        except Exception as e:
            print(f"Erro ao carregar o arquivo de configuração: {e}")
            return {}
    
    def get_response(self, user_query):
        """
        Processa a pergunta do usuário e retorna uma resposta adequada.
        
        Args:
            user_query (str): Pergunta do usuário
            
        Returns:
            tuple: (resposta, encontrada) onde resposta é a string com a resposta
                  e encontrada é um booleano indicando se a resposta foi encontrada
        """
        # Armazena a última consulta
        self.last_query = user_query
        
        # Adiciona a consulta ao contexto da conversa
        self.conversation_context.append({
            "role": "user",
            "content": user_query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Obtém a resposta da fonte apropriada (LLM ou base de conhecimento)
        if self.use_llm:
            # Prepara o contexto da conversa para enviar ao modelo LLM (últimas 5 interações)
            context_messages = []
            for msg in self.conversation_context[-10:]:  # Usa as últimas 5 interações (máximo)
                if msg["role"] == "user":
                    context_messages.append(f"Usuário: {msg['content']}")
                else:
                    context_messages.append(f"Agente: {msg['content']}")
            
            # Enriquece o prompt com o contexto da conversa
            context_text = "\n".join(context_messages[:-1]) if len(context_messages) > 1 else ""
            enhanced_prompt = user_query
            if context_text:
                enhanced_prompt = f"Contexto da conversa anterior:\n{context_text}\n\nPergunta atual: {user_query}"
            
            # Obtém a resposta do serviço LLM
            response, found = self.llm_service.get_completion(
                enhanced_prompt, 
                system_prompt=self.internal_prompt
            )
            
            # Se houver erro na chamada da API, tenta usar a base de conhecimento local como fallback
            if not found and hasattr(self, 'kb'):
                print("Erro na chamada da API LLM. Usando base de conhecimento local como fallback.")
                response, found = self.kb.get_response(user_query)
                
        else:
            # Usa a base de conhecimento local
            response, found = self.kb.get_response(user_query)
        
        # Armazena a resposta
        self.last_response = response
        
        # Adiciona a resposta ao contexto da conversa
        self.conversation_context.append({
            "role": "agent",
            "content": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Identifica e armazena insights
        insights = self._extract_insights(user_query, response, found)
        
        # Armazena a interação no banco de dados
        self.db.store_interaction(user_query, response, json.dumps(insights))
        
        return response, found
    
    def _extract_insights(self, query, response, found):
        """
        Extrai insights da interação entre usuário e agente.
        
        Args:
            query (str): Pergunta do usuário
            response (str): Resposta fornecida
            found (bool): Se a resposta foi encontrada
            
        Returns:
            dict: Insights extraídos da interação
        """
        if self.use_llm:
            # Usa o LLM para extrair insights mais sofisticados
            return self.llm_service.extract_insights(query, response)
        else:
            # Usa a abordagem baseada em regras para análise básica
            insights = {
                "category": "unknown",
                "patterns": [],
                "possible_improvements": []
            }
            
            # Identifica a categoria da pergunta
            if "o que é" in query.lower() or "definição" in query.lower():
                insights["category"] = "definição"
            elif "como" in query.lower() or "passos" in query.lower():
                insights["category"] = "procedimento"
            elif "diferença" in query.lower() or "versus" in query.lower() or " vs " in query.lower():
                insights["category"] = "comparação"
            elif "exemplo" in query.lower() or "demonstre" in query.lower():
                insights["category"] = "exemplificação"
            
            # Identifica padrões na pergunta
            if not found:
                insights["patterns"].append("pergunta_sem_resposta")
                
                # Tenta identificar tópicos para expandir a base de conhecimento
                topics = self._extract_topics(query)
                if topics:
                    insights["possible_improvements"].append(f"Adicionar informações sobre: {', '.join(topics)}")
            
            # Verifica se a pergunta é relacionada a técnicas específicas
            techniques = ["zero-shot", "few-shot", "chain of thought", "role prompting", "delimitadores"]
            for technique in techniques:
                if technique in query.lower():
                    insights["patterns"].append(f"interesse_em_{technique.replace(' ', '_')}")
            
            return insights
    
    def _extract_topics(self, text):
        """
        Extrai possíveis tópicos de interesse de um texto.
        
        Args:
            text (str): Texto para extração de tópicos
            
        Returns:
            list: Lista de tópicos identificados
        """
        # Lista de palavras-chave relevantes
        keywords = ["prompt", "engenharia", "IA", "modelo", "LLM", "ChatGPT", "GPT", 
                   "resposta", "instrução", "contexto", "exemplo", "técnica"]
        
        # Extrai palavras do texto
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filtra por palavras-chave ou frases
        topics = [word for word in words if word in keywords or len(word) > 7]
        
        return list(set(topics))  # Remove duplicatas
    
    def get_conversation_history(self):
        """
        Retorna o histórico completo da conversa.
        
        Returns:
            list: Lista com mensagens da conversa
        """
        return self.conversation_context
    
    def clear_conversation(self):
        """
        Limpa o histórico da conversa atual.
        """
        self.conversation_context = []
    
    def get_structured_output(self):
        """
        Gera um output estruturado com a última interação e insights.
        
        Returns:
            dict: Dados estruturados da interação
        """
        if not self.last_query or not self.last_response:
            return {"status": "Nenhuma interação registrada"}
        
        # Busca as últimas N interações no banco de dados
        interactions = self.db.get_all_interactions()
        recent_interactions = interactions[:5] if interactions else []
        
        # Formata as interações para o output
        formatted_interactions = []
        for interaction in recent_interactions:
            try:
                insights = json.loads(interaction[4]) if interaction[4] else {}
            except:
                insights = {}
                
            formatted_interactions.append({
                "id": interaction[0],
                "question": interaction[1],
                "response": interaction[2],
                "timestamp": interaction[3],
                "insights": insights
            })
        
        return {
            "current_interaction": {
                "query": self.last_query,
                "response": self.last_response,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "recent_interactions": formatted_interactions,
            "conversation_length": len(self.conversation_context)
        }
    
    def close(self):
        """
        Fecha conexões e libera recursos.
        """
        self.db.close()


def main():
    """
    Função principal para executar o agente interativamente.
    """
    print("\n=== Agente de Engenharia de Prompt da Academia Lendária ===")
    print("Digite 'sair' para encerrar, 'histórico' para ver conversas anteriores,")
    print("'testar' para executar testes de validação, 'limpar' para reiniciar a conversa,")
    print("ou 'modo' para alternar entre LLM e base de conhecimento local.\n")
    
    # Por padrão, usa o LLM se a configuração estiver disponível
    try:
        # Tenta carregar o arquivo de configuração para verificar se o LLM está configurado
        with open("config.yaml", 'r') as file:
            config = yaml.safe_load(file)
        if config.get('api_key', {}).get('key'):
            use_llm = True
        else:
            use_llm = False
    except:
        # Se não conseguir carregar o arquivo, usa a base de conhecimento local
        use_llm = False
    
    agent = PromptAgent(use_llm=use_llm)
    
    try:
        while True:
            user_input = input("\nVocê: ")
            
            if user_input.lower() == 'sair':
                break
                
            elif user_input.lower() == 'histórico':
                history = agent.get_conversation_history()
                print("\n=== Histórico da Conversa ===")
                for msg in history:
                    role = "Você" if msg["role"] == "user" else "Agente"
                    print(f"{role} ({msg['timestamp']}): {msg['content']}")
                    
            elif user_input.lower() == 'testar':
                print("\n=== Executando Testes de Validação ===")
                results = agent.validator.run_all_tests(agent)
                print(results["message"])
                print(f"Detalhes: {len(results['results'])} testes executados")
                
                # Mostra detalhes dos testes que falharam
                failed_tests = [r for r in results["results"] if not r["is_valid"]]
                if failed_tests:
                    print(f"\nTestes falhos ({len(failed_tests)}):")
                    for i, test in enumerate(failed_tests, 1):
                        print(f"{i}. Pergunta: {test['question']}")
                        print(f"   Esperado: {test['expected_response'][:50]}...")
                        print(f"   Recebido: {test['actual_response'][:50]}...")
            
            elif user_input.lower() == 'modo':
                # Alterna entre o modo LLM e o modo de base de conhecimento local
                agent.use_llm = not agent.use_llm
                mode = "LLM" if agent.use_llm else "base de conhecimento local"
                print(f"\nModo alterado para: {mode}")
                        
            elif user_input.lower() == 'limpar':
                agent.clear_conversation()
                print("Conversa reiniciada!")
                
            else:
                response, found = agent.get_response(user_input)
                print(f"\nAgente: {response}")
                
                # Se for uma resposta da base de conhecimento, oferece detalhes
                if found and not agent.use_llm:
                    print("\n[Informação encontrada na base de conhecimento]")
                
                # A cada 3 interações, mostra insights
                if len(agent.get_conversation_history()) % 6 == 0:
                    output = agent.get_structured_output()
                    insights = output.get("recent_interactions", [])[0].get("insights", {})
                    if insights and insights.get("category"):
                        print(f"\n[Insight: Sua pergunta foi classificada como '{insights.get('category')}']")
                    
    except KeyboardInterrupt:
        print("\nEncerrando o agente...")
    finally:
        agent.close()
        print("\nAgente encerrado. Obrigado por utilizar!")


if __name__ == "__main__":
    main() 