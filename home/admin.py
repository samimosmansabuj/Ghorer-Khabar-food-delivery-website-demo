from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Address)
class Address_Admin(admin.ModelAdmin):
    list_display = ['user', 'address_type', 'address_01', 'upazila', 'district']
