"""
Leitura dos documentos da NexaCommerce a partir do OCI Object Storage.
Acesso via Pre-Authenticated Request (PAR) de bucket inteiro - sem SDK,
sem chave de API, so requests + a URL do PAR.
"""

import io
from pypdf import PdfReader
import requests

# Cole aqui a URL do PAR copiada no Console (termina em "/o/").
# Formato: https://objectstorage.SUA-REGIAO.oraclecloud.com/p/SEU-TOKEN/n/SEU-NAMESPACE/b/SEU-BUCKET/o/
BASE_PAR_URL = "https://objectstorage.sa-saopaulo-1.oraclecloud.com/p/Mrq2Nwb_QbwrixLF23v1r_I58qSB03QXdjt5AVWGWuvwy_CpgWvDnLJqyTwKVTLi/n/grozlcquk1bs/b/nexacommerce-docs/o/"

# Nomes dos arquivos exatamente como estao no bucket
DOCUMENTOS = [
    "FAQ_de_Sistemas_e_Acessos_Operacionais.pdf",
    "Guia_da_Jornada_de_Onboarding.pdf",
    "Manual_do_Programa_de_Buddy.pdf",
    "Source_of_Truth_Onboarding_Buddy_e_BAU.pdf"
    # adicione os demais arquivos aqui
]


def extrair_texto_pdf(conteudo_bytes: bytes) -> str:
    """Extrai o texto de um PDF a partir dos bytes baixados."""
    leitor = PdfReader(io.BytesIO(conteudo_bytes))
    paginas = [pagina.extract_text() or "" for pagina in leitor.pages]
    return "\n".join(paginas)


def carregar_documentos() -> dict[str, str]:
    """Baixa cada PDF do Object Storage (via PAR) e devolve {nome: texto}."""
    textos = {}
    for nome in DOCUMENTOS:
        resposta = requests.get(BASE_PAR_URL + nome, timeout=30)
        resposta.raise_for_status()
        textos[nome] = extrair_texto_pdf(resposta.content)
        print(f"OK: {nome} ({len(textos[nome])} caracteres extraidos)")
    return textos


if __name__ == "__main__":
    documentos = carregar_documentos()
