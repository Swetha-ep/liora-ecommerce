from .models import Address
from django import forms

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'address_line1': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address Line 1'}),
            'address_line2': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address Line 2 (Optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        }
