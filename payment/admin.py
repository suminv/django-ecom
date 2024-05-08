from dataclasses import fields
from django.contrib import admin
from .models import ShipppingAddres, Order, OrderItem


admin.site.register(ShipppingAddres)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create OrderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    fields = ['full_name', 'email', 'shipping_address','amount_paid', 'date_ordered', 'shipped', 'date_shipped']
    inlines = [OrderItemInline]

# Unregister the old model
admin.site.unregister(Order)

#Re - register our Order and OrderAdmin
admin.site.register(Order, OrderAdmin)