import os
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza.settings")

# 🔥 THIS LINE IS MANDATORY
django.setup()

from home import consumers  # import AFTER django.setup()

websocket_urlpatterns = [
    path("ws/pizza/<order_id>/", consumers.OrderProgress.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    }
)
