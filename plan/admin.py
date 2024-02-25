from django.contrib import admin
from . import models as planModels

admin.site.register(planModels.PlanType)
admin.site.register(planModels.MemberSize)
admin.site.register(planModels.SubscriptionPlan)