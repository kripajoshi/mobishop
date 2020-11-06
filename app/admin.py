from django.contrib import admin

from app.models import Category
from app.models import Brand
from app.models import Product

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
