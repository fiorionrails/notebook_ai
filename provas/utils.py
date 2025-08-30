import fitz  # PyMuPDF

def extrair_questoes(pdf_path):
    doc = fitz.open(pdf_path)
    texto = ""
    for page in doc:
        texto += page.get_text()
    questoes = texto.split("Questão")  # quebra simples pelo padrão "Questão"
    questoes = [q.strip() for q in questoes if q.strip()]
    return questoes
