from django.urls import path, include
from rest_framework.routers import DefaultRouter

from option import views

router = DefaultRouter()
router.register(prefix="", viewset=views.OptionViewSet)

urlpatterns = [
    path("", include(router.urls))
]