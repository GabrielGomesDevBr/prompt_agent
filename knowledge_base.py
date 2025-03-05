class KnowledgeBase:
    """
    Classe que representa a base de conhecimento do agente com FAQs sobre
    Engenharia de Prompt e boas práticas.
    """
    
    def __init__(self):
        """
        Inicializa a base de conhecimento com perguntas e respostas predefinidas.
        """
        # Dicionário de perguntas frequentes (FAQs) e suas respostas
        self.faqs = {
            "o que é um prompt": "Um prompt é uma instrução dada a uma IA para obter uma resposta específica. É a entrada textual que orienta o modelo de linguagem sobre o que deve ser feito ou respondido.",
            
            "como criar um bom prompt": "Para criar um bom prompt, você deve: 1) Ser claro e específico; 2) Fornecer contexto suficiente; 3) Definir o tom e formato desejados; 4) Incluir exemplos quando necessário; 5) Considerar o uso de delimitadores para separar instruções de contexto.",
            
            "o que é engenharia de prompt": "Engenharia de Prompt é a prática de criar prompts eficazes para otimizar as respostas de modelos de IA. Envolve técnicas específicas para formular instruções que levam a respostas mais precisas, relevantes e úteis.",
            
            "quais são as técnicas de engenharia de prompt": "Algumas técnicas de Engenharia de Prompt incluem: 1) Zero-shot prompting; 2) Few-shot prompting com exemplos; 3) Chain-of-Thought (cadeia de pensamento); 4) Role prompting (definição de papéis); 5) Uso de delimitadores e estruturação; 6) Instruções passo a passo.",
            
            "o que é zero-shot prompting": "Zero-shot prompting é uma técnica onde você pede ao modelo para realizar uma tarefa sem fornecer exemplos específicos. O modelo usa seu conhecimento geral para responder com base apenas na instrução dada.",
            
            "o que é few-shot prompting": "Few-shot prompting é uma técnica onde você fornece alguns exemplos (geralmente de 1 a 5) do tipo de resposta que deseja antes de fazer sua pergunta principal. Isso ajuda a calibrar o modelo para o formato e estilo desejados.",
            
            "o que é chain-of-thought": "Chain-of-Thought (Cadeia de Pensamento) é uma técnica que incentiva o modelo a mostrar seu raciocínio passo a passo antes de chegar à resposta final. Isso geralmente melhora a precisão em tarefas complexas de raciocínio.",
            
            "como estruturar um prompt eficaz": "Um prompt eficaz geralmente segue esta estrutura: 1) Contexto claro; 2) Papel ou persona definida; 3) Tarefa específica; 4) Formato desejado para a resposta; 5) Restrições ou limitações; 6) Informações adicionais relevantes; 7) Exemplos quando necessário.",
            
            "quais são as boas práticas em engenharia de prompt": "Boas práticas incluem: 1) Ser específico e direto; 2) Usar delimitadores para separar seções; 3) Especificar o formato de saída desejado; 4) Testar e iterar prompts; 5) Definir personas ou papéis; 6) Incluir verificações de raciocínio; 7) Considerar limitações do modelo.",
            
            "o que são delimitadores em prompts": "Delimitadores são caracteres ou sequências específicas usadas para separar diferentes partes de um prompt, como contexto, instruções e exemplos. Exemplos comuns incluem: ```, ''', ###, <texto>, [texto], etc. Eles ajudam o modelo a distinguir claramente as diferentes seções do prompt.",
            
            "como avaliar a qualidade de um prompt": "A qualidade de um prompt pode ser avaliada por: 1) Precisão das respostas geradas; 2) Consistência dos resultados; 3) Capacidade de seguir instruções específicas; 4) Relevância do conteúdo para o objetivo; 5) Taxa de rejeição ou respostas inadequadas; 6) Feedback dos usuários finais.",
            
            "o que é role prompting": "Role prompting (ou prompting de papel) é uma técnica onde você atribui um papel específico ao modelo de IA, como 'Você é um especialista em marketing' ou 'Atue como um professor de matemática'. Isso ajuda a orientar o tom, estilo e tipo de conhecimento que o modelo deve utilizar na resposta.",
            
            "como lidar com prompts ambíguos": "Para lidar com prompts ambíguos: 1) Peça clarificações específicas; 2) Ofereça interpretações alternativas da pergunta; 3) Estruture a resposta considerando diferentes possibilidades; 4) Mencione explicitamente as ambiguidades identificadas; 5) Revise e refine o prompt original para reduzir ambiguidades."
        }
    
    def get_response(self, question):
        """
        Busca uma resposta para a pergunta na base de conhecimento.
        
        Args:
            question (str): Pergunta do usuário
        
        Returns:
            tuple: (resposta, encontrada) onde resposta é a string com a resposta
                  e encontrada é um booleano indicando se a resposta foi encontrada
        """
        # Normaliza a pergunta para comparação (minúsculas e sem pontuação)
        normalized_question = question.lower().strip('?!.,;:')
        
        # Verifica se a pergunta normalizada está na base de conhecimento
        for key, value in self.faqs.items():
            if key in normalized_question or normalized_question in key:
                return value, True
        
        # Se não encontrar correspondência exata, tenta encontrar palavras-chave
        for key, value in self.faqs.items():
            key_words = set(key.split())
            question_words = set(normalized_question.split())
            
            # Se pelo menos 70% das palavras-chave estiverem presentes
            if len(key_words.intersection(question_words)) >= 0.7 * len(key_words):
                return value, True
        
        # Se não encontrar nenhuma correspondência
        return "Desculpe, não sei responder isso. Posso ajudar com outra dúvida?", False
    
    def add_faq(self, question, answer):
        """
        Adiciona uma nova pergunta e resposta à base de conhecimento.
        
        Args:
            question (str): Nova pergunta
            answer (str): Resposta correspondente
        """
        normalized_question = question.lower().strip('?!.,;:')
        self.faqs[normalized_question] = answer
        
    def get_all_faqs(self):
        """
        Retorna todas as perguntas e respostas na base de conhecimento.
        
        Returns:
            dict: Dicionário com as perguntas e respostas
        """
        return self.faqs 