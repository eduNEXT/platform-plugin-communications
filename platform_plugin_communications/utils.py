"""
Utilities for the communications plugin.
"""
import hashlib
from collections import Counter

from platform_plugin_communications.edxapp_wrapper.bulk_email import get_course_email
from platform_plugin_communications.edxapp_wrapper.instructor_tasks import (
    InstructorTaskTypes,
    schedule_task,
    submit_task,
)
from platform_plugin_communications.tasks import send_bulk_course_email_to_learners


def submit_bulk_course_email_to_learners(
    request, course_key, email_id, schedule=None, emails=[]
):
    """
    Submit a bulk email to individual learners.

    Extracted from: lms.djangoapps.instructor.views.api.submit_bulk_course_email
    """
    email_obj = get_course_email(email_id)
    # task_input has a limit to the size it can store, so any target_type with count > 1 is combined and counted
    targets = Counter([target.target_type for target in email_obj.targets.all()])
    targets = [
        target if count <= 1 else f"{count} {target}"
        for target, count in targets.items()
    ]

    task_type = InstructorTaskTypes.BULK_COURSE_EMAIL
    task_class = send_bulk_course_email_to_learners
    task_input = {"email_id": email_id, "to_option": targets, "emails": emails}
    task_key_stub = str(email_id)
    # create the key value by using MD5 hash:
    task_key = hashlib.md5(task_key_stub.encode("utf-8")).hexdigest()

    if schedule:
        return schedule_task(
            request, task_type, course_key, task_input, task_key, schedule
        )

    return submit_task(request, task_type, task_class, course_key, task_input, task_key)
