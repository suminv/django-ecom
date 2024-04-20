from django.contrib import admin
from .models import Category, Product, Customer, Order, Profile, Review
from django.contrib.auth.models import User





class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
    # Mix profile info and user infomation
    model = Profile

class UserAdmin(admin.ModelAdmin):
    # Extend User Model
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re - register the new way
admin.site.register(User, UserAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'review_message', 'data_time_stamp']
    readonly_fields = ['data_time_stamp']  # Указываем, что это поле только для чтения

admin.site.register(Review, ReviewAdmin)