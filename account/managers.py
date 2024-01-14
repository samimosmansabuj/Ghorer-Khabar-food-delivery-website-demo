from django.contrib.auth.base_user import BaseUserManager

class BaseManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password, **extra_fields):
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, phone_number, password, **extra_fields):
        user = self.create_user(username=username, email=email, phone_number=phone_number, password=password, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.is_varified = True
        user.save()
        return user