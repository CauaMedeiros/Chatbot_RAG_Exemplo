# Chatbot com RAG no Replit

Este projeto e um exemplo de chatbot com RAG usando:

- **Streamlit** para criar a interface do chat.
- **LangChain** para organizar a cadeia de RAG.
- **Gemini** para gerar respostas e criar embeddings.
- **ChromaDB** para guardar e buscar os textos da base de conhecimento.
- **RAG.txt** como arquivo de conhecimento usado pelo bot.

RAG significa **Retrieval-Augmented Generation**. Em vez de o modelo responder apenas com o que ja sabe, o sistema primeiro busca trechos relevantes em uma base de conhecimento e depois usa esses trechos como contexto para responder.

## 1. Estrutura do projeto

O projeto deve ter estes arquivos:

```text
.
+-- .replit
+-- chatbot.py
+-- main.py
+-- RAG.txt
+-- README.md
+-- requirements.txt
```

Funcao de cada arquivo:

- `main.py`: cria a tela do chatbot com Streamlit.
- `chatbot.py`: contem a classe `Bot`, que carrega o RAG, cria o banco vetorial e gera respostas.
- `RAG.txt`: base de conhecimento usada pelo chatbot.
- `requirements.txt`: lista as bibliotecas Python que precisam ser instaladas.
- `.replit`: configura o comando que o Replit executa ao clicar em **Run**.

## 2. Criar o projeto no Replit

1. Acesse [https://replit.com](https://replit.com).
2. Crie um novo Repl usando o template **Python**.
3. Envie ou crie no Replit os arquivos deste projeto:
   - `.replit`
   - `main.py`
   - `chatbot.py`
   - `RAG.txt`
   - `requirements.txt`
   - `README.md`
4. Confirme que os nomes dos arquivos estao exatamente iguais aos nomes acima.

O arquivo `.replit` ja esta configurado para rodar:

```bash
streamlit run main.py --server.port 8501 --server.headless true
```

Por isso, depois de configurar tudo, o bot deve abrir pelo botao **Run** do Replit.

## 3. Instalar as dependencias

O Replit geralmente instala automaticamente as dependencias listadas em `requirements.txt`.

Se isso nao acontecer, abra a aba **Shell** no Replit e rode:

```bash
pip install -r requirements.txt
```

As principais dependencias sao:

- `streamlit`
- `langchain`
- `langchain-google-genai`
- `langchain-chroma`
- `chromadb`

## 4. Criar a chave da API do Gemini

O chatbot precisa de uma chave da API do Gemini para funcionar.

1. Acesse [Google AI Studio](https://aistudio.google.com/apikey).
2. Crie uma API key.
3. Copie a chave gerada.

Importante: nao cole a chave diretamente no codigo. A chave deve ficar em uma variavel de ambiente.

## 5. Configurar a chave no Replit

No Replit, use **Secrets** para guardar a chave com seguranca.

1. Abra o painel de **Secrets** no Replit.
2. Crie um novo Secret.
3. No campo **Key**, coloque exatamente:

```text
GEMINI_API_KEY
```

4. No campo **Value**, cole a chave da API do Gemini.
5. Salve o Secret.

O codigo busca essa chave no arquivo `main.py`:

```python
api_key = os.getenv("GEMINI_API_KEY")
```

Se o nome do Secret estiver diferente, o chatbot nao conseguira acessar a API.

## 6. Rodar o chatbot

Depois de instalar as dependencias e configurar o Secret:

1. Clique em **Run** no Replit.
2. Aguarde o Streamlit iniciar.
3. Abra a janela web que o Replit mostrar.
4. Digite uma pergunta no chat.

Para testar com a base atual, pergunte:

```text
O que significa ECT?
```

O bot deve responder usando a informacao que esta em `RAG.txt`.

## 7. Como o codigo funciona

### Interface

O arquivo `main.py` cria a pagina com Streamlit:

- configura o titulo da pagina;
- cria o bot uma unica vez usando `st.session_state`;
- guarda o historico das mensagens;
- recebe a pergunta do usuario com `st.chat_input`;
- mostra a resposta do chatbot na tela.

### Base de conhecimento

O arquivo `RAG.txt` e a fonte de conhecimento do bot.

Exemplo:

```text
ECT significa Escola de Ciencia e Tecnologia.
```

Voce pode trocar o conteudo desse arquivo para adaptar o chatbot ao tema da aula.

### Banco vetorial

No arquivo `chatbot.py`, o metodo `create_vector_db` faz quatro etapas:

1. Carrega o arquivo `RAG.txt`.
2. Divide o texto em partes menores.
3. Transforma essas partes em embeddings.
4. Salva os embeddings no ChromaDB.

Esse banco vetorial e usado para encontrar os trechos mais parecidos com a pergunta do usuario.

### Geracao da resposta

Quando o usuario faz uma pergunta:

1. O bot procura trechos relevantes no banco vetorial.
2. Esses trechos entram no prompt como contexto.
3. O Gemini gera a resposta usando a pergunta, o contexto e o historico da conversa.
4. A resposta aparece na interface do Streamlit.

## 8. Como alterar a base de conhecimento

Para usar outro conteudo na aula:

1. Abra o arquivo `RAG.txt`.
2. Apague o texto atual.
3. Cole o novo conteudo.
4. Rode o projeto novamente.

Exemplo:

```text
Python e uma linguagem de programacao muito usada em ciencia de dados, automacao e desenvolvimento web.
Streamlit e uma biblioteca Python que permite criar aplicativos web de forma simples.
RAG e uma tecnica que combina busca de informacao com geracao de texto.
```

Depois disso, faca perguntas relacionadas ao novo conteudo.

Se o bot continuar respondendo com informacoes antigas, apague a pasta `db` criada pelo ChromaDB e rode o projeto novamente. Essa pasta e gerada automaticamente.
