from prospect import models as prospectModels, forms as prospectForms
from django.contrib import messages


def change_status(request):
    if request.method == 'POST':
        prospect_status_form = prospectForms.ProspectStatusForm()
        prospect_status_form.save()
        messages.success(request, 'Contact has been successfully deleted')
    else:
        messages.error(request,'Unsuccessful, try again')