import datetime

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = 'Categories'




class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    description = models.CharField(max_length=255, default='', blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="upload/product/")

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self) -> str:
        return str(self.name)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=255, default='', blank=True)
    phone = models.CharField(max_length=10, default='', blank=True)
    data = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)


    def __str__(self) -> str:
        return str(self.product)
