import json
import logging

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_noop

User = get_user_model()

log = logging.getLogger("edx.celery.task")


try:
    from common.djangoapps.util.query import use_read_replica_if_available
    from lms.djangoapps.bulk_email.models import CourseEmail
    from lms.djangoapps.bulk_email.tasks import _get_course_email_context, send_course_email
    from lms.djangoapps.courseware.courses import get_course
    from lms.djangoapps.instructor_task.models import InstructorTask
    from lms.djangoapps.instructor_task.subtasks import queue_subtasks_for_query
    from lms.djangoapps.instructor_task.tasks_helper.runner import run_main_task
except ImportError:
    use_read_replica_if_available = None
    run_main_task = None
    InstructorTask = None
    CourseEmail = None
    get_course = None
    _get_course_email_context = None
    queue_subtasks_for_query = None


@shared_task
def send_bulk_course_email_to_learners(
    entry_id, _xblock_instance_args
):  # pylint: disable=unused-argument
    """
    Send email to individual learners.

    Extracted from: lms.djangoapps.instructor_task.tasks.send_bulk_course_email
    """
    action_name = gettext_noop("emailed")
    visit_fcn = perform_delegate_email_batches_to_learners
    return run_main_task(entry_id, visit_fcn, action_name)


def perform_delegate_email_batches_to_learners(
    entry_id, course_id, task_input, action_name
):
    """

    Extracted from: lms.djangoapps.bulk_email.tasks.perform_delegate_email_batches
    """
    emails = task_input.get("emails", [])
    entry = InstructorTask.objects.get(pk=entry_id)
    # Get inputs to use in this task from the entry.
    user_id = entry.requester.id
    task_id = entry.task_id

    # Perfunctory check, since expansion is made for convenience of other task
    # code that doesn't need the entry_id.
    if course_id != entry.course_id:
        format_msg = (
            "Course id conflict: explicit value %r does not match task value %r"
        )
        log.warning(
            "Task %s: " + format_msg, task_id, course_id, entry.course_id
        )  # lint-amnesty, pylint: disable=logging-not-lazy
        raise ValueError(format_msg % (course_id, entry.course_id))

    # Fetch the CourseEmail.
    email_id = task_input["email_id"]
    try:
        email_obj = CourseEmail.objects.get(id=email_id)
    except CourseEmail.DoesNotExist:
        # The CourseEmail object should be committed in the view function before the task
        # is submitted and reaches this point.
        log.warning("Task %s: Failed to get CourseEmail with id %s", task_id, email_id)
        raise

    # Check to see if email batches have already been defined.  This seems to
    # happen sometimes when there is a loss of connection while a task is being
    # queued.  When this happens, the same task gets called again, and a whole
    # new raft of subtasks gets queued up.  We will assume that if subtasks
    # have already been defined, there is no need to redefine them below.
    # So we just return right away.  We don't raise an exception, because we want
    # the current task to be marked with whatever it had been marked with before.
    if len(entry.subtasks) > 0 and len(entry.task_output) > 0:
        log.warning(
            "Task %s has already been processed for email %s!  InstructorTask = %s",
            task_id,
            email_id,
            entry,
        )
        progress = json.loads(entry.task_output)
        return progress

    # Sanity check that course for email_obj matches that of the task referencing it.
    if course_id != email_obj.course_id:
        format_msg = (
            "Course id conflict: explicit value %r does not match email value %r"
        )
        log.warning(
            "Task %s: " + format_msg, task_id, course_id, email_obj.course_id
        )  # lint-amnesty, pylint: disable=logging-not-lazy
        raise ValueError(format_msg % (course_id, email_obj.course_id))

    # Fetch the course object.
    course = get_course(course_id)

    # Get arguments that will be passed to every subtask.
    targets = email_obj.targets.all()
    global_email_context = _get_course_email_context(course)

    recipient_qsets = [target.get_users(course_id, user_id) for target in targets]

    emails = task_input["emails"]

    enrollment_query = models.Q(
        is_active=True,
        courseenrollment__course_id=course_id,
        courseenrollment__is_active=True,
    )

    if emails:
        recipient_qsets.append(
            use_read_replica_if_available(
                User.objects.filter(models.Q(email__in=emails) & enrollment_query)
            )
        )
    # Use union here to combine the qsets instead of the | operator.  This avoids generating an
    # inefficient OUTER JOIN query that would read the whole user table.
    combined_set = (
        recipient_qsets[0].union(*recipient_qsets[1:])
        if len(recipient_qsets) > 1
        else recipient_qsets[0]
    )
    recipient_fields = ["profile__name", "email", "username"]

    log.info(
        "Task %s: Preparing to queue subtasks for sending emails for course %s, email %s",
        task_id,
        course_id,
        email_id,
    )

    total_recipients = combined_set.count()

    # Weird things happen if we allow empty querysets as input to emailing subtasks
    # The task appears to hang at "0 out of 0 completed" and never finishes.
    if total_recipients == 0:
        msg = "Bulk Email Task: Empty recipient set"
        log.warning(msg)
        raise ValueError(msg)

    def _create_send_email_subtask(to_list, initial_subtask_status):
        """Creates a subtask to send email to a given recipient list."""
        subtask_id = initial_subtask_status.task_id
        new_subtask = send_course_email.subtask(
            (
                entry_id,
                email_id,
                to_list,
                global_email_context,
                initial_subtask_status.to_dict(),
            ),
            task_id=subtask_id,
        )
        return new_subtask

    progress = queue_subtasks_for_query(
        entry,
        action_name,
        _create_send_email_subtask,
        [combined_set],
        recipient_fields,
        settings.BULK_EMAIL_EMAILS_PER_TASK,
        total_recipients,
    )

    # We want to return progress here, as this is what will be stored in the
    # AsyncResult for the parent task as its return value.
    # The AsyncResult will then be marked as SUCCEEDED, and have this return value as its "result".
    # That's okay, for the InstructorTask will have the "real" status, and monitoring code
    # should be using that instead.
    return progress
