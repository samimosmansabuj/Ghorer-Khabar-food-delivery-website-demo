from django import forms
from .models import Delivery_Order

class Delivery_Order_Form(forms.ModelForm):
    class Meta:
        model = Delivery_Order
        fields = ['item_price', 'item_description', 'recipient_name', 'recipient_phone_number', 'special_instructions', 'item_name']
        widgets = {
            'item_price': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'item_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'item_description': forms.Textarea(
                attrs={'class': 'form-control'}
            ),
            'recipient_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'recipient_phone_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'special_instructions': forms.Textarea(
                attrs={'class': 'form-control'}
            ),
        }
