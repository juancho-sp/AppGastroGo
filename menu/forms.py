from django import forms
from .models import Ingrediente

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'nombre-ingrediente',
                'autocomplete': 'off',
                'placeholder': 'Nombre del ingrediente'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'precio-ingrediente',
                'placeholder': 'Precio'
            }),
        }
