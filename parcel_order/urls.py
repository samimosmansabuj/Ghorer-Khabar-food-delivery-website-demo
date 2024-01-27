from django.urls import path
from .views import *

urlpatterns = [
    path('place-new-order/', place_new_order, name='place_new_order'),
    path('order-confirm/', order_confirm, name='order_confirm'),
    path('order-payment/<int:id>/', unpaid_order_payment, name='unpaid_order_payment'),
    
    path('order-list/', delivery_order_list, name='delivery_order_list'),
    path('tracking-order/', tracking_order, name='tracking_order'),
    path('order-view/<int:id>/', view_order, name='view_order'),
    
    path('order-invoice/<int:id>/', order_invoice, name='order_invoice'),
    path('order-invoice-print/<int:id>/', order_invoice_print, name='order_invoice_print'),
    
    path('order-confirmation/<int:id>/', order_confirmation, name='order_confirmation'),
    
    path('order/payment-fail/', payment_fail, name='payment_fail'),
    path('order/payment-cancel/', payment_cancel, name='payment_cancel'),
    path('order/payment-success/', online_payment_processing, name='online_payment_processing'),
    path('order/payment-success/<int:id>/', payment_success_complete, name='payment_success_complete'),
]