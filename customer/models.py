from django.db import models
from django.contrib.postgres.fields import ArrayField

from plan import models as planModels
from misc import models as miscModels

import uuid


class CustomerInfo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    legal_name = models.CharField(max_length=55, verbose_name="Legal Name")
    profile_picture = models.ImageField(upload_to="pictures", blank=True)
    display_name = models.CharField(max_length=55, verbose_name="Display Name")
    short_name = models.CharField(
        max_length=50, verbose_name="Short Name or Abbreviation"
    )
    address = models.CharField(max_length=255, verbose_name="Address")
    city = models.CharField(max_length=50, verbose_name="City/Town/Village")
    country = models.ForeignKey(
        miscModels.Country, to_field="uuid", on_delete=models.SET_NULL, null=True
    )
    state = models.ForeignKey(
        miscModels.State, to_field="uuid", on_delete=models.SET_NULL, null=True
    )
    zip_code = models.IntegerField(verbose_name="Zip/Postal Code")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.legal_name


class CustomerPlan(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.ForeignKey(
        CustomerInfo,
        to_field="uuid",
        on_delete=models.SET_NULL,
        null=True,
        related_name="customer_plans",
    )
    subscription_plan = models.ForeignKey(
        planModels.SubscriptionPlan,
        to_field="uuid",
        on_delete=models.SET_NULL,
        null=True,
    )
    duration_in_months = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer}"


class CustomerUser(models.Model):
    """
    Staff Model
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.ForeignKey(
        CustomerInfo,
        related_name="customer_user",
        to_field="uuid",
        on_delete=models.CASCADE,
    )
    full_name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name = "staff"
        verbose_name_plural = "staff"



class UserAppPermissions(models.Model):
    """
    Member Family Relation Model
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(
        CustomerUser,
        related_name="user_app_permissions_customer",
        to_field="uuid",
        on_delete=models.CASCADE,
    )
    module = models.CharField(max_length=25, null=True)
    access_role = models.CharField(max_length=25, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} | {self.module}"

    class Meta:
        unique_together = ["user", "module"]
        ordering = ('user__full_name', )

