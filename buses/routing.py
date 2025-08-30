from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/buses/$', consumers.BusTrackingConsumer.as_asgi()),
    re_path(r'ws/route/(?P<route_id>\w+)/$', consumers.RouteTrackingConsumer.as_asgi()),
]