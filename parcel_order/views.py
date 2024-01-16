from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from home.forms import *
from .forms import Delivery_Order_Form
from django.contrib.auth.decorators import login_required
from .models import Delivery_Order
import random
from account.models import Custom_User
from notifications.signals import notify
from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

@login_required
def delivery_order_list(request):
    if request.user.user_type == 'Admin' or request.user.user_type == 'Staff':
        return redirect('admin_dashboard')
    
    delivery_order = Delivery_Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'delivery_order': delivery_order
    }
    return render(request, 'parcel_order/order_list.html', context)


def tracking_order(request):
    tracking_id = request.GET.get('tracking_id')
    if tracking_id:
        if Delivery_Order.objects.filter(tracking_ID=tracking_id).exists():
            order = get_object_or_404(Delivery_Order, tracking_ID=tracking_id)
            return render(request, 'parcel_order/view_order.html', {'order': order})
        else:
            return render(request, 'home/not_found.html', {'tracking_id': tracking_id})
    else:
        return redirect('index')
    

@login_required
def place_new_order(request):
    if request.user.user_type == 'Admin' or request.user.user_type == 'Staff':
        return redirect('admin_dashboard')
    
    address_list = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        previous_pickup_address = request.POST['previous_pickup_address']
        previous_delivery_address = request.POST['previous_delivery_address']
        
        
        if previous_pickup_address != 'Add New Address':
            pickup_address = get_object_or_404(Address, id=previous_pickup_address)
            print('pickup address', pickup_address)
        else:
            p_address = request.POST['pickup_address_01']
            p_upazila = request.POST['pickup_upazila']
            p_district = request.POST['pickup_district']
            delivery_address_type = request.POST['delivery_address_type']
            if Address.objects.filter(user=request.user, address_01=p_address, upazila=p_upazila, district=p_district).exists():
                pickup_add = Address.objects.filter(
                    address_01=p_address,
                    upazila=p_upazila,
                    district=p_district
                )
                pickup_address = pickup_add[0]
            else:
                pickup_address = Address.objects.create(
                    user=request.user,
                    address_01 = p_address,
                    upazila = p_upazila,
                    district = p_district,
                    address_type=delivery_address_type,
                )
        
        if previous_delivery_address != 'Add New Address':
            delivery_address = get_object_or_404(Address, id=previous_delivery_address)
            print('delivery address', delivery_address)
        else:
            d_address = request.POST['delivery_address_01']
            d_upazila = request.POST['delivery_upazila']
            d_district = request.POST['delivery_district']
            delivery_address_type = request.POST['delivery_address_type']
            if Address.objects.filter(user=request.user, address_01=d_address, upazila=d_upazila, district=d_district).exists():
                delivery_add = Address.objects.filter(
                    address_01=d_address,
                    upazila=d_upazila,
                    district=d_district
                )
                delivery_address = delivery_add[0]
            else:
                delivery_address = Address.objects.create(
                    user=request.user,
                    address_01 = d_address,
                    upazila = d_upazila,
                    district = d_district,
                    address_type=delivery_address_type,
                )
        
        
        if delivery_address.district == pickup_address.district:
            shipping_charge = 80
        else:
            shipping_charge = 200
        
        delivery_order_form = Delivery_Order_Form()
        context = {
            'pickup_address': pickup_address,
            'delivery_address': delivery_address,
            'shipping_charge': shipping_charge,
            'delivery_order_form': delivery_order_form,
        }
        return render(request, 'parcel_order/order_confirm.html', context)
    else:
        return render(request, 'parcel_order/new_order.html', {'address_list': address_list})



@login_required
def order_confirm(request):
    if request.user.user_type == 'Admin' or request.user.user_type == 'Staff':
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        pickup_address_id = request.POST['pickup_address_id']
        pickup = get_object_or_404(Address, id=pickup_address_id)
        
        delivery_address_id = request.POST['delivery_address_id']
        delivery = get_object_or_404(Address, id=delivery_address_id)
        
        pay_for = request.POST['pay_for']
        delivery_system = request.POST['delivery_system']
        shipping_charge = request.POST['shipping_charge']
        payment_method = request.POST['payment_method']
        
        delivery_order_form = Delivery_Order_Form(request.POST)
        if delivery_order_form.is_valid():
            place_order = delivery_order_form.save()
            place_order.tracking_ID = random.randint(1111111111, 9999999999)
            place_order.status = 'Pending'
            place_order.delivery_system = delivery_system
            place_order.delivery_secret_code = random.randint(111111, 999999)
            place_order.pay_for = pay_for
            place_order.shopping_payment_method = payment_method
            
            place_order.shipping_charge = shipping_charge
            place_order.pickup_address = pickup
            place_order.delivery_address = delivery
            place_order.user = request.user
            place_order.save()
            qr_bar_code_genarate(place_order.tracking_ID)
            
            user = request.user
            recipient=Custom_User.objects.filter(Q(user_type='Admin') | Q(user_type='Staff'))
            verb = 'Place New Order!'
            notify.send(user, recipient=recipient, verb=verb, action_object=place_order)
            
            if payment_method == 'Online':
                return online_payment(place_order.id)
            
            return redirect('order_confirmation', id=place_order.id)
        else:
            return HttpResponse(delivery_order_form.errors)

import qrcode
from io import BytesIO
from django.core.files import File
import barcode
from barcode.writer import ImageWriter

