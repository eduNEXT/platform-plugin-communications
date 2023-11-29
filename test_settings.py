"""
These settings are here to use during tests, because django requires them.

In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "default.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "platform_plugin_communications",
)

LOCALE_PATHS = [
    root("platform_plugin_communications", "conf", "locale"),
]

ROOT_URLCONF = "platform_plugin_communications.urls"

SECRET_KEY = "insecure-secret-key"

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",  # this is required for admin
                "django.contrib.messages.context_processors.messages",  # this is required for admin
            ],
        },
    }
]

PLATFORM_PLUGIN_COMMUNICATIONS_BULK_EMAIL_API_BACKEND = (
    "platform_plugin_communications.edxapp_wrapper.backends.bulk_email_api_p_v1_test"
)
PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_VIEWS_API_BACKEND = "platform_plugin_communications.edxapp_wrapper.backends.instructor_views_p_v1_test"
PLATFORM_PLUGIN_COMMUNICATIONS_COURSE_OVERVIEWS_BACKEND = "platform_plugin_communications.edxapp_wrapper.backends.course_overviews_p_v1_test"
PLATFORM_PLUGIN_COMMUNICATIONS_UTIL_QUERY_BACKEND = (
    "platform_plugin_communications.edxapp_wrapper.backends.util_query_p_v1_test"
)
PLATFORM_PLUGIN_COMMUNICATIONS_INSTRUCTOR_TASKS_BACKEND = (
    "platform_plugin_communications.edxapp_wrapper.backends.instructor_tasks_p_v1_test"
)
PLATFORM_PLUGIN_COMMUNICATIONS_COURSEWARE_COURSES_BACKEND = "platform_plugin_communications.edxapp_wrapper.backends.courseware_courses_p_v1_test"

BULK_EMAIL_EMAILS_PER_TASK = 1
