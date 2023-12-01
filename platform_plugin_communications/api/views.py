"""API Views for the plugin platform-plugin-communications."""
import datetime
import json
import logging

import dateutil
import pytz
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import models, transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from opaque_keys.edx.keys import CourseKey

import platform_plugin_communications.utils as task_api
from platform_plugin_communications.api.serializers import UserSearchSerializer
from platform_plugin_communications.edxapp_wrapper.bulk_email import create_course_email, is_bulk_email_feature_enabled
from platform_plugin_communications.edxapp_wrapper.course_overviews import get_course_overview_or_none
from platform_plugin_communications.edxapp_wrapper.instructor_views import (
    _get_branded_email_from_address,
    _get_branded_email_template,
    common_exceptions_400,
    permissions,
    require_course_permission,
    require_post_params,
)

User = get_user_model()

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
    Send email API view wrapper.

    Extracted from: lms.djangoapps.instructor.views.api import send_email
    """
    return send_email(request, course_id)


@transaction.non_atomic_requests
@require_GET
@ensure_csrf_cookie
@require_course_permission(permissions.EMAIL)
@common_exceptions_400
def search_learner_api_view(request, course_id):
    """
    Search for learners api view.
    """
    return search_learner(request, course_id)


def send_email(request, course_id):
    """
    Send an email to self, staff, cohorts, or everyone involved in a course.

    Arguments:
    - 'request' is the request object
        - body params:
            - 'send_to' specifies what group the email should be sent to
                Options are defined by the CourseEmail model in
                lms/djangoapps/bulk_email/models.py
            - 'subject' specifies email's subject
            - 'message' specifies email's content
            - 'schedule' specifies when the email should be sent
            - 'extra_targets' specifies additional targets to send the email to.
    - 'course_id' is the course id
    """
    course_id = CourseKey.from_string(course_id)
    course_overview = get_course_overview_or_none(course_id)

    if not is_bulk_email_feature_enabled(course_id):
        log.warning(f"Email is not enabled for course {course_id}")
        return JsonResponse(
            {"message": "Email is not enabled for this course."}, status=403
        )

    extra_targets = json.loads(request.POST.get("extra_targets", "{}"))
    targets = json.loads(request.POST.get("send_to"))
    subject = request.POST.get("subject")
    message = request.POST.get("message")
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

    task_api.submit_bulk_course_email(
        request, course_id, email.id, schedule_dt, extra_targets
    )

    return JsonResponse(
        {
            "course_id": str(course_id),
            "success": True,
        }
    )


def search_learner(request, course_id):
    """
    Search for learners based on the query param.
    """
    course_id = CourseKey.from_string(course_id)
    query = request.GET.get("query", "")

    queryset = User.objects.filter(
        is_active=True,
        courseenrollment__course_id=course_id,
        courseenrollment__is_active=True,
    )
    if query:
        cache_key = f"search_learner_{course_id}_{query}"
        data = cache.get(cache_key)
        if data:
            queryset = data
        else:
            queryset = queryset.filter(
                models.Q(  # pylint: disable=unsupported-binary-operation
                    email__icontains=query
                )
                | models.Q(username__icontains=query)
                | models.Q(profile__name__icontains=query),
            ).distinct()
            cache.set(cache_key, queryset, 60)

    page_number = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 50)
    paginator = Paginator(queryset, page_size)
    result_page = paginator.get_page(page_number)
    data = UserSearchSerializer(result_page, many=True).data

    response_data = {
        "course_id": str(course_id),
        "page": page_number,
        "pages": paginator.num_pages,
        "page_size": paginator.per_page,
        "total": paginator.count,
        "results": data,
    }

    return JsonResponse(response_data)
