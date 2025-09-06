import fitz  # PyMuPDF
import re

def extrair_questoes(pdf_path):
    """
    Extrai as questões de um arquivo PDF, separando o número, o enunciado e as alternativas.

    Args:
        pdf_path (str): O caminho para o arquivo PDF.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa uma questão
              com as chaves 'numero', 'enunciado' e 'alternativas'.
    """
    try:
        doc = fitz.open(pdf_path)
        texto_completo = ""
        for page in doc:
            texto_completo += page.get_text("text", flags=fitz.TEXTFLAGS_SEARCH)
        doc.close()

        # REGEX para capturar cada questão e seus componentes
        # Este regex é projetado para encontrar:
        # - O número da questão no início de uma linha
        # - O enunciado (todo o texto até as alternativas)
        # - O bloco de alternativas (de 'a)' até 'e)')
        regex_questoes = re.compile(
            r"^(?P<numero>\d+)\s*\n"  # Captura o número da questão
            r"(?P<enunciado>.*?)"     # Captura o enunciado
            r"(?P<alternativas>(?:^[a-e]\).*?)+)" # Captura o bloco de alternativas
            r"(?=\n\d+\s*\n|\Z)",    # Delimita o fim da questão (lookahead)
            re.MULTILINE | re.DOTALL
        )

        questoes_extraidas = []
        for match in regex_questoes.finditer(texto_completo):
            dados_questao = match.groupdict()
            
            # Limpa e formata os dados extraídos
            numero = int(dados_questao['numero'].strip())
            enunciado = dados_questao['enunciado'].strip()
            
            # Separa as alternativas em uma lista
            bloco_alternativas = dados_questao['alternativas'].strip()
            alternativas = re.split(r'\n(?=[a-e]\))', bloco_alternativas)
            
            questoes_extraidas.append({
                "numero": numero,
                "enunciado": enunciado,
                "alternativas": [alt.strip() for alt in alternativas]
            })
            
        return questoes_extraidas

    except Exception as e:
        print(f"Ocorreu um erro ao processar o PDF: {e}")
        return []