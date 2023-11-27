"""
Wrapper methods of courseware.courses in edx-platform.
"""
from importlib import import_module

from django.conf import settings


def get_course(*args, **kwargs):
    """
    Wrapper method of get_course_overview_or_none in edx-platform.
    """
    backend_function = (
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_COURSEWARE_COURSES_BACKEND
    )
    backend = import_module(backend_function)

    return backend.get_course(*args, **kwargs)
