from django import forms
from .models import Orcamento, OrcamentoItem

class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = ['cliente', 'responsavel', 'descricao', 'data_orcamento']
        widgets = {
            'data_orcamento': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class OrcamentoItemForm(forms.ModelForm):
    class Meta:
        model = OrcamentoItem
        fields = ['servico', 'quantidade', 'valor_unitario']