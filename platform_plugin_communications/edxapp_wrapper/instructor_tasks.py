"""
Wrapper methods of instructor_tasks in edx-platform.
"""
from importlib import import_module

from django.conf import settings


def run_main_task(*args, **kwargs):
    """
    Wrapper method of run_main_task in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND
    backend = import_module(backend_function)

    return backend.run_main_task(*args, **kwargs)


def send_course_email():
    """
    Wrapper method of send_course_email in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND
    backend = import_module(backend_function)

    return backend.send_course_email


def queue_subtasks_for_query(*args, **kwargs):
    """
    Wrapper method of queue_subtasks_for_query in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND
    backend = import_module(backend_function)

    return backend.queue_subtasks_for_query(*args, **kwargs)


def get_instructor_task_model():
    """
    Wrapper method of get_instructor_task_model in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND
    backend = import_module(backend_function)

    return backend.InstructorTask


def schedule_task(*args, **kwargs):
    """
    Wrapper method of schedule_task in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND
    backend = import_module(backend_function)

    return backend.schedule_task(*args, **kwargs)


def submit_task(*args, **kwargs):
    """
    Wrapper method of submit_task in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND
    backend = import_module(backend_function)

    return backend.submit_task(*args, **kwargs)


def get_instructor_tasks_types():
    """
    Wrapper method to get the InstructorTaskTypes model in edx-platform.
    """
    backend_function = settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND
    backend = import_module(backend_function)

    return backend.InstructorTaskTypes


InstructorTask = get_instructor_task_model()
InstructorTaskTypes = get_instructor_tasks_types()
send_course_email = send_course_email()
