import tempfile
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Prova, Questao
from .utils import analisar_pdf_com_ia

def importar_prova(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        ano = request.POST.get("ano")
        vestibular = request.POST.get("vestibular")
        pdf_file = request.FILES.get("pdf_file")

        if not pdf_file:
            # Adicionar uma mensagem de erro aqui se desejar
            return render(request, "provas/importar.html")

        # Salva o PDF em um arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            for chunk in pdf_file.chunks():
                tmp.write(chunk)
            caminho_pdf = tmp.name

        # Cria a prova no banco
        prova = Prova.objects.create(nome=nome, ano=ano, vestibular=vestibular)

        # Analisa o PDF com IA para extrair as questões
        dados_questoes = analisar_pdf_com_ia(caminho_pdf)

        if dados_questoes and 'questoes' in dados_questoes:
            for item_questao in dados_questoes['questoes']:
                Questao.objects.create(
                    prova=prova,
                    numero=item_questao.get('numero'),
                    enunciado=item_questao.get('enunciado'),
                    disciplina=item_questao.get('disciplina'),
                    dificuldade=item_questao.get('dificuldade'),
                    resposta=item_questao.get('resposta')
                )
        
        # Redireciona para a página de resultados
        return redirect(reverse('resultado_importacao', args=[prova.id]))

    return render(request, "provas/importar.html")

def resultado_importacao(request, prova_id):
    prova = Prova.objects.get(pk=prova_id)
    return render(request, "provas/resultado_importacao.html", {"prova": prova})