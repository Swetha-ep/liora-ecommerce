from django import forms
from django.forms import ModelForm
from products.models import Product, Categories, Color, Size, Inventory

class CategoryForm(ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewImage(event)'}),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
    

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'hex_code' : forms.TextInput(attrs={
                'type' : 'color',
                'class' : 'form-control form-control-color',
                'style': 'height: 50px; width: 100%; padding: 0; border: 1px solid #ccc;; cursor: pointer;',
                'title': 'Choose your color'
            }),
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter color name',
            })
        }
        labels = {
            'hex_code' : 'Choose Color'
        }

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = '__all__'


class StockForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        