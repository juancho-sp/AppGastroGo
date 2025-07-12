from django import forms
from django.forms import formset_factory

class PlatoTextoForm(forms.Form):
    nombre_plato = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-uppercase plato-input',
            'list': 'lista-platos',
            'required': 'required',
            'autocomplete': 'off'
        })
    )
    cantidad = forms.IntegerField(
        min_value=1,
        required=True, 
        widget=forms.NumberInput(attrs={
            'class': 'form-control cantidad-input',
            'required': 'required'
        })
    )
    nota_plato = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 1,
            'class': 'form-control',
            'placeholder': 'Ej: sin cebolla'
        })
    )
