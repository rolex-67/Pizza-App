from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    pizza = Pizza.objects.all()
    
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = [] # Empty list for guests
        
    context = {'pizza': pizza, 'orders': orders}
    return render(request, 'index.html', context)

def order(request , order_id):
    order = Order.objects.filter(order_id=order_id).first()
    if order is None:
        return redirect('/')
    
    context = {'order' : order}
    return render(request , 'order.html', context)
    
@csrf_exempt
def order_pizza(request):
    try:
        data = json.loads(request.body)
        pizza = Pizza.objects.get(id=data.get('id'))
        
        # If user is logged in, use their account
        # Otherwise, create anonymous order with a guest user
        if request.user.is_authenticated:
            user = request.user
        else:
            # Get or create a generic guest user for anonymous orders
            user, created = User.objects.get_or_create(
                username='guest',
                defaults={'email': 'guest@pizza.com'}
            )
        
        order = Order(user=user, pizza=pizza, amount=pizza.price)
        order.save()
        
        return JsonResponse({
            'message': 'Success', 
            'order_id': order.order_id,
            'amount': order.amount  # Add amount to response
        })
        
    except Pizza.DoesNotExist:
        return JsonResponse({'error': 'Pizza not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)