"""
Definition of urls for mobishop.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls.static import static
from django.conf import settings
from os import path as osPath

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_cart_item', views.remove_cart_item, name='remove_cart_item'),
    path('update_cart_item', views.update_cart_item, name='update_cart_item'),
    path('process_checkout', views.process_checkout, name='process_checkout'),
    path('checkout',views.checkout, name='checkout'),
    path('checkout_success',views.checkout_success, name='checkout_success'),
    path('myaccount', views.myaccount, name='myaccount'),
    path('orderhistory', views.order_history, name='order_history'),
    path('changepassword', views.change_password, name='change_password'),
    path('myprofile', views.my_profile, name='my_profile'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('cart/', views.cart, name='cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

