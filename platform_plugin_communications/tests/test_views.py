from unittest.mock import Mock

from django.test import TestCase

from platform_plugin_communications.api.views import SendEmailAPIView


class TestSendEmailAPIView(TestCase):
    """
    Test case for SendEmailAPIView.
    """

    def setUp(self):
        super().setUp()
        self.api = SendEmailAPIView()

    def test_send_email_to_individual_learners(self):
        """
        Test case for sending email to individual learners.
        """
        request = Mock()
        course_id = "course-v1:edX+DemoX+Demo_Course"
        response = self.api.get(request, course_id)
        assert response.status_code == 200
