from django import forms
from . import models as customerModels
from misc import models as miscModels
from plan import models as planModels


class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = customerModels.CustomerInfo
        fields = ['legal_name', 'display_name', 'short_name','profile_picture', 'address', 'country', 'city', 'state', 'zip_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = miscModels.State.objects.none()
        
        if 'country' in self.data:
            country_id = self.data.get('country')
            try:
                self.fields['state'].queryset = miscModels.State.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass


class CustomerPlanForm(forms.ModelForm):
    class Meta:
        model = customerModels.CustomerPlan
        fields = ['customer', 'subscription_plan', 'duration_in_months']
    
    

class PlanOptionsForm(forms.Form):
    DURATION_CHOICES = [('6', '6 months'), ('12', '1 Year')]

    plan_type = forms.ModelChoiceField(queryset=planModels.PlanType.objects.all())
    member_size = forms.ModelChoiceField(queryset=planModels.MemberSize.objects.none())
    duration = forms.ChoiceField(choices=DURATION_CHOICES)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'plan_type' in self.data:
            plan_type_id = self.data.get('plan_type')
            try:
                member_size_uuids = planModels.SubscriptionPlan.objects.filter(plan_type_id=plan_type_id).values_list('member_size', flat=True)
                self.fields['member_size'].queryset = planModels.MemberSize.objects.filter(uuid__in=member_size_uuids)
            except (ValueError, TypeError):
                pass
