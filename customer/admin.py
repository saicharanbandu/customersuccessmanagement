from django.contrib import admin
from . import models as customerModels


admin.site.register(customerModels.CustomerInfo)
admin.site.register(customerModels.CustomerPlan)
