from django import forms
from .models import Payment, QuestionImage

class PaymentForm(forms.ModelForm): 
    class Meta:
        model=Payment
        fields =("transaction_id","receipt","user","amount","test_series")

class QuestionImageUploadForm(forms.ModelForm): 
    class Meta:
        model = QuestionImage
        fields = ("file",)