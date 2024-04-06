from django.db import models
from django.conf import settings

from plan import models as planModels
from prospect import models as prospectModels

from tabernacle_customer_success import constants
import uuid


class Profile(models.Model):
    """
    Customer Profile
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    prospect = models.OneToOneField(
        prospectModels.Profile, to_field="uuid", on_delete=models.SET_NULL, null=True
    )
    profile_picture = models.ImageField(upload_to="pictures", blank=True)
    legal_name = models.CharField(max_length=255, verbose_name="Legal Name")
    display_name = models.CharField(max_length=255, verbose_name="Display Name")
    short_name = models.CharField(
        max_length=30, verbose_name="Short Name or Abbreviation"
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='customer_manager'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.legal_name


class SubscribedPlan(models.Model):
    """
    Plan the customer is subscribed to
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.OneToOneField(
        Profile,
        to_field="uuid",
        on_delete=models.CASCADE,
        null=True,
        related_name="customer_plan",
    )
    subscription_plan = models.ForeignKey(
        planModels.Tariff,
        to_field="uuid",
        on_delete=models.CASCADE,
        null=True,
    )
    duration = models.IntegerField(default=0) # Duration in months
    payment_status = models.CharField(max_length=55, choices=constants.PAYMENT_STATUS_CHOICES, verbose_name="Payment Status", default=constants.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer}"

    class Meta:
        ordering = ('customer__legal_name',)


class User(models.Model):
    """
    User created for a customer
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.ForeignKey(
        Profile,
        related_name="customer_user",
        to_field="uuid",
        on_delete=models.CASCADE,
    )
    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}"



class UserAppPermissions(models.Model):
    """
    User App Permissions
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(
        User,
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



class PaymentHistory(models.Model):
    """
    Customer's Payment History
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.ForeignKey(
        Profile,
        related_name="customer_payment",
        to_field="uuid",
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    payment_date = models.DateField()
    due_date = models.DateField()
    invoice_no = models.CharField(max_length=25, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.legal_name} | {self.payment_date}"

