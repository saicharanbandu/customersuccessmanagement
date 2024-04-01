import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    """
    Custom user manager
    """

    def create_user(self, full_name, mobile_no, email, password, **extra_fields):
        """
        Creates and saves a User with the given mobile_no, email and password.
        """
        if not full_name:
            raise ValueError('Users must have a full name')

        if not mobile_no:
            raise ValueError('Users must have a phone number')
        
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, mobile_no=mobile_no, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, mobile_no, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given mobile_no, email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(full_name, mobile_no, email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    """
        Custom user model
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    full_name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True),
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_no', 'full_name']

    objects = UserManager()

    def __str__(self):
        return self.full_name + '(' + self.email +')'

    class Meta:
        ordering = ['full_name']
