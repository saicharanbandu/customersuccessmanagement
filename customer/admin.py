from django.contrib import admin
from . import models as customerModels


admin.site.register(customerModels.UserAppPermissions)
admin.site.register(customerModels.Profile)
admin.site.register(customerModels.SubscribedPlan)
admin.site.register(customerModels.User)
admin.site.register(customerModels.PaymentHistory)