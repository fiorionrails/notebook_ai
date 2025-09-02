from django.urls import path
from . import views

urlpatterns = [
    path("importar/", views.importar_prova, name="importar_prova"),
]