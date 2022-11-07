from django import forms
from dashboard.models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'location', 'mobile', 'email']

