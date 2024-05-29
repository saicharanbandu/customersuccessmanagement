from django.shortcuts import render
from django.views import View

class UsageDashboardView(View):
    template_name = 'usage/overview_view.html'
    title = 'Usage Overview'
   
    def get(self, request, *args, **kwargs):
        
        context = {
            'title': self.title,
        }
        return render(request, self.template_name, context)
