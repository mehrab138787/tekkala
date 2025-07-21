import os
import django
from channels.routing import get_default_application

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import tekstore.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tekkala.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        tekstore.routing.websocket_urlpatterns
    ),
})
