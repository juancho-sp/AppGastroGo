from django import forms
from .models import Pedido, PedidoPlato
from menu.models import Plato

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['mesa']

class PedidoPlatoForm(forms.ModelForm):
    plato = forms.ModelChoiceField(
        queryset=Plato.objects.all(),
        empty_label="Selecciona un plato",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 1})
    )
    nota = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nota opcional'})
    )

    class Meta:
        model = PedidoPlato
        fields = ['plato', 'cantidad', 'nota']
