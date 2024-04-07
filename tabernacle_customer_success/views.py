from django.shortcuts import render


def handler_404_view(request, exception):
    return render(request, 'handler/404.html', status=404)


def handler_500_view(request):
    return render(request, 'handler/500.html', status=500)