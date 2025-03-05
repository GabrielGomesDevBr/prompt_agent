class Validator:
    """
    Classe para validar as respostas do agente contra respostas esperadas
    e calcular métricas de desempenho.
    """
    
    def __init__(self):
        """
        Inicializa o validador com respostas esperadas para testes.
        """
        # Dicionário de perguntas de teste e suas respostas esperadas
        self.expected_responses = {
            "O que é um prompt?": 
                "Um prompt é uma instrução dada a uma IA para obter uma resposta específica. É a entrada textual que orienta o modelo de linguagem sobre o que deve ser feito ou respondido.",
            
            "Me explique engenharia de prompt": 
                "Engenharia de Prompt é a prática de criar prompts eficazes para otimizar as respostas de modelos de IA. Envolve técnicas específicas para formular instruções que levam a respostas mais precisas, relevantes e úteis.",
            
            "Como faço para criar prompts melhores?": 
                "Para criar um bom prompt, você deve: 1) Ser claro e específico; 2) Fornecer contexto suficiente; 3) Definir o tom e formato desejados; 4) Incluir exemplos quando necessário; 5) Considerar o uso de delimitadores para separar instruções de contexto.",
            
            "Quais são os tipos de técnicas de prompting?": 
                "Algumas técnicas de Engenharia de Prompt incluem: 1) Zero-shot prompting; 2) Few-shot prompting com exemplos; 3) Chain-of-Thought (cadeia de pensamento); 4) Role prompting (definição de papéis); 5) Uso de delimitadores e estruturação; 6) Instruções passo a passo.",
            
            "O que é uma pergunta que não está na base de conhecimento?":
                "Desculpe, não sei responder isso. Posso ajudar com outra dúvida?"
        }
        
        # Adiciona palavras-chave para verificação em vez de correspondência exata no modo LLM
        self.key_concepts = {
            "O que é um prompt?": ["instrução", "modelo", "linguagem", "IA", "entrada textual"],
            "Me explique engenharia de prompt": ["otimizar", "eficazes", "instruções", "precisas", "técnicas"],
            "Como faço para criar prompts melhores?": ["claro", "específico", "contexto", "exemplo", "delimitadores"],
            "Quais são os tipos de técnicas de prompting?": ["zero-shot", "few-shot", "chain", "pensamento", "role"],
        }
        
        # Contadores para métricas
        self.total_tests = 0
        self.correct_responses = 0
    
    def validate_response(self, question, actual_response, is_llm_mode=False):
        """
        Valida se a resposta do agente corresponde à resposta esperada.
        
        Args:
            question (str): Pergunta de teste
            actual_response (str): Resposta fornecida pelo agente
            is_llm_mode (bool): Se True, usa validação baseada em palavras-chave
        
        Returns:
            bool: True se a resposta for válida, False caso contrário
        """
        self.total_tests += 1
        
        # Verifica se a pergunta está nos testes esperados
        for test_question, expected_response in self.expected_responses.items():
            # Normaliza as perguntas para comparação
            if question.lower().strip('?!.,;:') == test_question.lower().strip('?!.,;:'):
                # Se estiver no modo LLM, usa validação baseada em palavras-chave
                if is_llm_mode and test_question in self.key_concepts:
                    # Verifica se a resposta contém as palavras-chave esperadas
                    keywords = self.key_concepts[test_question]
                    matches = sum(1 for keyword in keywords if keyword.lower() in actual_response.lower())
                    # Considera válido se pelo menos 60% das palavras-chave estiverem presentes
                    is_valid = matches >= 0.6 * len(keywords)
                else:
                    # Compara as respostas (normaliza removendo espaços extras)
                    normalized_actual = ' '.join(actual_response.split())
                    normalized_expected = ' '.join(expected_response.split())
                    
                    # Compara o início da resposta (primeiros 50 caracteres)
                    # Este método é mais flexível que uma comparação exata
                    is_valid = normalized_actual.startswith(normalized_expected[:50])
                
                if is_valid:
                    self.correct_responses += 1
                
                return is_valid
        
        # Se a pergunta não está nas esperadas, assume como incorreta
        return False
    
    def get_accuracy_rate(self):
        """
        Calcula a taxa de precisão das respostas.
        
        Returns:
            float: Taxa de respostas precisas (0 a 100%)
            str: Mensagem formatada com a taxa
        """
        if self.total_tests == 0:
            return 0, "Nenhum teste realizado ainda."
        
        accuracy_rate = (self.correct_responses / self.total_tests) * 100
        message = f"Taxa de Respostas Precisas: {accuracy_rate:.2f}% ({self.correct_responses}/{self.total_tests})"
        
        return accuracy_rate, message
    
    def reset_metrics(self):
        """
        Reinicia os contadores de métricas.
        """
        self.total_tests = 0
        self.correct_responses = 0
    
    def add_expected_response(self, question, expected_response):
        """
        Adiciona uma nova resposta esperada ao conjunto de testes.
        
        Args:
            question (str): Pergunta de teste
            expected_response (str): Resposta esperada
        """
        self.expected_responses[question] = expected_response
        
    def run_all_tests(self, agent):
        """
        Executa todos os testes disponíveis usando o agente fornecido.
        
        Args:
            agent: Instância do agente que possui método get_response
            
        Returns:
            dict: Resultados dos testes com perguntas, respostas esperadas,
                 respostas reais e status de validação
        """
        self.reset_metrics()
        results = []
        
        # Determina se o agente está usando o modo LLM
        is_llm_mode = hasattr(agent, 'use_llm') and agent.use_llm
        
        for question, expected in self.expected_responses.items():
            # Obtém a resposta do agente
            actual, _ = agent.get_response(question)
            
            # Valida a resposta
            is_valid = self.validate_response(question, actual, is_llm_mode)
            
            # Adiciona aos resultados
            results.append({
                "question": question,
                "expected_response": expected,
                "actual_response": actual,
                "is_valid": is_valid
            })
        
        accuracy, message = self.get_accuracy_rate()
        
        return {
            "results": results,
            "accuracy_rate": accuracy,
            "message": message
        } 