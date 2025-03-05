import yaml
import openai
import json
from typing import Dict, Any, Optional, List, Tuple

class LLMService:
    """
    Classe responsável por gerenciar a comunicação com o modelo LLM.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Inicializa o serviço LLM com configurações do arquivo YAML.
        
        Args:
            config_path (str): Caminho para o arquivo de configuração YAML
        """
        self.config = self._load_config(config_path)
        self._setup_client()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Carrega as configurações do arquivo YAML.
        
        Args:
            config_path (str): Caminho para o arquivo de configuração
            
        Returns:
            Dict[str, Any]: Configurações carregadas
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            return config
        except Exception as e:
            raise Exception(f"Erro ao carregar o arquivo de configuração: {e}")
    
    def _setup_client(self):
        """
        Configura o cliente da API de LLM com base na configuração.
        """
        api_key = self.config.get('api_key', {}).get('key')
        if not api_key:
            raise ValueError("API key não encontrada na configuração.")
        
        # Configurar o cliente OpenAI
        self.client = openai.OpenAI(api_key=api_key)
    
    def get_completion(self, 
                       prompt: str, 
                       system_prompt: Optional[str] = None,
                       temperature: Optional[float] = None,
                       max_tokens: Optional[int] = None) -> Tuple[str, bool]:
        """
        Envia uma solicitação ao modelo LLM e obtém uma resposta.
        
        Args:
            prompt (str): Pergunta ou prompt do usuário
            system_prompt (str, optional): Prompt de sistema para orientar o modelo
            temperature (float, optional): Temperatura para controlar a aleatoriedade
            max_tokens (int, optional): Número máximo de tokens na resposta
            
        Returns:
            Tuple[str, bool]: (Resposta do modelo, indicador de sucesso)
        """
        try:
            # Obter configurações do arquivo de configuração ou usar valores padrão
            model_name = self.config.get('model', {}).get('name', 'gpt-4o')
            _temperature = temperature or self.config.get('agent', {}).get('temperature', 0.7)
            _max_tokens = max_tokens or self.config.get('agent', {}).get('max_tokens', 1000)
            _system_prompt = system_prompt or self.config.get('agent', {}).get('system_prompt', '')
            
            # Preparar mensagens para o modelo
            messages = []
            
            # Adicionar o prompt de sistema se fornecido
            if _system_prompt:
                messages.append({"role": "system", "content": _system_prompt})
            
            # Adicionar a mensagem do usuário
            messages.append({"role": "user", "content": prompt})
            
            # Enviar a solicitação ao modelo
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=_temperature,
                max_tokens=_max_tokens
            )
            
            # Extrair a resposta do modelo
            answer = response.choices[0].message.content.strip()
            
            return answer, True
            
        except Exception as e:
            error_message = f"Desculpe, ocorreu um erro ao processar sua solicitação: {str(e)}"
            return error_message, False
    
    def extract_insights(self, query: str, response: str) -> Dict[str, Any]:
        """
        Extrai insights da interação entre usuário e modelo.
        
        Args:
            query (str): Pergunta do usuário
            response (str): Resposta do modelo
            
        Returns:
            Dict[str, Any]: Insights extraídos
        """
        try:
            # Preparar um prompt para extrair insights
            insight_prompt = f"""
            Analise a seguinte interação entre um usuário e um agente de IA sobre Engenharia de Prompt:
            
            Pergunta do usuário: "{query}"
            
            Resposta do agente: "{response}"
            
            Por favor, extraia e forneça os seguintes insights no formato JSON:
            1. category: Categoria da pergunta (definição, procedimento, comparação, exemplificação, ou outro)
            2. patterns: Lista de padrões identificados na pergunta
            3. possible_improvements: Sugestões para melhorar a base de conhecimento
            
            Retorne apenas o JSON sem explicações adicionais.
            """
            
            # Obter insights do modelo
            model_name = self.config.get('model', {}).get('name', 'gpt-4o')
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": insight_prompt}],
                temperature=0.3,  # Baixa temperatura para respostas mais consistentes
                max_tokens=500
            )
            
            # Extrair e analisar o JSON da resposta
            insights_text = response.choices[0].message.content.strip()
            
            # Tentar extrair o JSON se estiver embutido em blocos de código
            if "```json" in insights_text:
                json_str = insights_text.split("```json")[1].split("```")[0].strip()
            elif "```" in insights_text:
                json_str = insights_text.split("```")[1].strip()
            else:
                json_str = insights_text
            
            insights = json.loads(json_str)
            return insights
            
        except Exception as e:
            # Retornar um insight padrão em caso de erro
            return {
                "category": "unknown",
                "patterns": ["erro_na_analise"],
                "possible_improvements": [f"Melhorar a extração de insights: {str(e)}"]
            } 