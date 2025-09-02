import requests, tempfile
from django.shortcuts import render
from .models import Prova, Questao
from .utils import extrair_questoes

def importar_prova(request):
    if request.method == "POST":
        url = request.POST.get("pdf_url")

        # Baixa o PDF da internet
        response = requests.get(url)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            caminho = tmp.name

        # Cria a prova no banco
        prova = Prova.objects.create(nome="Prova Importada", ano=2025, vestibular="desconhecido")

        # Extrai e salva as questões
        questoes_pdf = extrair_questoes(caminho)
        for i, enunciado in enumerate(questoes_pdf, start=1):
            Questao.objects.create(prova=prova, numero=i, enunciado=enunciado)

    return render(request, "provas/importar.html")