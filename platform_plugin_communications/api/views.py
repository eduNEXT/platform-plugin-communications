"""API Views for the platform_plugin_forum_email_notifier plugin."""
import logging

from django.http import JsonResponse
from rest_framework.views import APIView

log = logging.getLogger(__name__)


class SendEmailAPIView(APIView):
    """
    API endpoint that allows to update the forum email notification preference.
    """

    def get(self, request, course_id):
        """
        Get the forum email notification preference for the user.
        """
        return JsonResponse({"status": "ok"})


send_email_api_view = SendEmailAPIView.as_view()
