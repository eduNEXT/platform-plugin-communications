"""
URLs for platform_plugin_communications.
"""
from django.urls import path

from platform_plugin_communications.api.views import send_email_api_view

urlpatterns = [
    path(
        "send_email",
        send_email_api_view,
        name="send_email",
    ),
]
