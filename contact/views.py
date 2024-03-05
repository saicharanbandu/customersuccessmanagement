from django.shortcuts import render,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from . import models as contactModel,forms as contactForm
def index(request):
    return render(request,'index.html')

class ContactCreateView(View):
    template_name = 'contact_form.html'
    title = 'Contact Directory'
    active_tab = 'contact'

    def get(self, request, *args, **kwargs):
        contact_info_form = contactForm.ContactForm(request.GET)
        
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_info_form': contact_info_form
        }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        contact_info_form = contactForm.ContactForm(request.POST, request.FILES)
        print('a')
        if contact_info_form.is_valid():
            print('b')
            if 'profile_picture' in request.FILES:
                contact_info_form.profile_picture = request.FILES['profile_picture']
            contact_info_form.save()
            return redirect(reverse('contact:list'))
        else:
            print(contact_info_form.errors)
            contact_info_form = contactForm.ContactForm(request.POST, request.FILES)
            context = {
                'title': self.title,
                'active_tab': self.active_tab,
                'contact_info_form': contact_info_form
            }
            return render(request, self.template_name, context)

class MyPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise
            
class ContactListView(ListView):
    model = contactModel.Contact
    template_name = 'list.html'
    context_object_name = 'contacts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        users = self.get_queryset()
        paginator = Paginator(users, self.paginate_by)
        users = paginator.page(page)
        for contact in users:
            print(contact.profile_picture)
        context['users'] = users
        return context