from django import forms
from . import models as userModels


class UserInfo(forms.ModelForm):
    class Meta:
        model = userModels.User
        exclude = [
            'uuid',
            'last_login',
            'updated_at',
            'date_joined',
        ]
        widgets = {
            
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password':forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'mobile_no': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'is_superuser' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),}
        
class UserProfile(forms.ModelForm):
    class Meta:
        model = userModels.Profile
        exclude = [
            'uuid','user',
        ]   
        widgets = {
            'user': forms.HiddenInput(),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'accept': 'image/*'}
            ),}