from django.db import models

# Create your models here.
class PlanName(models.Model):
    type = models.CharField(max_length=30)
    def __str__(self):
        return self.type


class Number(models.Model):
    type = models.ForeignKey(PlanName, on_delete=models.CASCADE)
    num = models.CharField(max_length=30)
    def __str__(self):
        return self.num

# class Duration(models.Model):
#     CHOICES = [
#         ("6 Months", '6'),
#         ('1 Year', '12'),
#     ]
#     dur=models.CharField(max_length=10,choices=CHOICES)
    
# class Amount(models.Model):
#     type = models.ForeignKey(PlanName, on_delete=models.CASCADE)
#     num = models.ForeignKey(Number, on_delete=models.CASCADE)
#     dur=models.ForeignKey(Duration, on_delete=models.CASCADE)
#     amt=models.CharField(max_length=255)

# Amount._meta.get_field('dur').default = 1
    
class plan_info(models.Model):
    CHOICES = [
        (6 , '6 Months'),
        (12, '1 Year'),
    ]
    # duration=models.CharField(max_length=10,choices=CHOICES)
    plan_name = models.ForeignKey(PlanName,verbose_name="Plan Type", on_delete=models.SET_NULL, null=True)
    no_of_members = models.ForeignKey(Number,verbose_name="Number of Members", on_delete=models.SET_NULL, null=True)
    # duration = models.ForeignKey(Duration,verbose_name="Duration", on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(null=True)

# class subscription(models.Model):
