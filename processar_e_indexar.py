"""
Processa os documentos ja baixados (etapa 1) e monta o indice
vetorial local com Chroma.
"""

from carregar_documentos import carregar_documentos
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

EMBEDDINGS = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def dividir_em_chunks(documentos: dict[str, str]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = []
    for nome_arquivo, texto in documentos.items():
        for parte in splitter.split_text(texto):
            chunks.append(Document(page_content=parte, metadata={"fonte": nome_arquivo}))
    return chunks


def criar_indice(chunks: list[Document]) -> Chroma:
    return Chroma.from_documents(
        documents=chunks,
        embedding=EMBEDDINGS,
        persist_directory="./indice_vetorial",
    )


if __name__ == "__main__":
    documentos = carregar_documentos()
    chunks = dividir_em_chunks(documentos)
    indice = criar_indice(chunks)
    print(f"Indice criado com {len(chunks)} chunks.")
