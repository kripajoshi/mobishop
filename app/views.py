"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app.models import Product, Cart, CartItem
from django.db.models import Sum

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    products = Product.objects.all()
    return render(
        request,
        'app/index.html',
        {
            'title':'Welcome to MobiShop',
            'year':datetime.now().year,
            'products': products
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def cart(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated == False:
        return redirect(f'/login/?redirect_to=/cart/')
    carts = Cart.objects.filter(user_id=request.user.id).order_by('-created_on')
    if carts.exists():
       cart = carts[0]
    else:
       cart = Cart(user_id = request.user.id)

    cartItems = cart.cartitem_set.all()
    grand_total = cart.cartitem_set.aggregate(Sum('total'))['total__sum']

    return render(
        request,
        'app/cart.html',
        {
            'title':'Cart',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'cartItems': cartItems,
            'grand_total': grand_total
        }
    )

def product_detail(request,id):
    product = Product.objects.get(pk=id)
    return render(
        request,
        'app/product_detail.html',
         {
            'title': product.title,
            'year':datetime.now().year,
            'p': product
         }
    )

def search(request):
    search_text = request.GET.get('search_text')
    products = Product.objects.filter(title__icontains=search_text)

    return render(request,'app/search.html',
                  {
                      'title': 'search',
                      'year': datetime.now().year,
                      'search': search_text,
                      'products': products

                  })

def add_to_cart(request):
    product_id=request.POST.get('product_id')
    if request.user.is_authenticated == False:
        return redirect(f'/login/?redirect_to=/products/{product_id}/')
    
    product = Product.objects.get(pk=product_id)
    carts = Cart.objects.filter(user_id=request.user.id).order_by('-created_on')
    if carts.exists():
       cart=carts[0]
    else:
       cart = Cart(user_id=request.user.id)
       cart.save()
    cartItems = cart.cartitem_set.filter(product_id=product_id)
    if cartItems.exists():
        cartItem = cartItems[0]
        cartItem.quantity = cartItem.quantity + 1
        cartItem.total = product.unit_price * cartItem.quantity
    else: 
        cartItem = CartItem(cart = cart, product = product, quantity = 1, unit_price = product.unit_price, total = product.unit_price * 1)
    cartItem.save()
    return redirect(product_detail, id=product_id)

def remove_cart_item(request):
    cart_item_id=request.POST.get('cart_item_id')
    cartItem = CartItem.objects.get(pk = cart_item_id)
    cartItem.delete()
    return redirect(cart)

def update_cart_item(request):
    cart_item_id=request.POST.get('cart_item_id')
    quantity = int(request.POST.get('quantity'))
    cartItem = CartItem.objects.get(pk = cart_item_id)
    cartItem.quantity = quantity
    cartItem.total = cartItem.unit_price * cartItem.quantity
    cartItem.save()
    return redirect(cart)

def checkout(request,id):
   return render(request, )