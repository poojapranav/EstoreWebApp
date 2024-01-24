from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django import forms
class demo(forms.Form):
    name=forms.CharField(max_length=20)
    email=forms.CharField(max_length=30)
class Product(models.Model):
    CAT=((1,'Mobile'),(2,'Shoes'),(3,'Cloth'))
    name=models.CharField(max_length=20,verbose_name='Product Name')
    price=models.FloatField()
    pdetails=models.CharField(max_length=50)
    cat=models.IntegerField(verbose_name='category',choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name='Available')
    pimage=models.ImageField(upload_to='image')
    def __str__(self):
        return self.name
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
