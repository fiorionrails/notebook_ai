import requests
import tempfile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Prova, Questao
from .utils import extrair_questoes
from .forms import ProvaForm

def upload_prova(request):
    if request.method == 'POST':
        form = ProvaForm(request.POST, request.FILES)
        if form.is_valid():
            prova = form.save()
            pdf_file = request.FILES['pdf_file']
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                for chunk in pdf_file.chunks():
                    tmp.write(chunk)
                caminho = tmp.name

            questoes_data = extrair_questoes(caminho)
            for questao in questoes_data:
                enunciado_completo = questao['enunciado'] + "\n\n" + "\n".join(questao['alternativas'])
                Questao.objects.create(
                    prova=prova,
                    numero=questao['numero'],
                    enunciado=enunciado_completo
                )
            
            return redirect('revisar_questoes', prova_id=prova.id)
    else:
        form = ProvaForm()
    return render(request, 'provas/upload_prova.html', {'form': form})

def revisar_questoes(request, prova_id):
    prova = get_object_or_404(Prova, id=prova_id)
    questoes = prova.questoes.order_by('numero')
    return render(request, 'provas/revisar_questoes.html', {'prova': prova, 'questoes': questoes})

def atualizar_questao(request, questao_id):
    questao = get_object_or_404(Questao, id=questao_id)
    if request.method == 'POST':
        enunciado = request.POST.get('enunciado')
        disciplina = request.POST.get('disciplina')
        dificuldade = request.POST.get('dificuldade')
        resposta = request.POST.get('resposta')
        
        questao.enunciado = enunciado
        questao.disciplina = disciplina
        questao.dificuldade = dificuldade
        questao.resposta = resposta
        questao.save()
        return redirect('revisar_questoes', prova_id=questao.prova.id)
    
    return render(request, 'provas/atualizar_questao.html', {'questao': questao})

def marcar_prova_corrigida(request, prova_id):
    prova = get_object_or_404(Prova, id=prova_id)
    prova.corrigida = True
    prova.save()
    return redirect('revisar_questoes', prova_id=prova.id)

def importar_prova(request):
    if request.method == "POST":
        url = request.POST.get("pdf_url")

        # Baixa o PDF da internet
        response = requests.get(url)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            caminho = tmp.name

        # Cria a prova no banco
        prova = Prova.objects.create(nome="Prova Importada", ano=2024, vestibular="UEL")

        # Extrai e salva as questões com a nova função
        questoes_data = extrair_questoes(caminho)
        for questao in questoes_data:
            # Concatena enunciado e alternativas para salvar no campo 'enunciado'
            # O ideal seria ter um campo específico para as alternativas no seu modelo
            enunciado_completo = questao['enunciado'] + "\n\n" + "\n".join(questao['alternativas'])
            
            Questao.objects.create(
                prova=prova,
                numero=questao['numero'],
                enunciado=enunciado_completo
            )

    return render(request, "provas/importar.html")
