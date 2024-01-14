from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('registration/', registration, name='registration'),
    path('reset-password/', reset_password, name='reset_password'),
    path('reset-password-confirm/', password_reset_confirm, name='password_reset_confirm'),
    
    path('my-account/', my_account, name='my_account'),
    path('update-account/', update_account, name='update_account'),
]