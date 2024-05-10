from django.views import View
from django.shortcuts import render

class RevenueDashboardViewView(View):
    template_name = 'revenue/overview_view.html'
    title = 'Revenue Overview'
   
    def get(self, request, *args, **kwargs):
        
        context = {
            'title': self.title,
        }
        return render(request, self.template_name, context)