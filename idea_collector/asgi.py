"""
ASGI config for idea_collector project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
#calling the asgi app so the following imports work
django_asgi_app = get_asgi_application()

from idea_collector.routing import ws_urlpatterns
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idea_collector.settings')

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})