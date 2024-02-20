from django.db import models

# Create your models here.
class plan_info(models.Model):
    plan_name = models.CharField(max_length=55,verbose_name='Plan Type')
    no_of_members = models.CharField(max_length=55,verbose_name='Number of Members')
    duration = models.CharField(max_length=50,verbose_name='Subscription Duration')
    amount = models.CharField(max_length=255,verbose_name='Amount to be Payed')

# class subscription(models.Model):
