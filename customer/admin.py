from django.contrib import admin
from .models import CustomerInfo,Country,State
# Register your models here.
admin.site.register(CustomerInfo)
admin.site.register(Country)
admin.site.register(State)
