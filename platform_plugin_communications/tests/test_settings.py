from django.conf import settings
from django.test import TestCase

from platform_plugin_communications.settings import common as common_settings
from platform_plugin_communications.settings import production as production_settings


class SettingsTestCase(TestCase):
    """
    Tests for the settings module.
    """

    def setUp(self) -> None:
        """
        Set up the test case.
        """
        self.common_settings = common_settings
        self.production_settings = production_settings

    def test_common_settings(self):
        common_settings.plugin_settings(settings)

    def test_production_settings(self):
        production_settings.plugin_settings(settings)
