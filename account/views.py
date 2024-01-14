from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import User_Create_Form, Login_Form
from .models import Normal_User, Merchant_User, Custom_User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def Logout(request):
    logout(request)
    return redirect('index')

def Login(request):
    if request.user.is_authenticated:
        return redirect('delivery_order_list')
    
    form = Login_Form()
    context = {'form': form}
    
    if request.method == 'POST':
        form = Login_Form(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            if not Custom_User.objects.filter(username=username).exists():
                messages.warning(request, 'Invalid Username')
                return redirect(request.META['HTTP_REFERER'])
            
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if user.user_type == 'Admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('my_account')
            else:
                messages.warning(request, 'Incorrect Password')
    
    return render(request, 'account/login.html', context)

def registration(request):
    if request.user.is_authenticated:
        return redirect('delivery_order_list')
    
    if request.method == 'POST':
        form = User_Create_Form(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = form.save()
            user.set_password(password)
            user.save()
            if user.user_type == 'Normal User':
                profile = Normal_User.objects.create(user=user)
            elif user.user_type == 'Merchant':
                merchat = Merchant_User.objects.create(user=user)
            return redirect('login')
        else:
            # message = form.errors
            return redirect(request.META['HTTP_REFERER'])
            # return HttpResponse(form.errors)
    else:
        form = User_Create_Form()
        context = {'form': form}
        return render(request, 'account/registration.html', context)


def reset_password(request):
    if request.method == 'POST':
        otp = random.randint(111111, 999999)
        email = request.POST['email']
        user = get_object_or_404(Custom_User, email=email)
        user.otp_token = otp
        user.save()
        subject = "OTP Verification For Reset Password!"
        message = f"""Dear User,
        Your Username: {user.username}
        Your Email: {user.email}
        Your OTP is : {otp}
        Thanks!
        """
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(subject, message, from_email, recipient_list)
        return render(request, 'account/reset_password.html', {'email': email})

def password_reset_confirm(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']
        new_password = request.POST['new_password']
        
        try:
            user = get_object_or_404(Custom_User, email=email)
            if user.otp_token == otp:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password Reset Successfully!')
                return redirect('login')
            else:
                messages.warning(request, 'OTP is incorrect')
                return redirect(request.META['HTTP_REFERER'])
        except:
            return HttpResponse("System Error")


@login_required
def my_account(request):
    if request.user.user_type == 'Admin' or request.user.user_type == 'Staff':
        return redirect('admin_dashboard')
    
    user = request.user
    context = {}
    if user.user_type == 'Merchant':
        merchant = get_object_or_404(Merchant_User, user=user)
        context['merchant'] = merchant
        
    elif user.user_type == 'Normal User':
        normal_user = get_object_or_404(Normal_User, user=user)
        context['normal_user'] = normal_user
    
    return render(request, 'account/my_account/my_account.html', context)

@login_required
def update_account(request):
    if request.user.user_type == 'Admin' or request.user.user_type == 'Staff':
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.phone_number = request.POST['phone_number']
        user.save()

        if user.user_type == 'Normal User':
            profile_picture = request.FILES.get('profile_picture')
            user_profile = get_object_or_404(Normal_User, user=request.user)
            
            user_profile.first_name = request.POST['first_name']
            user_profile.last_name = request.POST['last_name']
            if profile_picture:
                user_profile.profile_picture = profile_picture
            user_profile.save()
            
        elif user.user_type == 'Merchant':
            company_logo = request.FILES.get('company_logo')
            merchant = get_object_or_404(Merchant_User, user=request.user)
            
            merchant.name = request.POST['name']
            merchant.company_name = request.POST['company_name']
            if company_logo:
                merchant.company_logo = company_logo
            merchant.save()
            
        return redirect(request.META['HTTP_REFERER'])

