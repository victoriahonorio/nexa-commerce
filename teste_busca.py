from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

print("Carregando modelo de embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("Conectando ao banco Chroma...")
indice = Chroma(persist_directory="./indice_vetorial", embedding_function=embeddings)

pergunta_teste = "Quantas horas por semana meu buddy tem disponível para mim?"
print(f"\nBuscando por: '{pergunta_teste}'\n")

# Faz a busca direto no banco, sem usar o Gemini
resultados = indice.similarity_search(pergunta_teste, k=4)

if not resultados:
    print("❌ ERRO: O Chroma não encontrou NENHUM documento. O banco está vazio ou a indexação falhou.")
else:
    print(f"✅ SUCESSO: O Chroma encontrou {len(resultados)} trechos!\n")
    for i, doc in enumerate(resultados):
        print(f"--- Trecho {i+1} (Fonte: {doc.metadata.get('fonte', 'Desconhecida')}) ---")
        print(f"{doc.page_content[:300]}...\n")