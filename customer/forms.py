from django import forms
from . import models as customerModels
from plan import models as planModels

from tabernacle_customer_success import constants


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = customerModels.Profile
        exclude = [
            'uuid',
            'created_at',
            'updated_at',
        ]

        widgets = {
            'prospect': forms.HiddenInput(),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'profile_picture': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'accept': 'image/*'}
            ),
        }


class CustomerPlanForm(forms.ModelForm):
    class Meta:
        model = customerModels.SubscribedPlan
        exclude = ['uuid', 'created_at', 'updated_at']


class SubscriptionPlanOptionsForm(forms.Form):
    plan = forms.ModelChoiceField(
        queryset=planModels.Tariff.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio'}),
    )
    duration = forms.ChoiceField(
        choices=constants.PLAN_DURATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    payment_status = forms.ChoiceField(
        choices=constants.PAYMENT_STATUS_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = customerModels.User
        exclude = ['uuid', 'created_at', 'updated_at']

        widgets = {
            'customer': forms.HiddenInput(),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class AddUserAppPermissionsForm(forms.ModelForm):
    has_access = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input module-permission'}
        )
    )
    access_role = forms.ChoiceField(
        required=False,
        choices=constants.STAFF_ACCESS_ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
    )
    module_name = forms.CharField(widget=forms.TextInput(), required=False)

    class Meta:
        model = customerModels.UserAppPermissions
        fields = ['module', 'access_role']
        widgets = {
            'module': forms.HiddenInput(),
        }


class EditUserAppPermissionsForm(forms.ModelForm):
    has_access = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input module-permission'}
        )
    )
    access_role = forms.ChoiceField(
        required=False,
        choices=constants.STAFF_ACCESS_ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
    )

    class Meta:
        model = customerModels.UserAppPermissions
        fields = ['user', 'module', 'access_role']
        widgets = {
            'user': forms.HiddenInput(),
            'module': forms.HiddenInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super(UserAppPermissionsForm, self).__init__(*args, **kwargs)
    #     self.fields['access_role'].initial = 'editor'

    # class Meta:
    #     model = customerModels.UserAppPermissions
    #     fields = ['module', 'access_role']
