from django.urls import path
from store import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("update_user/", views.update_user, name="update_user"),
    path("update_info/", views.update_info, name="update_info"),
    path("update_password/", views.update_password, name="update_password"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("category/<slug:slug>/products/", views.category_products, name="category_products"),
    path("search/", views.search, name="search"),

]
