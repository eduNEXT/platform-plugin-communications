"""
For more information on this file, see
https://docs.djangoproject.com/en/2.22/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.22/ref/settings/
"""
INSTALLED_APPS = [
    "filesmanager",
]


def plugin_settings(settings):  # pylint: disable=unused-argument
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND = (
        "platform_plugin_communications.edxapp_wrapper.backends.bulk_email_api_p_v1"
    )
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND = "platform_plugin_communications.edxapp_wrapper.backends.instructor_views_api_p_v1"
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_COURSE_OVERVIEWS_API_BACKEND = "platform_plugin_communications.edxapp_wrapper.backends.course_overviews_api_p_v1"
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_UTIL_QUERY_BACKEND = (
        "platform_plugin_communications.edxapp_wrapper.backends.util_query_p_v1"
    )
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND = (
        "platform_plugin_communications.edxapp_wrapper.backends.instructor_tasks_p_v1"
    )
    settings.PLATFORM_PLUGIN_COMMUNICATIONS_COURSEWARE_COURSES_BACKEND = (
        "platform_plugin_communications.edxapp_wrapper.backends.courseware_courses_p_v1"
    )
