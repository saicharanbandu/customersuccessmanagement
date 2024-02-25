from django.db import models
import uuid


class PlanType(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MemberSize(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    upper_limit = models.IntegerField()
    lower_limit = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.lower_limit} - {self.upper_limit}'

    
class SubscriptionPlan(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    plan_type = models.ForeignKey(PlanType, related_name='subscription_plan_type', to_field='uuid', on_delete=models.SET_NULL, null=True)
    member_size = models.ForeignKey(MemberSize, related_name="subscription_plan_member_size", to_field='uuid', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.plan_type.name} [{self.member_size}]'