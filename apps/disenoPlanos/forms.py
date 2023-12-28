from django import forms
from .models import Planos

class PlanosForm(forms.ModelForm):
    class Meta:
        model = Planos
        fields = ['imagen']
        labels = {'imagen': ''}
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'hidden', 'id': 'imagenInput'}),
        }
