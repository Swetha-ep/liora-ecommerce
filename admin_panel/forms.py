from django import forms
from django.forms import ModelForm
from products.models import Product, Categories

class CategoryForm(ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewImage(event)'}),
        }