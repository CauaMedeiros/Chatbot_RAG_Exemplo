from typing import Dict
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class Bot:
    def __init__(self, api_key):
        self.api_key = api_key

        # Modelo responsável por gerar as respostas
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            google_api_key=api_key,
            temperature=0.6
        )

        # Modelo responsável por transformar textos em embeddings
        self.embedding = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key
        )

        # Pasta onde o banco vetorial será salvo
        self.persist_directory = "./db"

        # Arquivo usado como base de conhecimento da RAG
        self.files_dir = "RAG.txt"

        # Configurações da divisão do texto em chunks
        self.chunk_size = 1000
        self.chunk_overlap = 200

        # Quantidade máxima de interações salvas no histórico
        self.max_history = 5
        self.history_handler = HistoryHandler()

        # Cria o banco vetorial a partir do arquivo RAG.txt
        self.vectordb = self.create_vector_db()

        # Cria o prompt usado pelo chatbot
        self.prompt = self.create_prompt()

        # Configura o mecanismo de busca dos documentos relevantes
        self.retriever = self.vectordb.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.2}
        )

        # Cadeia que combina os documentos recuperados com o prompt
        self.combine_docs_chain = create_stuff_documents_chain(
            self.llm,
            self.prompt
        )

        # Cadeia final de RAG: recupera contexto e gera resposta
        self.retrieval_chain = create_retrieval_chain(
            self.retriever,
            self.combine_docs_chain
        )

    def create_prompt(self):
        # Instruções principais do comportamento do chatbot
        system_msg = """
        Você é um bot que ajuda na resolução de diversos problemas.
        """

        # Template que organiza histórico, pergunta e contexto recuperado
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_msg.strip()),
            ("human", """
            Histórico da conversa:
            {conversation_history}

            Pergunta:
            {input}

            Contexto:
            {context}
            """)
        ])

        return prompt

    def create_vector_db(self):
        # Carrega o arquivo de texto usado como base de conhecimento
        loader = TextLoader(
            file_path=self.files_dir,
            encoding="utf-8"
        )

        documents = loader.load()

        # Divide o documento em pedaços menores
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        texts = text_splitter.split_documents(documents)

        # Cria o banco vetorial com os chunks e seus embeddings
        vectordb = Chroma.from_documents(
            documents=texts,
            persist_directory=self.persist_directory,
            embedding=self.embedding
        )

        return vectordb

    def format_conversation_history(self, user_id: str) -> str:
        # Busca o histórico de conversa do usuário
        conversation_history = self.history_handler.get_user_history(user_id)

        if not conversation_history:
            return "Nenhum histórico de conversa anterior."

        formatted_history = []

        # Formata o histórico para ser enviado no prompt
        for i, (question, answer) in enumerate(conversation_history, 1):
            formatted_history.append(f"Pergunta {i}: {question}")
            formatted_history.append(f"Resposta {i}: {answer}\n")

        return "\n".join(formatted_history)

    def generate_response(self, query: str, user_id: str) -> Dict:
        # Monta os dados de entrada para a cadeia RAG
        input_dict = {
            "input": query,
            "conversation_history": self.format_conversation_history(user_id)
        }

        # Executa a busca de contexto e gera a resposta
        result = self.retrieval_chain.invoke(input_dict)

        # Salva a nova interação no histórico
        if "answer" in result:
            history = self.history_handler.get_user_history(user_id)

            history.append((query, result["answer"]))

            # Mantém apenas as últimas interações
            if len(history) > self.max_history:
                history.pop(0)

            self.history_handler.update_history(user_id, history)

        return result


class HistoryHandler:
    def __init__(self):
        # Dicionário que armazena o histórico por usuário
        self.history_list = {}

    def get_user_history(self, user_id):
        # Cria um histórico vazio caso o usuário ainda não exista
        if user_id not in self.history_list:
            self.history_list[user_id] = []

        return self.history_list[user_id]

    def update_history(self, user_id, history):
        # Atualiza o histórico do usuário
        self.history_list[user_id] = history