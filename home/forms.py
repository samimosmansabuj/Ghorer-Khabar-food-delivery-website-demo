from django import forms
from home.models import Address

class Delivery_Address_Form(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_01', 'upazila', 'district']
        widgets = {
            'address_01': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'upazila': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'district': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }

class PickUp_Address_Form(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_01', 'upazila', 'district']
        widgets = {
            'address_01': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'upazila': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'district': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }



