from django import forms
from . import models as userModels


class UserInfo(forms.ModelForm):
    class Meta:
        model = userModels.user_info
        fields = ['full_name', 'designation','dailing_code','mobile_no']