from django.contrib.auth.models import Permission, User
from django.db import models
from datetime import datetime,timedelta


class Product(models.Model):
	product_id = models.CharField(max_length=250)
	user = models.ForeignKey(User, default=1)
	customer = models.CharField(max_length=250, blank=True)
	start_price = models.IntegerField(default=0)
	bought = models.BooleanField(default=False)
	product_name = models.CharField(max_length=400)
	min_increase = models.IntegerField(default=5)
	description = models.TextField(default='product description')
	current_price = models.IntegerField(max_length=100,default=0)
	category = models.CharField(default = "general", max_length=100)
	status = models.CharField(max_length=10, default='live')
	date = models.DateTimeField(default=datetime.now(), blank=True)
	rem_days = models.IntegerField(help_text="enter in days",default="2")
	days = models.IntegerField(help_text="enter in days",default="2")
	end_date = models.DateTimeField(blank=True)
	product_image = models.FileField()

	def __str__(self):
		return self.product_name + ' - ' + str(self.rem_days)

class Profile(models.Model):
	first_name = models.CharField(max_length=100,default="whatever")
	last_name = models.CharField(max_length=100,default="whatever")
	contact = models.IntegerField(default="whatever")
	Address = models.CharField(max_length=300,default="whatever")
		
class Bid(models.Model):
	user = models.ForeignKey(User, default=1)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	bid_value = models.IntegerField(max_length=250)

	def __str__(self):
		return self.bid_value