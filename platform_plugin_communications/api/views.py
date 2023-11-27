"""API Views for the platform_plugin_forum_email_notifier plugin."""
import datetime
import json
import logging

import dateutil
import pytz
from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from opaque_keys.edx.keys import CourseKey

import platform_plugin_communications.utils as task_api
from platform_plugin_communications.edxapp_wrapper.bulk_email import create_course_email, is_bulk_email_feature_enabled
from platform_plugin_communications.edxapp_wrapper.course_overviews_api import get_course_overview_or_none
from platform_plugin_communications.edxapp_wrapper.instructor_views_api import (
    _get_branded_email_from_address,
    _get_branded_email_template,
    common_exceptions_400,
    permissions,
    require_course_permission,
    require_post_params,
)

log = logging.getLogger(__name__)


@transaction.non_atomic_requests
@require_POST
@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@require_course_permission(permissions.EMAIL)
@require_post_params(
    send_to="sending to whom", subject="subject line", message="message text"
)
@common_exceptions_400
def send_email_api_view(request, course_id):
    """
    Get the forum email notification preference for the user.

    Extracted from: lms.djangoapps.instructor.views.api import send_email
    """
    return send_email(request, course_id)


def send_email(request, course_id):
    """
    Send email to individual learners.
    """
    course_id = CourseKey.from_string(course_id)
    course_overview = get_course_overview_or_none(course_id)

    if not is_bulk_email_feature_enabled(course_id):
        log.warning(f"Email is not enabled for course {course_id}")
        return JsonResponse(
            {"message": "Email is not enabled for this course."}, status=403
        )

    emails = json.loads(request.POST.get("individual_learners_emails", "[]"))
    targets = json.loads(request.POST.get("send_to"))
    subject = request.POST.get("subject", "hi")
    message = request.POST.get("message", "Hi, this is an example email")
    # optional, this is a date and time in the form of an ISO8601 string
    schedule = request.POST.get("schedule", "")

    schedule_dt = None
    if schedule:
        try:
            # convert the schedule from a string to a datetime, then check if its a valid future date and time, dateutil
            # will throw a ValueError if the schedule is no good.
            schedule_dt = dateutil.parser.parse(schedule).replace(tzinfo=pytz.utc)
            if schedule_dt < datetime.datetime.now(pytz.utc):
                raise ValueError("the requested schedule is in the past")
        except ValueError as value_error:
            error_message = (
                f"Error occurred creating a scheduled bulk email task. Schedule provided: '{schedule}'. Error: "
                f"{value_error}"
            )
            log.error(error_message)
            return HttpResponseBadRequest(error_message)

    from_addr = _get_branded_email_from_address(course_overview)
    template_name = _get_branded_email_template(course_overview)

    try:
        email = create_course_email(
            course_id,
            request.user,
            targets,
            subject,
            message,
            template_name=template_name,
            from_addr=from_addr,
        )
    except ValueError as err:
        return HttpResponseBadRequest(repr(err))

    task_api.submit_bulk_course_email_to_learners(
        request, course_id, email.id, schedule_dt, emails
    )

    return JsonResponse(
        {
            "course_id": str(course_id),
            "success": True,
        }
    )
