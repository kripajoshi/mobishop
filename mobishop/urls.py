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

