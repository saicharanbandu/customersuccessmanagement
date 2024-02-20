from django import forms
from .models import plan_info

class pl_info(forms.ModelForm):
    class Meta:
        model = plan_info
        fields = ['plan_name', 'no_of_members','duration','amount']
