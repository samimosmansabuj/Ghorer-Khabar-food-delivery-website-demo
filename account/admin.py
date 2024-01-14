from django.contrib import admin
from .models import Custom_User, Normal_User, Merchant_User

# Register your models here.
@admin.register(Custom_User)
class Custom_User_Admin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'is_varified']
    list_filter = ['joined_date', 'user_type', 'is_varified']

@admin.register(Merchant_User)
class Merchant_User_Admin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'user']

@admin.register(Normal_User)
class Normal_User_Admin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user']


