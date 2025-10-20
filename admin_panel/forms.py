from django import forms
from django.forms import ModelForm
from products.models import Product, Categories, Color, Size, Inventory, Offer
from .models import Banner
from orders.models import Coupon

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
        

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        exclude = ['users_used']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter coupon code'}),
            'discount_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter coupon amount'}),
            'min_order_amount' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter minimum order amount'}),
            'valid_from': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'  
            }),
            'valid_to': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'active': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter caption'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewImage(event)'}),
        }



class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ['min_order_value']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewImage(event)'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.discount_type == 'percent':
            self.fields['discount_value'].label = "Discount Percentage (%)"
        else:
            self.fields['discount_value'].label = "Discount Amount (₹)"

    def clean(self):
        cleaned_data = super().clean()
        discount_type = cleaned_data.get('discount_type')
        discount_value = cleaned_data.get('discount_value')

        if discount_type == 'percent' and discount_value > 100:
            self.add_error('discount_value', 'Percentage discount cannot exceed 100%.')
        elif discount_value <= 0:
            self.add_error('discount_value', 'Discount value must be greater than 0.')
        return cleaned_data