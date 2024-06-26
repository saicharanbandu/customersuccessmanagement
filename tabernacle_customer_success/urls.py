"""
URL configuration for tabernacle_customer_success project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("contact/", include("contact.urls")),
    path("customer/", include("customer.urls")),
    path("misc/", include("misc.urls")),
    path("plan/", include("plan.urls")),
    path("prospect/", include("prospect.urls")),
    path('user/',include('user.urls')),
    path('revenue/',include('revenue.urls')),
    path('usage/',include('usage.urls')),

    path("__debug__/", include("debug_toolbar.urls")),
    # path('', RedirectView.as_view(pattern_name='customer:list')),
]


handler404 = 'tabernacle_customer_success.views.handler_404_view'
handler500 = 'tabernacle_customer_success.views.handler_500_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)