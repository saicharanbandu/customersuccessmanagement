from django import forms
from . import models as customerModels
from misc import models as miscModels
from plan import models as planModels
from tabernacle_customer_success import constants

class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = customerModels.CustomerInfo
        fields = [
            'legal_name',
            'display_name',
            'short_name',
            'profile_picture',
            'address',
            'country',
            'state',
            'city',
            'zip_code',
        ]

        widgets = {
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
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'state': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'zip_code': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = miscModels.State.objects.none()

        if 'country' in self.data:
            country_id = self.data.get('country')
            try:
                self.fields['state'].queryset = miscModels.State.objects.filter(
                    country_id=country_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            if self.instance.state:
                self.fields['state'].queryset = self.instance.country.state_set.order_by ('name')

class CustomerPlanForm(forms.ModelForm):
    class Meta:
        model = customerModels.CustomerPlan
        fields = ['customer', 'subscription_plan', 'duration_in_months']


class PlanOptionsForm(forms.Form):
    DURATION_CHOICES = [('6', '6 months'), ('12', '1 Year')]

    plan_type = forms.ModelChoiceField(queryset=planModels.PlanType.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    member_size = forms.ModelChoiceField(queryset=planModels.MemberSize.objects.none(), widget=forms.Select(attrs={'class': 'form-select'}))
    duration = forms.ChoiceField(choices=DURATION_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'plan_type' in self.data:
            plan_type_id = self.data.get('plan_type')
            try:
                member_size_uuids = planModels.SubscriptionPlan.objects.filter(
                    plan_type_id=plan_type_id
                ).values_list('member_size', flat=True)
                self.fields['member_size'].queryset = (
                    planModels.MemberSize.objects.filter(uuid__in=member_size_uuids)
                )
            except (ValueError, TypeError):
                pass
class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = customerModels.CustomerUser
        fields = ['full_name', 'designation', 'mobile_no', 'email']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class AddUserAppPermissionsForm(forms.ModelForm):
    has_access = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input module-permission'}))
    access_role = forms.ChoiceField(required=False, choices=constants.STAFF_ACCESS_ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select',}))
    module_name = forms.CharField(widget=forms.TextInput(), required=False)

    class Meta:
        model = customerModels.UserAppPermissions
        fields = ['module', 'access_role']
        widgets = {
            'module': forms.HiddenInput(),
        }


class EditUserAppPermissionsForm(forms.ModelForm):
    has_access = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input module-permission'}))
    access_role = forms.ChoiceField(required=False, choices=constants.STAFF_ACCESS_ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select',}))
   
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