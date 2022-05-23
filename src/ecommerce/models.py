from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=350)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    img_url = models.CharField(max_length=350)
    stock = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Order(models.Model):
    date = models.DateField()
    total_price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
