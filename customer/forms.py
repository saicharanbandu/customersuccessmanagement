from django import forms
from .models import Cus_info

class Customer_info(forms.ModelForm):
    class Meta:
        model = Cus_info
        fields = ['legal_name', 'display_name','short_name','address','country','city','state','zip_code']
