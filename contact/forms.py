from django import forms
from . import models as contactModel


class ContactForm(forms.ModelForm):
    class Meta:
        model = contactModel.Contact
        exclude = [
            'uuid',
            'created_at',
            'updated_at'
        ]
        widgets = {
            'created_by': forms.HiddenInput(),
            'updated_by': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(
                attrs={
                    'class': 'form-control',
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
            'email':
            forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'address':
           forms.Textarea(attrs={'class': 'form-control', 'rows':'4'}),
             'profile_picture':
            forms.ClearableFileInput(attrs={
                'class': 'form-control file-upload-info',
                'accept': 'image/*'
            }),
        }
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['address'].initial = self.instance.address


    def mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if len(mobile_number) != 10:
            raise forms.ValidationError('Please enter a valid 10-digit mobile number.')
        return mobile_number

    def alt_number(self):
        alt_number = self.cleaned_data['alt_number']
        if len(alt_number) != 10:
            raise forms.ValidationError('Please enter a valid 10-digit mobile number.')
        return alt_number

            
