from django import forms
from . import models as prospectModels
from misc import models as miscModels


class ProspectProfileForm(forms.ModelForm):
    class Meta:
        model = prospectModels.Profile
        exclude = [
            'uuid',
            'created_at',
            'updated_at',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'website': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'denomination': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'congregation': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'country': forms.Select(attrs={'class': 'form-select'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class PointOfContactForm(forms.ModelForm):
    class Meta:
        model = prospectModels.PointOfContact
        exclude = [
            'uuid',
            'prospect',
            'created_at',
            'updated_at',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
