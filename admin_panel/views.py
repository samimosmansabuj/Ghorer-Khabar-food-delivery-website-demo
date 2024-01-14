from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from account.models import Custom_User
from parcel_order.models import Delivery_Order
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import check_password

# Create your views here.
def dashboard_Unauthorized(request):
    return render(request, 'admin_base/dashboard_unauthorized.html')

@login_required
def admin_dashboard(request):
    if request.user.user_type == 'Normal User' or request.user.user_type == 'Merchant':
        return redirect('dashboard_Unauthorized')
    
    order = Delivery_Order.objects.all().order_by('-id')
    user = Custom_User.objects.all()
    merchant_user = Custom_User.objects.filter(user_type='Merchant')
    context = {
        'order': order, 'user': user, 'merchant_user': merchant_user
    }
    return render(request, 'admin_base/dashboard/dashboard.html', context)


@login_required
def order_list(request):
    if request.user.user_type == 'Normal User' or request.user.user_type == 'Merchant':
        return redirect('dashboard_Unauthorized')
    
    filter = request.GET.get('filter')
    print('filter', filter)
    if filter == 'active':
        order = Delivery_Order.objects.filter(Q(status='Received') | Q(status='Shipped') | Q(status='On The Way') | Q(status='Receive at delivery point') | Q(status='Out For Delivery')).order_by('-id')
    elif filter == 'pending':
        order = Delivery_Order.objects.filter(status='Pending').order_by('-id')
    elif filter == 'delivered':
        order = Delivery_Order.objects.filter(status='Delivered').order_by('-id')
    else:
        order = Delivery_Order.objects.all().order_by('-id')
    return render(request, 'admin_base/order/order.html', {'order': order})

def notification_view(request, id):
    return None

@login_required
def order_view(request, id):
    if request.user.user_type == 'Normal User' or request.user.user_type == 'Merchant':
        return redirect('dashboard_Unauthorized')
    
    order = get_object_or_404(Delivery_Order, id=id)
    if request.method == 'POST':
        if request.POST['status'] == 'Received':
            if order.pay_for == 'Pickup':
                order.shipping_charge_paid = True
        elif request.POST['status'] == 'Delivered':
            order.shipping_charge_paid = True
        
        order.status = request.POST['status']
        order.status_details = request.POST['status_comment']
        order.order_update = request.POST['update_date_time']
        order.save()
        messages.success(request, 'Order Update Successfully!')
        return redirect(request.META['HTTP_REFERER'])
    return render(request, 'admin_base/order/order_view.html', {'order': order})

@login_required
def my_profile(request):
    if request.user.user_type == 'Normal User' or request.user.user_type == 'Merchant':
        return redirect('dashboard_Unauthorized')
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        
        user = get_object_or_404(Custom_User, username=username)
        user.email = email
        user.phone_number = phone_number
        current_password = request.user.password
        
        if old_password and new_password and confirm_new_password:
            old_password_check = check_password(old_password, current_password)
            if old_password_check:
                if new_password == confirm_new_password:
                    user.set_password(new_password)
                    user.save()
                    messages.warning(request, "Password Change Successfully!")
                    return redirect(request.META['HTTP_REFERER'])
                else:
                    messages.warning(request, "New password & confirm new password is doesn't match!")
                    return redirect(request.META['HTTP_REFERER'])
            else:
                messages.warning(request, 'Old Password is not currect!')
                return redirect(request.META['HTTP_REFERER'])
        else:
            messages.warning(request, "Profile Details Update Successfully!")
            return redirect(request.META['HTTP_REFERER'])
    
    return render(request, 'admin_base/profile/my_profile.html')
