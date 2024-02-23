from django import forms
from . import models as customerModels

class CustomerInfo(forms.ModelForm):
    class Meta:
        model = customerModels.CustomerInfo
        fields = ['legal_name', 'display_name', 'short_name', 'address', 'country', 'city', 'state', 'zip_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = customerModels.State.objects.none()
        
        if 'country' in self.data:
            country_id = self.data.get('country')
            try:
                country_id = int(country_id)
                self.fields['state'].queryset = customerModels.State.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass