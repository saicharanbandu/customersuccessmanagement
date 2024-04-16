from django import forms
from . import models as prospectModels
from misc import models as miscModels
from user import models as userModels
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
        self.fields['state'].queryset = miscModels.State.objects.none()

        if 'prospect-country' in self.data:
            country_id = self.data.get('prospect-country')

            try:
                self.fields['state'].queryset = miscModels.State.objects.filter(
                    country_id=country_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            if self.instance.state:
                self.fields['state'].queryset = (
                    self.instance.country.state_set.order_by('name')
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

    def __init__(self, *args, **kwargs):
        super(PointOfContactForm, self).__init__(*args, **kwargs)
        if 'prospect' in self.fields:
            self.fields['prospect'].required = False

    def is_empty(self):
        """
        Check if the form is empty (all fields are empty).
        """
        for field_name, field in self.fields.items():
            if field_name not in ['uuid', 'DELETE']:
                value = self.cleaned_data.get(field_name)
                if value is not None and value != '':
                    return False
        return True

class ProspectStatusForm(forms.ModelForm):
    class Meta:
        model = prospectModels.StatusHistory
        exclude = [
            'uuid',
            'created_at',
            'updated_at',
        ]
        widgets = {
            'prospect': forms.HiddenInput(),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time',
                }
            ),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(ProspectStatusForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = [('', '--Select--'),] + list(self.fields['status'].choices)[1:]


class ProspectRemarksForm(forms.ModelForm):
    class Meta:
        model = prospectModels.Profile
        fields = [
            'remarks',
        ]
        widgets = {
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class ProspectManagerForm(forms.ModelForm):
    class Meta:
        model = prospectModels.Profile
        fields = [
            'manager',
        ]
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProspectManagerForm, self).__init__(*args, **kwargs)
        self.fields['manager'].choices = self.get_manager_choices()

    def get_manager_choices(self):
        choices = userModels.User.objects.all().values_list('uuid', 'full_name')
        formatted_choices = [(user_id, f'{full_name}') for user_id, full_name in choices]
        return [('', '--Select--')] + formatted_choices