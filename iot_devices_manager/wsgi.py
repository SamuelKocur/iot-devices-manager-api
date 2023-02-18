"""
WSGI config for iot_devices_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iot_devices_manager.settings')

application = get_wsgi_application()

# from mqtt.clients.mqtt_client import thread as mqtt_thread
#
# mqtt_thread.start()
