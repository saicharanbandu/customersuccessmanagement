from django.db import models

# Create your models here.
# class Country(models.Model):
#     name = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.name
#
# class State(models.Model):
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)
#
#     def __str__(self):
        # return self.name
class CustomerInfo(models.Model):
    legal_name = models.CharField(max_length=55,verbose_name='Legal Name')
    display_name = models.CharField(max_length=55,verbose_name='Display Name')
    short_name = models.CharField(max_length=50,verbose_name='Short Name or Abbreviation')
    address = models.CharField(max_length=255,verbose_name='Address')
    city = models.CharField(max_length=50,verbose_name='City/Town/Village')
    # country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    # state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=50,verbose_name='Country')
    state = models.CharField(max_length=50,verbose_name='State/Province')
    zip_code = models.CharField(max_length=10,verbose_name='Zip/Postal Code')
