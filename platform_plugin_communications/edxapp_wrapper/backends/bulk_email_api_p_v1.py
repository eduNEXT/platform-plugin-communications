"""
Backend for bulk_email.api module.
"""
from lms.djangoapps.bulk_email.api import (  # pylint: disable=import-error, unused-import
    create_course_email,
    get_course_email,
    is_bulk_email_feature_enabled,
)
from lms.djangoapps.bulk_email.models import CourseEmail  # pylint: disable=import-error, unused-import
from lms.djangoapps.bulk_email.tasks import _get_course_email_context  # pylint: disable=import-error, unused-import
