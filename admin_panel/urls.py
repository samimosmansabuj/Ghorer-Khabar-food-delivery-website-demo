from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/order/', order_list, name='order_list'),
    path('dashboard/order/<int:id>/', order_view, name='order_view'),
    path('dashboard/notification/<int:id>/', notification_view, name='notification_view'),
    path('dashboard/my-profile/', my_profile, name='my_profile'),
    
    path('dashboard/unauthorized/', dashboard_Unauthorized, name='dashboard_Unauthorized')
    
]