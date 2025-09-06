from django.urls import path
from . import views

urlpatterns = [
    path("importar/", views.importar_prova, name="importar_prova"),
    path('upload/', views.upload_prova, name='upload_prova'),
    path('revisar/<int:prova_id>/', views.revisar_questoes, name='revisar_questoes'),
    path('atualizar_questao/<int:questao_id>/', views.atualizar_questao, name='atualizar_questao'),
    path('marcar_corrigida/<int:prova_id>/', views.marcar_prova_corrigida, name='marcar_prova_corrigida'),
]
