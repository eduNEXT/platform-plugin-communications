"""
Test module for URLs.
"""
from django.test import TestCase

from platform_plugin_communications.api.views import search_learner_api_view, send_email_api_view
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
        assert urlpatterns[0].name == "send_email"
        assert (  # pylint: disable=comparison-with-callable
            urlpatterns[0].callback == send_email_api_view
        )
        assert urlpatterns[1].name == "search_learners"
        assert (  # pylint: disable=comparison-with-callable
            urlpatterns[1].callback == search_learner_api_view
        )
