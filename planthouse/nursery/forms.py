from django.forms import ModelForm
from django import forms
from .models import Plant
# class addItemForm(mode)

class ProductForm(ModelForm):
    class Meta:
        model = Plant
        fields = ['plantName','plantPrice','plantImage','plantDesc','plantNursery']
        widgets = {
            'plantName': forms.TextInput(attrs={'placeholder': 'Enter Plant Name'}),
            'plantPrice': forms.NumberInput(attrs={'placeholder': 'Enter Plant Price'}),
            'plantDesc': forms.Textarea(
                attrs={'placeholder': 'Enter description here'}),
        }