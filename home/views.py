from django.shortcuts import render, redirect, HttpResponse
from account.forms import Login_Form

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.user_type == 'Staff':
            return redirect('admin_dashboard')
        else:
            return redirect('delivery_order_list')
    
    form = Login_Form()
    context = {'form': form}
    return render(request, 'home/index.html', context)
