from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from store.models import Product


class ShipppingAddres(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_zipcode = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f'Shiping Address for - {str(self.id)} '

def create_shipping(sender, instance, created, **kwargs):
    """
    A function that creates a user shipping address by default when a new user is signed up.
    """
    if created:
        user_shipping = ShipppingAddres(user=instance)
        user_shipping.save()

# Automatically the profile thing is created
post_save.connect(create_shipping, sender=User)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Order - {str(self.id)}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quatity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self) -> str:
        return f'Order Item - {str(self.id)}'
    