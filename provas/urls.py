from django.urls import path
from . import views

urlpatterns = [
    path("", views.importar_prova, name="importar_prova"),
    path("resultado/<int:prova_id>/", views.resultado_importacao, name="resultado_importacao"),
]