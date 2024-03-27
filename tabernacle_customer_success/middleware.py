from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith('/accounts') and not request.path.startswith('/admin'):
            return redirect(reverse('account_login'))
        
        response = self.get_response(request)
        return response