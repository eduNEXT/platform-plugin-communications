"""
For more information on this file, see
https://docs.djangoproject.com/en/2.22/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.22/ref/settings/
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND",
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND,
    )
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND",
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND,
    )
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_COURSE_OVERVIEWS_API_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_COMMUNICATIONS_COURSE_OVERVIEWS_API_BACKEND",
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_COURSE_OVERVIEWS_API_BACKEND,
    )
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_UTIL_QUERY_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_COMMUNICATIONS_UTIL_QUERY_BACKEND",
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_UTIL_QUERY_BACKEND,
    )
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND",
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND,
    )
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_COURSEWARE_COURSES_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_COMMUNICATIONS_COURSEWARE_COURSES_BACKEND",
        settings.PLATFORM_PLUGIN_COMMUNICATIONS_COURSEWARE_COURSES_BACKEND,
    )
