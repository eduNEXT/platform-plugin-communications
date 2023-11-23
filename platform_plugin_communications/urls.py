"""
URLs for platform_plugin_communications.
"""
from django.urls import re_path

from platform_plugin_communications.api.views import SendEmailAPIView

urlpatterns = [
    re_path(
        r"^individual_learners",
        SendEmailAPIView.as_view(),
        name="send_email_to_individual_learners",
    ),
]
