from django import forms
from . import models as contactModel


class ContactForm(forms.ModelForm):
    class Meta:
        model = contactModel.Contact
        fields = [
            "name",
            "designation",
            "organization",
            "mobile_number",
            "alt_number",
            "email_id",
            "address",
            "profile_picture",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "designation": forms.TextInput(attrs={"class": "form-control"}),
            "organization": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            'mobile_number':
            forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'alt_number':
            forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'email_id':
            forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'address':
           forms.TextInput(attrs={"class": "form-control"}),
             'profile_picture':
            forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['address'].initial = self.instance.address


    def mobile_number(self):
        mobile_number = self.cleaned_data["mobile_number"]
        if len(mobile_number) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
        return mobile_number

    def alt_number(self):
        alt_number = self.cleaned_data["alt_number"]
        if len(alt_number) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
        return alt_number

            
