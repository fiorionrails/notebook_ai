from django.db import models

class Prova(models.Model):
    nome = models.CharField(max_length=200)
    ano = models.IntegerField()
    vestibular = models.CharField(max_length=100)
    corrigida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.ano}"


class Questao(models.Model):
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE, related_name="questoes")
    numero = models.IntegerField()
    enunciado = models.TextField()
    disciplina = models.CharField(max_length=100, null=True, blank=True)
    dificuldade = models.CharField(max_length=50, null=True, blank=True)
    resposta = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Questão {self.numero} - {self.prova}"
