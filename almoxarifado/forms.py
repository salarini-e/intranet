from django import forms
from .models import Item, AlocaItem, RetiraItem

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'quantidade_total']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do Item',
            'quantidade_total': 'Quantidade Total',
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome',]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do Item',
        }


class AlocaItemForm(forms.ModelForm):
    class Meta:
        model = AlocaItem
        fields = ['quantidade', 'descricao']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'quantidade': 'Quantidade',
            'descricao': 'Descrição'
        }

class RetiraItemForm(forms.ModelForm):
    class Meta:
        model = RetiraItem
        fields = ['quantidade', 'descricao']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'quantidade': 'Quantidade',
            'descricao': 'Descrição'
        }