
# Assistente de Onboarding e Buddy Program — NexaCommerce

Agente de IA que responde, em linguagem natural, perguntas de novos colaboradores da NexaCommerce sobre onboarding, o Programa de Buddy, sistemas internos e políticas de RH — com base nos documentos oficiais da empresa, sempre citando a fonte.

Projeto desenvolvido para o desafio final **Alura Agent** (imersão ONE — Oracle Next Education — em parceria com a Alura).

## 📋 Sobre o projeto

Colaboradores recém-chegados gastam tempo procurando informação espalhada em manuais internos (onboarding, buddy program, FAQ de sistemas). Este agente centraliza essas respostas: qualquer pessoa pergunta em linguagem natural e recebe uma resposta direta, com a fonte citada — sem precisar abrir nenhum PDF.

## 🏗️ Arquitetura

```text
Documentos (PDF)  →  Processamento + RAG local   →  Agente + LLM        →  Interface + Deploy
NexaCommerce          chunking → embeddings →         LangChain +           Streamlit
                       Chroma (busca vetorial)         Gemini                (local e Streamlit
                                                                              Community Cloud)
      ↑
OCI Object Storage (Pre-Authenticated Request)

```

1. **Documentos**: os PDFs de onboarding/buddy program ficam num bucket privado no **OCI Object Storage**, acessados via Pre-Authenticated Request (PAR) — cumpre o requisito do desafio de usar ao menos 1 serviço do ecossistema OCI no processo.
2. **Processamento + RAG local**: o texto é dividido em chunks (`langchain-text-splitters`), transformado em vetores (`sentence-transformers`, local e gratuito) e indexado no **Chroma**.
3. **Agente + LLM**: o **LangChain** orquestra a busca semântica no índice e envia o contexto recuperado para o **Gemini**, que responde citando sempre o documento de origem — e admite quando não sabe, em vez de inventar.
4. **Interface + Deploy**: chat simples em **Streamlit**, rodando localmente ou publicado no **Streamlit Community Cloud**.

## 🛠️ Tecnologias utilizadas

| Camada | Ferramenta |
| --- | --- |
| Armazenamento de documentos | OCI Object Storage (Pre-Authenticated Request) |
| Leitura de PDF | pypdf |
| Chunking | langchain-text-splitters |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`, local) |
| Banco vetorial | Chroma |
| Orquestração do agente | LangChain |
| LLM | Google Gemini (`gemini-2.5-flash`) via langchain-google-genai |
| Interface | Streamlit |
| Deploy | Streamlit Community Cloud |
| Segredos | python-dotenv (local) / Streamlit Secrets (produção) |

## ⚙️ Como rodar localmente

Pré-requisitos: Python 3.10+ e uma chave de API do Gemini ([aistudio.google.com/apikey](https://aistudio.google.com/apikey), gratuita).

```bash
# 1. Clonar o repositório
git clone <url-do-seu-repositorio>
cd <pasta-do-projeto>

# 2. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Configurar a chave de API
# crie um arquivo .env na raiz do projeto com:
# GOOGLE_API_KEY=sua_chave_aqui

# 5. Rodar o pipeline, na ordem
python carregar_documentos.py       # baixa e extrai os PDFs da OCI
python processar_e_indexar.py       # cria o índice vetorial (Chroma)
python agente.py                    # testa o agente com uma pergunta de exemplo

# 6. Subir a interface
streamlit run app.py

```

## 💬 Exemplos de uso


<img width="1437" height="871" alt="Image" src="https://github.com/user-attachments/assets/d264cc4f-ec9d-44d6-b8e7-09cb9fc6d5ba" />

**Pergunta:** Posso ser reembolsado por bebida alcoólica em viagem a trabalho?
**Resposta:** Não. Bebidas alcoólicas não são reembolsáveis sob nenhuma circunstância administrativa, segundo a política de Travel & Expenses. *[fonte: Source_of_Truth_Onboarding_Buddy_e_BAU.pdf]*

**Pergunta:** Quando meu notebook corporativo chega?
**Resposta:** O IT Support despacha o notebook por transportadora rastreada com previsão de chegada até 3 dias úteis antes do seu Dia 1. Se não chegar até o fim do dia anterior ao início, abra um chamado P2 no ServiceNow. *[fonte: FAQ_de_Sistemas_e_Acessos_Operacionais.pdf]*

## ☁️ Deploy

* **Aplicação em produção:** `https://nexa-commerce.streamlit.app/`
* **Evidência do deploy na OCI:** `https://cloud.oracle.com/object-storage/buckets/grozlcquk1bs/nexacommerce-docs/details?region=sa-saopaulo-1`

## 📁 Estrutura do projeto

```text
.
├── carregar_documentos.py     # Etapa 1 — baixa os PDFs do OCI Object Storage
├── processar_e_indexar.py     # Etapa 2 — chunking, embeddings e índice Chroma
├── agente.py                  # Etapa 3 — agente RAG (LangChain + Gemini)
├── app.py                     # Etapa 4 — interface Streamlit
├── requirements.txt
├── .env.example                # copie para .env e preencha sua chave (nunca commite o .env real)
├── .gitignore
└── README.md
