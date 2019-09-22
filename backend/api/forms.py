from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm): 
    class Meta:
        model=Payment
        fields =("transaction_id","receipt","user","amount","test_series")