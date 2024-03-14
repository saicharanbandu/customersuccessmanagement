from django import forms
from . import models as prospectModels
from . import models as pointOfContactModels
from misc import models as miscModels


class ProspectInfoForm(forms.ModelForm):
    class Meta:
        model = prospectModels.ProspectInfo
        fields = [
            'name',
            'street',
            'country',
            'state',
            'city',
            'email',
            'website',
            'denomination',
            'congregation',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = miscModels.State.objects.none()

        if 'country' in self.data:
            country_name = self.data.get('country')
            try:
                country = miscModels.Country.objects.get(name=country_name)
                self.fields['state'].queryset = miscModels.State.objects.filter(
                    country=country
                ).order_by('name')
            except miscModels.Country.DoesNotExist:
                self.add_error('country', 'Invalid country name.')


class PointOfContactForm(forms.ModelForm):
    class Meta:
        model = pointOfContactModels.PointOfContactInfo
        fields = ['contact_name', 'mobile', 'email', 'remarks']

        widgets = {
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
