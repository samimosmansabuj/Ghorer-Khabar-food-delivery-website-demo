from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import BaseManager

# Create your models here.
class Custom_User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Normal User', 'Normal User'),
        ('Merchant', 'Merchant'),
    )
    
    username = models.CharField(max_length=100, validators=[UnicodeUsernameValidator], unique=True)
    email = models.EmailField(max_length=150)
    phone_number = models.CharField(max_length=14)
    user_type = models.CharField(choices=USER_TYPE, blank=True, null=True, max_length=20)
    
    joined_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    is_varified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=500, blank=True, null=True)
    otp_token = models.CharField(max_length=6, blank=True, null=True)
    
    objects = BaseManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']
    
    def __str__(self) -> str:
        return self.username

class Merchant_User(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE, related_name='company_user')
    name = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_logo = models.ImageField(upload_to='company/logo/', blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.company_name} | {self.user.username}'


class Normal_User(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE, related_name='regular_user')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='regular_user/picture/', blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.first_name} | {self.user.username}'


