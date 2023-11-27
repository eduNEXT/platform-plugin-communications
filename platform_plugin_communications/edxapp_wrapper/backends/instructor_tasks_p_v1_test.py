"""
Backend for instructor.views.api module.
"""
from unittest.mock import Mock

send_course_email = object
schedule_task = object
submit_task = object
InstructorTaskTypes = Mock()
InstructorTaskTypes.BULK_EMAIL = "bulk_email"
InstructorTask = Mock()
queue_subtasks_for_query = object
run_main_task = object
