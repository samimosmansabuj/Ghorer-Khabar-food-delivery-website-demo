from django.db import models
from account.models import Custom_User

# Create your models here.
class Address(models.Model):
    ADDRESS_TYPE = (
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Others', 'Others'),
    )
    
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_address')
    
    address_type = models.CharField(choices=ADDRESS_TYPE, blank=True, null=True, max_length=50)
    address_01 = models.TextField()
    address_02 = models.TextField(blank=True, null=True)
    upazila = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True, default='Bangladesh')
    
    def __str__(self) -> str:
        return f'{self.user} | {self.address_type} | {self.address_01} {self.upazila} {self.district} {self.country}'
    
