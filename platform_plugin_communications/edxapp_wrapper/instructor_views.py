"""
Instructor views API public function definitions.
"""
from importlib import import_module

from django.conf import settings


def _get_branded_email_from_address(*args, **kwargs):
    """
    Wrapper method of _get_branded_email_from_address in edx-platform.
    """
    backend_function = (
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND
    )
    backend = import_module(backend_function)

    return backend._get_branded_email_from_address(  # pylint: disable=protected-access
        *args, **kwargs
    )


def _get_branded_email_template(*args, **kwargs):
    """
    Wrapper method of _get_branded_email_template in edx-platform.
    """
    backend_function = (
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND
    )
    backend = import_module(backend_function)

    return backend._get_branded_email_template(  # pylint: disable=protected-access
        *args, **kwargs
    )


def common_exceptions_400(*args, **kwargs):
    """
    Wrapper method of common_exceptions_400 in edx-platform.
    """
    backend_function = (
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND
    )
    backend = import_module(backend_function)

    return backend.common_exceptions_400(*args, **kwargs)


def permissions():
    """
    Wrapper method of permissions in edx-platform.
    """
    backend_function = (
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND
    )
    backend = import_module(backend_function)

    return backend.permissions


def require_course_permission(*args, **kwargs):
    """
    Wrapper method of require_course_permission in edx-platform.
    """
    backend_function = (
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND
    )
    backend = import_module(backend_function)

    return backend.require_course_permission(*args, **kwargs)


def require_post_params(*args, **kwargs):
    """
    Wrapper method of require_post_params in edx-platform.
    """
    backend_function = (
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND
    )
    backend = import_module(backend_function)

    return backend.require_post_params(*args, **kwargs)


permissions = permissions()
