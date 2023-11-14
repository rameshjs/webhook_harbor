from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/events/(?P<workspace_id>\S+)/$", consumers.NotifyConsumer.as_asgi()),
]
