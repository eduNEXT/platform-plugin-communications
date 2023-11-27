"""
Backend for instructor.views.api module.
"""
from functools import wraps
from unittest.mock import Mock

_get_branded_email_from_address = Mock()
_get_branded_email_from_address.return_value = "test@openedx.org"

_get_branded_email_template = Mock()
_get_branded_email_template.return_value = "test_template"

permissions = Mock()
permissions.EMAIL = object


def require_course_permission(*args, **kwargs):
    def decorator(func, *args, **kwargs):
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    return decorator


def require_post_params(*args, **kwargs):
    def decorator(func, *args, **kwargs):
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    return decorator


def common_exceptions_400(*args, **kwargs):
    def decorator(func, *args, **kwargs):
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    return decorator
