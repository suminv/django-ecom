import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=255, blank=True)
    old_cart = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    """
    A function that creates a user profile by default when a new user is signed up.
    """
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# Automatically the profile thing is created
post_save.connect(create_user_profile, sender=User)



class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Categories"


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    description = models.TextField(max_length=500, default="", blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="upload/product/")
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self) -> str:
        return str(self.name)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=255, default="", blank=True)
    phone = models.CharField(max_length=10, default="", blank=True)
    data = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.product)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_subject = models.CharField(max_length=255, default="", blank=True)
    review_message = models.TextField(max_length=1000, default="", blank=True)
    review_photo = models.ImageField(null=True, blank=True, upload_to="upload/review/")
    rating = models.IntegerField(default=5)
    # data_time_stamp = models.DateTimeField(default=datetime.datetime.today)
    data_time_stamp = models.DateTimeField(default=timezone.now)  
    def __str__(self) -> str:
        return str(self.product)