from django.urls import path
from payment import views


urlpatterns = [
    path('payment_sucsses/', views.payment_success, name="payment_success"),
    path('checkout/', views.checkout, name="checkout"),
    path('billing_info/', views.billing_info, name="billing_info"),
    path('process_order/', views.process_order, name="process_order"),
    path('shipping_dashboard/', views.shipping_dashboard, name="shipping_dashboard"),
    path('orders/<int:pk>/', views.orders, name='orders')

]
