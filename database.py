import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name="prompt_agent.db"):
        """
        Inicializa a estrutura do banco de dados.
        
        Args:
            db_name (str): Nome do arquivo de banco de dados
        """
        self.db_path = db_name
        # Garantir que as tabelas existam
        self._create_tables()
    
    def _get_connection(self):
        """
        Cria e retorna uma nova conexão com o banco de dados.
        Esta abordagem garante thread-safety no Streamlit.
        
        Returns:
            tuple: (conexão, cursor)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        return conn, cursor
    
    def _create_tables(self):
        """
        Cria as tabelas necessárias no banco de dados, caso não existam.
        """
        conn, cursor = self._get_connection()
        try:
            # Tabela para armazenar as interações
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_question TEXT NOT NULL,
                agent_response TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                patterns_insights TEXT
            )
            ''')
            conn.commit()
        finally:
            conn.close()
    
    def store_interaction(self, user_question, agent_response, patterns_insights=None):
        """
        Armazena uma interação no banco de dados.
        
        Args:
            user_question (str): Pergunta do usuário
            agent_response (str): Resposta fornecida pelo agente
            patterns_insights (str, optional): Padrões ou insights identificados
        
        Returns:
            int: ID da interação inserida
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn, cursor = self._get_connection()
        try:
            cursor.execute(
                "INSERT INTO interactions (user_question, agent_response, timestamp, patterns_insights) VALUES (?, ?, ?, ?)",
                (user_question, agent_response, timestamp, patterns_insights)
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        finally:
            conn.close()
    
    def get_all_interactions(self):
        """
        Recupera todas as interações armazenadas.
        
        Returns:
            list: Lista de tuplas contendo as interações
        """
        conn, cursor = self._get_connection()
        try:
            cursor.execute("SELECT * FROM interactions ORDER BY timestamp DESC")
            return cursor.fetchall()
        finally:
            conn.close()
    
    def get_interaction_by_id(self, interaction_id):
        """
        Recupera uma interação específica pelo ID.
        
        Args:
            interaction_id (int): ID da interação
        
        Returns:
            tuple: Dados da interação ou None se não encontrada
        """
        conn, cursor = self._get_connection()
        try:
            cursor.execute("SELECT * FROM interactions WHERE id = ?", (interaction_id,))
            return cursor.fetchone()
        finally:
            conn.close()
    
    def get_interactions_by_pattern(self, pattern):
        """
        Busca interações que contenham um padrão específico.
        
        Args:
            pattern (str): Padrão para busca
        
        Returns:
            list: Lista de interações que contêm o padrão
        """
        conn, cursor = self._get_connection()
        try:
            cursor.execute(
                "SELECT * FROM interactions WHERE user_question LIKE ? OR agent_response LIKE ?",
                (f'%{pattern}%', f'%{pattern}%')
            )
            return cursor.fetchall()
        finally:
            conn.close()
    
    def close(self):
        """
        Método mantido para compatibilidade com o código existente.
        Não faz nada, pois cada operação gerencia sua própria conexão.
        """
        pass 