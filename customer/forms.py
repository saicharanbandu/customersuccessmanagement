from django import forms
from . import models as customerModels
from plan import models as planModels
from user import models as userModels

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
            'official_name': forms.TextInput(attrs={'class': 'form-control'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sms_name': forms.TextInput(
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
        queryset=planModels.Tariff.objects.all().order_by('lower_limit'),
        widget=forms.RadioSelect(attrs={'class': 'radio'}),
    )
    is_yearly = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'toggle'}),
    )
    discount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '0.00'}),
    )
    payment_mode = forms.ChoiceField(
        choices=constants.PAYMENT_MODE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}))
    
    payment_status = forms.ChoiceField(
        choices=constants.PAYMENT_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super(SubscriptionPlanOptionsForm, self).__init__(*args, **kwargs)
        self.fields['payment_mode'].initial = 'cash'
        self.fields['payment_status'].initial = 'paid'
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



class CustomerManagerForm(forms.ModelForm):
    class Meta:
        model = customerModels.Profile
        fields = [
            'manager',
        ]
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerManagerForm, self).__init__(*args, **kwargs)
        self.fields['manager'].choices = self.get_manager_choices()

    def get_manager_choices(self):
        choices = userModels.User.objects.all().values_list('uuid', 'full_name')
        formatted_choices = [(user_id, f'{full_name}') for user_id, full_name in choices]
        return [('', '--Select--')] + formatted_choices

class PaymentHistoryForm(forms.ModelForm):
    class Meta:
        model = customerModels.PaymentHistory
        fields = [
            'amount',
            'payment_date',
            'invoice_no',
            'receipt_no',
            'remarks',
        ]
        widgets = {
            'payment_date': forms.DateInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control'}),
            'receipt_no': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control','rows': 2}),
        }