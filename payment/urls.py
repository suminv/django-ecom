from django.urls import path
from payment import views


urlpatterns = [
    path('payment_sucsses/', views.payment_success, name="payment_success"),
    path('checkout/', views.checkout, name="checkout"),
    path('billing_info/', views.billing_info, name="billing_info"),


]
