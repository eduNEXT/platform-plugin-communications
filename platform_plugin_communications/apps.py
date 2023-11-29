"""
platform_plugin_communications Django application initialization.
"""

from django.apps import AppConfig

try:
    from openedx.core.constants import COURSE_ID_PATTERN
except ImportError:
    COURSE_ID_PATTERN = object()


class PlatformPluginCommunicationsConfig(AppConfig):
    """
    Configuration for the platform_plugin_communications Django application.
    """

    name = "platform_plugin_communications"

    plugin_app = {
        "url_config": {
            "lms.djangoapp": {
                "namespace": "platform_plugin_communications",
                "regex": rf"platform-plugin-communications/{COURSE_ID_PATTERN}/api/",
                "relative_path": "urls",
            }
        },
        "settings_config": {
            "lms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
        },
    }
