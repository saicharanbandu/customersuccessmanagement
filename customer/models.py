from django.db import models

from plan import models as planModels
from misc import models as miscModels

import uuid


class CustomerInfo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    legal_name = models.CharField(max_length=55,verbose_name='Legal Name')
    profile_picture = models.ImageField(upload_to='pictures',blank=True)
    display_name = models.CharField(max_length=55,verbose_name='Display Name')
    short_name = models.CharField(max_length=50,verbose_name='Short Name or Abbreviation')
    address = models.CharField(max_length=255,verbose_name='Address')
    city = models.CharField(max_length=50,verbose_name='City/Town/Village')
    country = models.ForeignKey(miscModels.Country, to_field='uuid', on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(miscModels.State, to_field='uuid', on_delete=models.SET_NULL, null=True)
    zip_code = models.IntegerField(verbose_name='Zip/Postal Code')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.legal_name
    


class CustomerPlan(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.ForeignKey(CustomerInfo, to_field='uuid', on_delete=models.SET_NULL, null=True,related_name='plans')
    subscription_plan = models.ForeignKey(planModels.SubscriptionPlan, to_field='uuid', on_delete=models.SET_NULL, null=True)
    duration_in_months = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.customer} - {self.plan}'
    

    