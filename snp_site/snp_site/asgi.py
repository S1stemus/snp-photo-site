"""
ASGI config for snp_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from snp_site import routing
from snp_site.middlewares import JwtAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snp_site.settings")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JwtAuthMiddleware(URLRouter(routing.websocket_urlpatterns)),
    }
)
