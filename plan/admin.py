from django.contrib import admin
from .models import plan_info,PlanName,Number
# Register your models here.
admin.site.register(plan_info)
admin.site.register(PlanName)
# admin.site.register(Duration)
# admin.site.register(Amount)
admin.site.register(Number)