from django.db import models

# Create your models here.
class user_info(models.Model):
    CHOICES = [
        ("India", '+91'),
        ('USA', '+1'),
        ("UK", '+44'),
    ]
    full_name = models.CharField(max_length=55,verbose_name='Full Name')
    designation = models.CharField(max_length=55,verbose_name='Designation')
    dailing_code=models.CharField(max_length=10,choices=CHOICES)
    mobile_no = models.CharField(max_length=50,verbose_name='Mobile Number')
    