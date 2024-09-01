from django.urls import path, include
from rest_framework.routers import DefaultRouter

from position import views

router = DefaultRouter()
router.register(prefix="", viewset=views.PositionViewSet)

urlpatterns = [
    path("statistic/", views.statistic, name="statistic"),
    path("start-publishing/", views.start_publishing, name="start-publishing"),
    path("stop-publishing/", views.stop_publishing, name="stop-publishing"),
    path("", include(router.urls)),
]
