from django.test import TestCase

from platform_plugin_communications.api.views import send_email_api_view
from platform_plugin_communications.urls import urlpatterns


class UrlTestCases(TestCase):
    """
    Test case for URL patterns.
    """

    def test_url_has_1_value(self):
        """
        Test case for checking the number of URL patterns.
        """
        assert len(urlpatterns) == 1
        assert urlpatterns[0].name == "send_email_to_individual_learners"
        assert urlpatterns[0].callback == send_email_api_view
