from django import forms
from . import models as customerModels


class CustomerInfo(forms.ModelForm):
    class Meta:
        model = customerModels.CustomerInfo
        fields = ['legal_name', 'display_name','short_name','address','country','city','state','zip_code']
