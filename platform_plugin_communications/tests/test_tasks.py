"""
Test for tasks.
"""
from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from platform_plugin_communications.tasks import (
    perform_delegate_email_batches_to_learners,
    send_bulk_course_email_to_learners,
)


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
class TestTasks(TestCase):
    """
    Test case for tasks.
    """

    @patch("platform_plugin_communications.tasks.run_main_task")
    def test_send_bulk_course_email_to_learners(self, mock_run_main_task):
        """
        Test case for sending email to individual learners.
        """

        mock_run_main_task.return_value = True

        entry_id = 1
        _xblock_instance_args = None

        send_bulk_course_email_to_learners(entry_id, _xblock_instance_args)

        mock_run_main_task.assert_called_once_with(
            entry_id, perform_delegate_email_batches_to_learners, "emailed"
        )

    @patch("platform_plugin_communications.tasks.InstructorTask")
    @patch("platform_plugin_communications.tasks.queue_subtasks_for_query")
    @patch("platform_plugin_communications.tasks.send_course_email")
    @patch("platform_plugin_communications.tasks.CourseEmail")
    @patch("platform_plugin_communications.tasks.get_course")
    @patch("platform_plugin_communications.tasks._get_course_email_context")
    @patch("platform_plugin_communications.target.User")
    def test_perform_delegate_email_batches_to_learners(
        self,
        mock_User,
        mock_get_course_email_context,
        mock_get_course,
        mock_CourseEmail,
        mock_send_course_email,
        mock_queue_subtasks_for_query,
        mock_InstructorTask,
    ):
        """
        Test case for sending email to individual learners.
        """
        course_id = "course-v1:edX+DemoX+Demo_Course"
        instructor_task_mock = Mock(requester=Mock(id=1), task_id=1)
        instructor_task_mock.subtasks = []
        instructor_task_mock.course_id = course_id
        mock_InstructorTask.objects.get.return_value = instructor_task_mock
        mock_queue_subtasks_for_query.return_value = True
        mock_send_course_email.return_value = True
        target_mock = Mock(target_type="myself")
        target_mock.get_users.return_value = Mock(id=1)
        mock_union = Mock(id=1)
        target_mock.get_users.return_value.union.return_value = mock_union
        target_mock.get_users.return_value.union.return_value.count.return_value = 2
        mock_course_email_instance = Mock(course_id=course_id)
        mock_course_email_instance.targets.all.return_value = [target_mock]
        mock_CourseEmail.objects.get.return_value = mock_course_email_instance
        mock_get_course.return_value = Mock(id=course_id)
        mock_get_course_email_context.return_value = {"course": Mock(id=course_id)}
        mock_User.objects.filter.return_value = {Mock(id=1)}
        entry_id = 1
        course_id = mock_InstructorTask.objects.get.return_value.course_id
        task_input = {
            "email_id": 1,
            "to_option": ["myself"],
            "extra_targets": {"emails": ["test@openedx.org"]},
        }

        perform_delegate_email_batches_to_learners(
            entry_id, course_id, task_input, "emailed"
        )

        mock_InstructorTask.objects.get.assert_called_once_with(pk=entry_id)
        mock_CourseEmail.objects.get.assert_called_once_with(id=task_input["email_id"])
        mock_get_course.assert_called_once_with(course_id)
        mock_get_course_email_context.assert_called_once_with(
            mock_get_course.return_value
        )
        mock_User.objects.filter.assert_called_once_with(
            email__in=task_input["extra_targets"]["emails"],
            is_active=True,
            courseenrollment__course_id=course_id,
            courseenrollment__is_active=True,
        )

        args, kwargs = mock_queue_subtasks_for_query.call_args
        expected = (
            instructor_task_mock,
            "emailed",
            [mock_union],
            ["profile__name", "email", "username"],
            1,
            2,
        )
        for arg in expected:
            self.assertIn(
                arg,
                args,
            )
