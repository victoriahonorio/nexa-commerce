"""
Monta o agente de RAG: busca no indice vetorial + LLM que responde
citando a fonte.
"""

import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()  # le o arquivo .env (na raiz do projeto) e carrega GOOGLE_API_KEY

EMBEDDINGS = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

PROMPT = ChatPromptTemplate.from_template("""
Voce e o assistente de onboarding e buddy program da NexaCommerce.
Responda a pergunta usando APENAS o contexto abaixo. Sempre cite o
arquivo de origem da informacao. Se a resposta nao estiver no
contexto, diga claramente que nao encontrou essa informacao nos
documentos disponiveis - nunca invente.

Contexto:
{context}

Pergunta: {pergunta}
""")


def montar_agente():
    indice = Chroma(persist_directory="./indice_vetorial", embedding_function=EMBEDDINGS)
    buscador = indice.as_retriever(search_kwargs={"k": 4})

    chave = os.getenv("GOOGLE_API_KEY")
    if not chave:
        raise RuntimeError(
            "GOOGLE_API_KEY nao encontrada. Crie um arquivo .env na raiz "
            "do projeto (mesma pasta do agente.py) com a linha:\n"
            "GOOGLE_API_KEY=sua-chave-aqui"
        )
    # gemini-2.5-flash confirmado ativo em ago/2026 (tier gratuito) - nomes
    # de modelo mudam com frequencia, confira o mais recente em
    # ai.google.dev/gemini-api/docs/models
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0, google_api_key=chave)

    def formatar_contexto(docs):
        return "\n\n".join(f"[{d.metadata['fonte']}] {d.page_content}" for d in docs)

    cadeia = (
        {"context": buscador | formatar_contexto, "pergunta": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )
    return cadeia


if __name__ == "__main__":
    agente = montar_agente()
    resposta = agente.invoke("Como funciona o programa de buddy da NexaCommerce?")
    print(resposta)
