from django import forms
from .models import Prova

class ProvaForm(forms.ModelForm):
    pdf_file = forms.FileField(label='PDF da Prova')
    class Meta:
        model = Prova
        fields = ['nome', 'ano', 'vestibular']
