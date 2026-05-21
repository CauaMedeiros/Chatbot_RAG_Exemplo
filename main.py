from chatbot import Bot
import streamlit as st
from dotenv import load_dotenv
import os

# Configuração da página
st.set_page_config(
    page_title="Chatbot RAG",
    layout="wide"
)

# Cria o bot apenas uma vez
if "bot" not in st.session_state:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    # Mantém um perfil padrão, caso sua classe Bot precise disso
    profile_number = 0

    st.session_state.bot = Bot(api_key)

# Cria um ID fixo para o usuário
# Isso é útil caso o método generate_response precise de um user_id
if "user_id" not in st.session_state:
    st.session_state.user_id = "usuario_demo"

# Histórico de mensagens
if "message_log" not in st.session_state:
    st.session_state.message_log = [
        {
            "role": "assistant",
            "content": "Olá! Sou um chatbot com RAG. Qual é a sua dúvida?"
        }
    ]

st.title("Chatbot com RAG")

# Exibe mensagens antigas
for message in st.session_state.message_log:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
query = st.chat_input("Digite sua pergunta...")

if query:
    # Mostra mensagem do usuário
    st.session_state.message_log.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    # Gera resposta do chatbot
    with st.chat_message("assistant"):
        with st.spinner("Buscando resposta..."):
            response = st.session_state.bot.generate_response(
                query,
                st.session_state.user_id
            )

            answer = response["answer"]

            st.markdown(answer)

    # Salva resposta no histórico
    st.session_state.message_log.append({
        "role": "assistant",
        "content": answer
    })
