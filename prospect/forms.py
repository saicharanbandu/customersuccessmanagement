from django import forms
from . import models as prospectModels
from misc import models as miscModels

from tabernacle_customer_success import constants

class ProspectProfileForm(forms.ModelForm):
    class Meta:
        model = prospectModels.Profile
        exclude = [
            'uuid',
            'created_at',
            'updated_at',
            'status',
        ]

        widgets = {
            'manager': forms.HiddenInput(),
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
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'country': forms.Select(attrs={'class': 'form-select'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


    def __init__(self, *args, **kwargs):
        super(ProspectProfileForm, self).__init__(*args, **kwargs)
        self.fields["state"].queryset = miscModels.State.objects.none()

        if "prospect-country" in self.data:
            country_id = self.data.get("prospect-country")

            try:
                self.fields["state"].queryset = miscModels.State.objects.filter(
                    country_id=country_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            if self.instance.state:
                self.fields["state"].queryset = (
                    self.instance.country.state_set.order_by("name")
                )

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

PointOfContactFormSet = forms.formset_factory(PointOfContactForm, extra=1)

class ProspectStatusForm(forms.ModelForm):
   class Meta:
        model = prospectModels.StatusHistory
        exclude = [
            'uuid',
            'created_at',
            'updated_at',
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

