from django import forms
from . import models as prospectModels
from . import models as pointOfContactModels
from misc import models as miscModels


class ProspectInfoForm(forms.ModelForm):
    class Meta:
        model = prospectModels.ProspectInfo
        fields = ['prospect_name', 'street_loc', 'city', 'country', 'state', 'email', 'website', 'denomination',
                  'congregation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = miscModels.State.objects.none()

        if 'country' in self.data:
            country_name = self.data.get('country')
            try:
                country = miscModels.Country.objects.get(name=country_name)
                self.fields['state'].queryset = miscModels.State.objects.filter(country=country).order_by('name')
            except miscModels.Country.DoesNotExist:
                self.add_error('country', 'Invalid country name.')


class PointOfContactForm(forms.ModelForm):
    class Meta:
        model = pointOfContactModels.PointOfContactInfo
        fields=['pOC_name','mobile','email','remarks']