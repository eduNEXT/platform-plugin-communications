"""
Tests for views.
"""
import datetime
import hashlib
import json
from unittest.mock import Mock, patch

import pytz
from django.test import TestCase, override_settings
from opaque_keys.edx.keys import CourseKey

from platform_plugin_communications.api.views import send_email
from platform_plugin_communications.tasks import send_bulk_course_email_to_learners

delta = datetime.timedelta(days=1)
now = datetime.datetime.now()
tomorrow = now + delta


class Target(Mock):
    """
    Mock class for Target.
    """

    def __init__(self, target_type):
        super().__init__()
        self.target_type = target_type


@override_settings(
    PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND=(
        "platform_plugin_communications.edxapp_wrapper.backends.bulk_email_api_p_v1_test"
    ),
    PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND=(
        "platform_plugin_communications.edxapp_wrapper.backends.instructor_views_api_p_v1_test"
    ),
    PLATFORM_PLUGIN_COMMUNICATIONS_COURSE_OVERVIEWS_BACKEND=(
        "platform_plugin_communications.edxapp_wrapper.backends.course_overviews_p_v1_test"
    ),
    PLATFORM_PLUGIN_COMMUNICATIONS_UTIL_QUERY_BACKEND=(
        "platform_plugin_communications.edxapp_wrapper.backends.util_query_p_v1_test"
    ),
    PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND=(
        "platform_plugin_communications.edxapp_wrapper.backends.instructor_tasks_p_v1_test"
    ),
    PLATFORM_PLUGIN_COMMUNICATIONS_COURSEWARE_COURSES_BACKEND=(
        "platform_plugin_communications.edxapp_wrapper.backends.courseware_courses_p_v1_test"
    ),
)
class TestSendEmailAPIView(TestCase):
    """
    Test case for send_email_api_view.
    """

    @patch("platform_plugin_communications.api.views.get_course_overview_or_none")
    @patch("platform_plugin_communications.api.views.is_bulk_email_feature_enabled")
    @patch("platform_plugin_communications.api.views.create_course_email")
    @patch("platform_plugin_communications.utils.get_course_email")
    @patch("platform_plugin_communications.utils.submit_task")
    def test_send_email_to_individual_learners(
        self,
        mock_submit_task,
        mock_get_course_email,
        mock_create_course_email,
        mock_is_bulk_email_feature_enabled,
        mock_get_course_overview_or_none,
    ):
        """
        Test case for sending email to individual learners.
        """
        from platform_plugin_communications.edxapp_wrapper.instructor_tasks import (  # noqa pylint: disable=import-outside-toplevel
            InstructorTaskTypes,
        )

        request = Mock()
        request.method = "POST"
        targets = ["myself"]
        individual_learners_emails = ["student@openedx.org"]
        subject = "Test Subject"
        message = "Test Message"
        extra_targets = {"emails": individual_learners_emails}
        request.POST = {
            "extra_targets": json.dumps(extra_targets),
            "send_to": json.dumps(targets),
            "subject": subject,
            "message": message,
        }
        course_id = "course-v1:edX+DemoX+Demo_Course"
        mock_is_bulk_email_feature_enabled.return_value = True
        mock_get_course_overview_or_none.return_value = Mock()
        course_email_mock = Mock()
        mock_get_course_email.return_value = course_email_mock
        course_email_mock.targets.all.return_value = [Target(x) for x in targets]
        mock_create_course_email.return_value = course_email_mock
        mock_submit_task.return_value = Mock()
        course_key = CourseKey.from_string(course_id)

        response = send_email(request, course_id)

        mock_is_bulk_email_feature_enabled.assert_called_once_with(course_key)
        mock_create_course_email.assert_called_once_with(
            course_key,
            request.user,
            targets,
            subject,
            message,
            template_name="test_template",
            from_addr="test@openedx.org",
        )
        course_email_mock.targets.all.assert_called_once()
        email_id = course_email_mock.id

        mock_submit_task.assert_called_once_with(
            request,
            InstructorTaskTypes.BULK_COURSE_EMAIL,
            send_bulk_course_email_to_learners,
            course_key,
            {
                "email_id": email_id,
                "to_option": targets,
                "extra_targets": extra_targets,
            },
            hashlib.md5(str(email_id).encode("utf-8")).hexdigest(),
        )

        assert response.status_code == 200
        assert json.loads(response.content) == {
            "course_id": course_id,
            "success": True,
        }

    @patch("platform_plugin_communications.api.views.get_course_overview_or_none")
    @patch("platform_plugin_communications.api.views.is_bulk_email_feature_enabled")
    @patch("platform_plugin_communications.api.views.create_course_email")
    @patch("platform_plugin_communications.utils.get_course_email")
    @patch("platform_plugin_communications.utils.schedule_task")
    def test_send_email_to_individual_learners_with_schedule(
        self,
        mock_schedule_task,
        mock_get_course_email,
        mock_create_course_email,
        mock_is_bulk_email_feature_enabled,
        mock_get_course_overview_or_none,
    ):
        """
        Test case for sending email to individual learners.
        """
        from platform_plugin_communications.edxapp_wrapper.instructor_tasks import (  # noqa pylint: disable=import-outside-toplevel
            InstructorTaskTypes,
        )

        request = Mock()
        request.method = "POST"
        targets = ["myself"]
        individual_learners_emails = ["student@openedx.org"]
        subject = "Test Subject"
        message = "Test Message"
        extra_targets = {"emails": individual_learners_emails}
        request.POST = {
            "extra_targets": json.dumps(extra_targets),
            "send_to": json.dumps(targets),
            "subject": subject,
            "message": message,
            "schedule": tomorrow.isoformat(),
        }
        course_id = "course-v1:edX+DemoX+Demo_Course"
        mock_is_bulk_email_feature_enabled.return_value = True
        mock_get_course_overview_or_none.return_value = Mock()
        course_email_mock = Mock()
        mock_get_course_email.return_value = course_email_mock
        course_email_mock.targets.all.return_value = [Target(x) for x in targets]
        mock_create_course_email.return_value = course_email_mock
        mock_schedule_task.return_value = Mock()
        course_key = CourseKey.from_string(course_id)

        response = send_email(request, course_id)

        mock_is_bulk_email_feature_enabled.assert_called_once_with(course_key)
        mock_create_course_email.assert_called_once_with(
            course_key,
            request.user,
            targets,
            subject,
            message,
            template_name="test_template",
            from_addr="test@openedx.org",
        )
        course_email_mock.targets.all.assert_called_once()
        email_id = course_email_mock.id

        mock_schedule_task.assert_called_once_with(
            request,
            InstructorTaskTypes.BULK_COURSE_EMAIL,
            course_key,
            {
                "email_id": email_id,
                "to_option": targets,
                "extra_targets": extra_targets,
            },
            hashlib.md5(str(email_id).encode("utf-8")).hexdigest(),
            tomorrow.replace(tzinfo=pytz.utc),
        )
        assert response.status_code == 200
        assert json.loads(response.content) == {
            "course_id": course_id,
            "success": True,
        }
