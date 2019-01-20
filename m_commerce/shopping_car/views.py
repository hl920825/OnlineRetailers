from django.shortcuts import render

# Create your views here.

def shopcart_empty(request):

    return render(request,'shopping_car/shopcart.html')