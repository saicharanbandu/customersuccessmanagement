import os
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import models as contactModel

@login_required
def delete_contact(request, contact_id):
    if request.method == 'POST':
        contact = contactModel.Contact.objects.get(uuid=contact_id)
        try:
            if contact.profile_picture:
                os.remove(contact.profile_picture.path)
        except OSError:
            pass
        contact.delete()
        messages.success(request, 'Contact has been successfully deleted')
        return redirect(reverse('contact:list'))
    else:
        messages.error(request,'Unsuccessful, try again')