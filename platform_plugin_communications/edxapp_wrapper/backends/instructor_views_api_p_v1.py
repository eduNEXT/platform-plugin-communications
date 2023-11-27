"""
Backend for instructor.views.api module.
"""

from lms.djangoapps.instructor.views.api import (
    _get_branded_email_from_address,
    _get_branded_email_template,
    common_exceptions_400,
    permissions,
    require_course_permission,
    require_post_params,
)
