from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from machine import routing
from machine.routing import websocket_urlpatterns


application = ProtocolTypeRouter(
    {
        'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns,
        ))
    }
)