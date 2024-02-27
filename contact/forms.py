from django import forms
from . import models as contactModel

class ContactForm(forms.ModelForm):
    class Meta:
        model = contactModel.Contact
        fields = ['name', 'designation', 'organization', 'mobile_number','alt_number', 'email_id', 'address','profile_picture']
        
    
    def mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if  len(mobile_number) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
        return mobile_number
    def alt_number(self):
        alt_number = self.cleaned_data['alt_number']
        if  len(alt_number) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
        return alt_number