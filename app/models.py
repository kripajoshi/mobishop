"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=100)
	created_on = models.DateField(auto_now_add=True)
	last_modified = models.DateField(auto_now=True)
	def __str__(self):
		return self.name

class Brand(models.Model):
	name = models.CharField(max_length=100)
	created_on = models.DateField(auto_now_add=True)
	last_modified = models.DateField(auto_now=True)
	def __str__(self):
		return self.name

class Product(models.Model):
	title = models.CharField(max_length=500)
	description = models.CharField(max_length=3000)
	unit_price = models.IntegerField()
	image = models.ImageField(upload_to='uploads/')
	is_featured = models.BooleanField()
	created_on = models.DateField(auto_now_add=True)
	last_modified = models.DateField(auto_now=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
	def __str__(self):
		return self.title

class Cart(models.Model):
	user_id = models.IntegerField()
	created_on = models.DateField(auto_now_add=True)
	last_modified = models.DateField(auto_now=True)

class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	unit_price= models.IntegerField()
	quantity= models.IntegerField()
	total=models.IntegerField()