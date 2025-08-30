from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'routes', views.RouteViewSet)
router.register(r'buses', views.BusViewSet)
router.register(r'locations', views.BusLocationViewSet)
router.register(r'stops', views.RouteStopViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]