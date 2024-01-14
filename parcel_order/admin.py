from django.contrib import admin
from .models import Delivery_Order

# Register your models here.
@admin.register(Delivery_Order)
class Delivery_Order_Admin(admin.ModelAdmin):
    list_display = ['tracking_ID', 'status', 'shipping_charge', 'recipient_name', 'delivery_system', 'user']
    list_filter = ['status', 'delivery_system', 'shipping_charge_paid', 'order_date']
    
