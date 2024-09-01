from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stock import views

router = DefaultRouter()
router.register(prefix="", viewset=views.StockViewSet)

urlpatterns = [
    path("", include(router.urls))
]