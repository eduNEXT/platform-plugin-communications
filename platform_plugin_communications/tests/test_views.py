"""
Tests for views.
"""
import datetime
import hashlib
import json
from unittest.mock import Mock, patch

import pytz
from django.db import models
from django.test import TestCase, override_settings
from opaque_keys.edx.keys import CourseKey

from platform_plugin_communications.api.views import search_learner, send_email
from platform_plugin_communications.edxapp_wrapper.instructor_tasks import InstructorTaskTypes
from platform_plugin_communications.tasks import send_bulk_course_email

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
        "platform_plugin_communications.edxapp_wrapper.backends.instructor_views_p_v1_test"
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
    def test_send_email(
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
        course_email_mock.targets.all.return_value = [
            Target(target) for target in targets
        ]
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
            send_bulk_course_email,
            course_key,
            {
                "email_id": email_id,
                "to_option": targets,
                "extra_targets": extra_targets,
            },
            hashlib.md5(str(email_id).encode("utf-8")).hexdigest(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "course_id": course_id,
                "success": True,
            },
        )

    @patch("platform_plugin_communications.api.views.get_course_overview_or_none")
    @patch("platform_plugin_communications.api.views.is_bulk_email_feature_enabled")
    @patch("platform_plugin_communications.api.views.create_course_email")
    @patch("platform_plugin_communications.utils.get_course_email")
    @patch("platform_plugin_communications.utils.schedule_task")
    def test_send_email_with_schedule(
        self,
        mock_schedule_task,
        mock_get_course_email,
        mock_create_course_email,
        mock_is_bulk_email_feature_enabled,
        mock_get_course_overview_or_none,
    ):
        """
        Test case for sending email to individual learners with schedule.
        """
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


class TestSearchUsersAPIView(TestCase):
    """
    Test case for search_learners_api_view.
    """

    @patch("platform_plugin_communications.api.views.User")
    def test_search_users(self, mock_User):
        """
        Test case for search users API View.
        """

        request = Mock()
        request.method = "GET"
        request.GET = {}
        course_id = "course-v1:edX+DemoX+Demo_Course"
        course_key = CourseKey.from_string(course_id)
        users = [
            {
                "email": "test@openedx.org",
                "username": "test",
                "name": "test",
            }
        ]
        users_mock = []
        for user in users:
            user_mock = Mock()
            user_mock.username = user["username"]
            user_mock.email = user["email"]
            user_mock.profile.name = user["name"]
            users_mock.append(user_mock)
        mock_User.objects.filter.return_value = users_mock
        response = search_learner(request, course_id)

        mock_User.objects.filter.assert_called_once_with(
            is_active=True,
            courseenrollment__course_id=course_key,
            courseenrollment__is_active=True,
        )
        assert response.status_code == 200
        assert json.loads(response.content) == {
            "total": 1,
            "page": 1,
            "pages": 1,
            "page_size": 50,
            "course_id": course_id,
            "results": users,
        }

    @patch("platform_plugin_communications.api.views.User")
    def test_search_users_with_query(self, mock_User):
        """
        Test case for search users API View with query.
        """

        request = Mock()
        request.method = "GET"
        request.GET = {
            "query": "test",
        }
        course_id = "course-v1:edX+DemoX+Demo_Course"
        course_key = CourseKey.from_string(course_id)
        users = [
            {
                "email": "test@openedx.org",
                "username": "test",
                "name": "test",
            }
        ]
        users_mock = []
        for user in users:
            user_mock = Mock()
            user_mock.username = user["username"]
            user_mock.email = user["email"]
            user_mock.profile.name = user["name"]
            users_mock.append(user_mock)
        mock_filter = Mock()
        mock_User.objects.filter.return_value = mock_filter
        mock_filter2 = Mock()
        mock_filter.filter.return_value = mock_filter2
        mock_filter2.distinct.return_value = users_mock
        response = search_learner(request, course_id)

        mock_User.objects.filter.assert_called_once_with(
            is_active=True,
            courseenrollment__course_id=course_key,
            courseenrollment__is_active=True,
        )
        mock_User.objects.filter().filter.assert_called_once_with(
            models.Q(  # pylint: disable=unsupported-binary-operation
                email__icontains="test"
            )
            | models.Q(username__icontains="test")
            | models.Q(profile__name__icontains="test"),
        )
        mock_User.objects.filter().filter().distinct.assert_called_once()
        assert response.status_code == 200
        assert json.loads(response.content) == {
            "total": 1,
            "page": 1,
            "pages": 1,
            "page_size": 50,
            "course_id": course_id,
            "results": users,
        }
