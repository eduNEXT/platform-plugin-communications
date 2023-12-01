"""
Instructor views API public function definitions.
"""
from importlib import import_module

from django.conf import settings


def use_read_replica_if_available(*args, **kwargs):
    """
    Wrapper method of _get_branded_email_from_address in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_UTIL_QUERY_BACKEND
    backend = import_module(backend_function)

    return backend.use_read_replica_if_available(*args, **kwargs)
