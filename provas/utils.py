import fitz  # PyMuPDF
import requests
import json
import re

def analisar_pdf_com_ia(caminho_pdf):
    """
    Analisa o texto de um PDF usando um modelo generativo local (phi3 via Ollama)
    para extrair questões e seus metadados em um formato JSON estruturado.
    """
    try:
        doc = fitz.open(caminho_pdf)
        texto_completo = ""
        for page in doc:
            texto_completo += page.get_text()
        doc.close()

        # Divida o texto em questões (ajuste conforme o padrão do seu PDF)
        questoes = re.split(r'\n\d+\.', texto_completo)
        resultados = []

        for idx, questao in enumerate(questoes[1:], 1):  # Pula o cabeçalho
            prompt = f"""
Extraia os campos abaixo da questão a seguir e responda SOMENTE com o JSON solicitado, sem explicações, comentários ou texto fora do JSON. Não escreva nada além do JSON. Se não conseguir, responda {{"questoes":[]}}.

Campos:
- "numero": {idx}
- "enunciado": texto completo da questão, incluindo alternativas
- "resposta": letra da resposta correta, se houver
- "disciplina": null
- "dificuldade": null

Formato de resposta:
{{
  "questoes": [
    {{
      "numero": ...,
      "disciplina": ...,
      "enunciado": ...,
      "resposta": ...,
      "dificuldade": ...
    }}
  ]
}}

Questão:
{questao}
"""

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "gemma",
                    "prompt": prompt,
                    "stream": False
                }
            )
            result = response.json()
            json_response_text = result["response"].strip().replace("```json", "").replace("```", "")

            try:
                parsed_json = json.loads(json_response_text)
                if parsed_json.get("questoes"):
                    resultados.extend(parsed_json["questoes"])
            except Exception:
                print("Falha ao processar questão:", idx)
                print(json_response_text)

        return {"questoes": resultados}

    except Exception as e:
        print(f"Ocorreu um erro durante a análise do PDF com IA: {e}")
        return None