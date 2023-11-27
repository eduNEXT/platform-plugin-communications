"""
Bulk email public function definitions.
"""
from importlib import import_module

from django.conf import settings


def create_course_email(*args, **kwargs):
    """
    Wrapper method of create_course_email in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND
    backend = import_module(backend_function)

    return backend.create_course_email(*args, **kwargs)


def is_bulk_email_feature_enabled(*args, **kwargs):
    """
    Wrapper method of is_bulk_email_feature_enabled in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND
    backend = import_module(backend_function)

    return backend.is_bulk_email_feature_enabled(*args, **kwargs)


def get_course_email_model():
    """
    Wrapper method of get_course_email in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND
    backend = import_module(backend_function)

    return backend.CourseEmail


def _get_course_email_context(*args, **kwargs):
    """
    Wrapper method of _get_course_email_context in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND
    backend = import_module(backend_function)

    return backend._get_course_email_context(*args, **kwargs)


def get_course_email(*args, **kwargs):
    """
    Wrapper method of get_course_email in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND
    backend = import_module(backend_function)

    return backend.get_course_email(*args, **kwargs)


CourseEmail = get_course_email_model()