def qr_bar_code_genarate(tracking_ID):
    order = get_object_or_404(Delivery_Order, tracking_ID=tracking_ID)
    qr_code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_code.add_data(f'http://127.0.0.1:8000/tracking-order/?tracking_id={tracking_ID}')
    qr_code.make(fit=True)
    
    qr_image = qr_code.make_image(fill_color="black", back_color="white")
    qr_image_stream = BytesIO()
    qr_image.save(qr_image_stream)
    qr_image_stream.seek(0)
    order.qr_code.save(f'qr_tracking_id_{tracking_ID}.png', File(qr_image_stream), save=True)
    
    bar_code = barcode.get('code128', f'{tracking_ID}', writer=ImageWriter())
    bar_code_image = bar_code.render()
    bar_code_stream = BytesIO()
    bar_code_image.save(bar_code_stream, format='PNG')
    bar_code_stream.seek(0)
    order.bar_code.save(f'bar_tracking_id_{tracking_ID}.png', File(bar_code_stream), save=True)


def unpaid_order_payment(request, id):
    if request.user.user_type == 'Admin' or request.user.user_type == 'Staff':
        return redirect('admin_dashboard')
    order = get_object_or_404(Delivery_Order, id=id)
    return online_payment(order.id)

# ====================Online Payment Credential Start======================
def online_payment(id):
    order = get_object_or_404(Delivery_Order, id=id)
    
    sslcommez = SSLCOMMERZ({ 'store_id': 'ecomm654bdaf1131e9', 'store_pass': 'ecomm654bdaf1131e9@ssl', 'issandbox': True })
    post_body = {
        'total_amount': order.shipping_charge,
        'currency': "BDT",
        'tran_id': order.id,
        
        'success_url' : "http://127.0.0.1:8000/order/payment-success/",
        'fail_url' : "http://127.0.0.1:8000/order/payment-fail/",
        'cancel_url' : "http://127.0.0.1:8000/order/payment-cancel/",
        
        'emi_option' : 0,
        'cus_name' : order.recipient_name,
        'cus_email' : order.user.email,
        'cus_phone' : str(order.recipient_phone_number),
        'cus_add1' : order.delivery_address.upazila,
        'cus_city' : order.delivery_address.district,
        'cus_country' : order.delivery_address.country,
        'shipping_method' : "NO",
        'multi_card_name' : "",
        'num_of_item' : 1,
        'product_name' : order.item_name,
        'product_category' : "Test Category",
        'product_profile' : "general",
        }
    post_body['value_a'] = order.id
    post_body['value_a'] = ""
    post_body['value_b'] = ""
    post_body['value_c'] = ""
    post_body['value_d'] = ""
    response = sslcommez.createSession(post_body)
    return redirect(response['GatewayPageURL'])

@csrf_exempt
def online_payment_processing(request):
    data = request.POST
    tran_id = data['tran_id']
    return redirect('payment_success_complete', id=tran_id)

def payment_success_complete(request, id):
    order = get_object_or_404(Delivery_Order, id=id)
    order.shipping_charge_paid = True
    order.save()
    return redirect('order_confirmation', id=order.id)

@csrf_exempt
def payment_fail(request):
    return HttpResponse("Payment Fail")

@csrf_exempt
def payment_cancel(request):
    return HttpResponse("Payment Cancel")
# ====================Online Payment Credential End======================




def order_confirmation(request, id):
    if request.user.user_type == 'Admin' or request.user.user_type == 'Staff':
        return redirect('admin_dashboard')
    
    place_order = get_object_or_404(Delivery_Order, id=id)
    return render(request, 'parcel_order/order_confirmation.html', {'place_order': place_order})

def view_order(request, id):
    if request.user.user_type == 'Admin' or request.user.user_type == 'Staff':
        return redirect('admin_dashboard')
    
    order = get_object_or_404(Delivery_Order, id=id)
    return render(request, 'parcel_order/view_order.html', {'order': order})



# Create your views here.
# def place_new_order(request):
#     if request.method == 'POST':
#         pickup_forms = PickUp_Address_Form(request.POST)
#         print(pickup_forms)
#         if pickup_forms.is_valid():
#             pickup_address = pickup_forms.save()
#             pickup_address.user = request.user
#             pickup_address.address_type = 'PickUp Address'
#             pickup_address.save()
#         else:
#             return HttpResponse(pickup_forms.errors)
        
#         delivery_forms = Delivery_Address_Form(request.POST)
#         print(delivery_forms)
#         if delivery_forms.is_valid():
#             delivery_address = delivery_forms.save()
#             delivery_address.user = request.user
#             delivery_address.address_type = 'Delivery Address'
#             delivery_address.save()
#         else:
#             return HttpResponse(delivery_forms.errors)
        
#         delivery_address_district = delivery_address.district
#         pickup_address_district = pickup_address.district
#         if delivery_address_district.upper() == pickup_address_district.upper():
#             shipping_charge = 80
#         else:
#             shipping_charge = 200
        
#         context = {
#             'pickup_address': pickup_address,
#             'delivery_address': delivery_address,
#             'shipping_charge': shipping_charge,
#         }
#         return render(request, 'parcel_order/order_confirm.html', context)
    
#     else:
#         pickup_forms = PickUp_Address_Form()
#         delivery_forms = Delivery_Address_Form()
#         context = {'pickup_forms': pickup_forms, 'delivery_forms': delivery_forms}
#     return render(request, 'parcel_order/new_order.html', context)



