from django import forms
from . import models as planModels

class pl_info(forms.ModelForm):
    class Meta:
        model = planModels.plan_info
        fields = ['plan_name', 'no_of_members','amount']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['no_of_members'].queryset = planModels.Number.objects.none()
        # self.fields['amount'].queryset = planModels.Amount.objects.none()
        if 'plan_name' in self.data:
            plan_name_id = self.data.get('plan_name')
            no_of_members_id = self.data.get('no_of_members')
            # duration_id = self.data.get('duration')
            try:
                plan_name_id = int(plan_name_id)
                no_of_members_id = int(no_of_members_id)
                duration_id = int(duration_id)
                self.fields['no_of_members'].queryset = planModels.Number.objects.filter(type_id=plan_name_id).order_by('name')
                # self.fields['amount'].queryset = planModels.Amount.objects.filter(type_id=plan_name_id,num_id=no_of_members_id,dur_id=duration_id)
            
            except (ValueError, TypeError):
                pass