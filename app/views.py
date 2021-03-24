"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app.models import Product, Cart, CartItem, Address, Order, OrderItem
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    products = Product.objects.filter(is_featured=True)
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

def checkout(request):
   addresses = Address.objects.filter(user_id=request.user.id)
   if addresses.exists():
       address = addresses[0]
   else:
       address = Address()   
   return render(request,'app/checkout.html', 
          {
              'a': address,
              'title':'Checkout', 
              'year':datetime.now().year                                 
          })

def checkout_success(request):
   return render(request,'app/checkout_success.html',
          {
            'title':'Thank you for purchasing from us.', 
            'year':datetime.now().year
          })

def process_checkout(request):
    addresses = Address.objects.filter(user_id=request.user.id)
    if addresses.exists():
       address=addresses[0]
       address.first_name=request.POST.get('first_name')
       address.last_name= request.POST.get('last_name')
       address.address_line_1= request.POST.get('address_line_1')
       address.address_line_2= request.POST.get('address_line_2')
       address.city= request.POST.get('city')
       address.province= request.POST.get('province')
       address.postal_code= request.POST.get('postal_code')
       address.phone_number = request.POST.get('phone_number')
    else:
        address= Address(
            first_name=request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            address_line_1= request.POST.get('address_line_1'),
            address_line_2= request.POST.get('address_line_2'),
            city= request.POST.get('city'),
            province= request.POST.get('province'),
            postal_code= request.POST.get('postal_code'),
            phone_number = request.POST.get('phone_number'),
            user_id = request.user.id
        )
    address.save()

    carts = Cart.objects.filter(user_id=request.user.id).order_by('-created_on')
    if carts.exists():
       cart=carts[0]
       order = Order(user_id=cart.user_id)
       order.save()
       for cartItem in cart.cartitem_set.all():
           orderItem = OrderItem(
               product_id = cartItem.product.id,
               product_title  = cartItem.product.title,
               product_image = cartItem.product.image.url,
               order = order,
               unit_price = cartItem.unit_price,
               quantity = cartItem.quantity,
               total = cartItem.total
           )
           orderItem.save()
       cart.delete()

    return redirect(checkout_success)

def myaccount(request):
   return render(request,'app/myaccount.html', {
       'title':'My Account', 
       'year':datetime.now().year
       })

def order_history(request):
   orders = Order.objects.filter(user_id=request.user.id).order_by('-created_on')
   return render(request,'app/order_history.html', {'orders':orders, 'title':'Order History', 'year':datetime.now().year})

def change_password(request):
   return render(request,'app/change_password.html')

def process_change_password(request):
    user= authenticate(username=request.user.username, password=request.POST.get('current_password'))
    if user is not None:
        if request.POST.get('new_password')==request.POST.get('confirm_new_password'):
            user.set_password(request.POST.get('new_password'))
            user.save()
    return redirect(change_password)

def my_profile(request):
   user=User.objects.get(pk=request.user.id)
   return render(request,'app/my_profile.html',{'user':user})

def process_my_profile(request):
    user=User.objects.get(pk=request.user.id)
    user.first_name=request.POST.get('first_name')
    user.last_name=request.POST.get('last_name')
    user.save()
    return redirect (my_profile)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            else:
                return redirect(home)

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "app/register.html",
                          context={"form":form,'title': 'Register',
                           'year':datetime.now().year})

    form = UserCreationForm
    return render(request = request,
                  template_name = "app/register.html",
                  context={"form":form, 
                           'title': 'Register',
                           'year':datetime.now().year
                  })