from django.db import models
from home.models import Address
from account.models import Custom_User

# Create your models here.
class Delivery_Order(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE, related_name='user', blank=True, null=True)
    STATUS = (
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Shipped', 'Shipped'),
        ('On The Way', 'On The Way'),
        ('Receive at delivery point', 'Receive at delivery point'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered'),
        ('Return', 'Return'),
        ('Cancel', 'Cancel'),
    )
    DELIVERY_SYSTEM = (
        ('Train', 'Train'),
        ('Bus', 'Bus'),
    )
    PAY_FOR = (
        ('Pickup', 'Pickup'),
        ('Recipent', 'Recipent'),
    )
    PAYMENT_METHOD = (
        ('Cash', 'Cash'),
        ('Online', 'Online'),
    )
    tracking_ID = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(choices=STATUS, max_length=50, blank=True, null=True)
    status_details = models.CharField(max_length=600, blank=True, null=True)
    delivery_system = models.CharField(choices=DELIVERY_SYSTEM, max_length=50, blank=True, null=True)
    
    shipping_charge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    shipping_charge_paid = models.BooleanField(default=False)
    shopping_payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=50, blank=True, null=True)
    pay_for = models.CharField(choices=PAY_FOR, max_length=50, blank=True, null=True)
    
    delivery_secret_code = models.CharField(max_length=6, blank=True, null=True)
    
    pickup_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='pickup_address', blank=True, null=True)
    item_name = models.CharField(max_length=500, blank=True, null=True)
    item_price = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2)
    item_description = models.TextField(blank=True, null=True)
    
    recipient_name = models.CharField(max_length=100)
    recipient_phone_number = models.CharField(max_length=14)
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='delivery_address', blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    
    
    order_date = models.DateTimeField(auto_now_add=True)
    order_update = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField(blank=True,null=True)
    return_date = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return f'{self.user} | {self.tracking_ID}'



