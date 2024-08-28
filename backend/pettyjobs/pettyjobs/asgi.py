import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from pettyjobsapp.websocket.middleware import JWTAuthMiddleware
from pettyjobsapp.websocket.routing import websocket_patterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pettyjobs.settings')
django_asgi_application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        'http': django_asgi_application,
        'websocket':
        JWTAuthMiddleware(
            URLRouter(
                websocket_patterns
            )
        )
    }
)
