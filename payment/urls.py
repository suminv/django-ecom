from django.urls import path
from payment import views


urlpatterns = [
    path('payment_sucsses/', views.payment_success, name="payment_success"),
    

]
