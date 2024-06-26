from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from ecom import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("store.urls")),
    path("cart/", include("cart.urls")),
    path("payment/", include("payment.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
