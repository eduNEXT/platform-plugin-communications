"""
Target module for platform_plugin_communications.
"""
from django.contrib.auth import get_user_model

from platform_plugin_communications.edxapp_wrapper.util_query import use_read_replica_if_available

User = get_user_model()


class Target:
    """
    Base class for targets.

    A target is a way to select a set of users to send a message to. This base class
    defines the interface for targets, and provides a registry for targets to be
    registered with.
    """

    name = None
    __registry__ = {}

    def get_queryset(self, course_id, value):
        """
        Return a queryset of users to send a message to.
        """
        raise NotImplementedError

    def __init_subclass__(cls) -> None:
        """
        Register subclasses in the registry.
        """
        if not cls.name:
            raise NotImplementedError("Target.name must be set")
        super().__init_subclass__()
        cls.__registry__[cls.name] = cls

    @classmethod
    def target_for_name(cls, name) -> "Target":
        """
        Return the target class for the given name.
        """
        target_class = cls.__registry__.get(name, None)
        if target_class:
            return target_class()
        raise ValueError(f"Unknown target {name}")


class TargetEmails(Target):
    """
    Target to send a message to a list of emails.
    """

    name = "emails"

    def get_queryset(self, course_id, value):
        """
        Return a queryset of users to send a message to.
        """
        return use_read_replica_if_available(
            User.objects.filter(
                email__in=value,
                is_active=True,
                courseenrollment__course_id=course_id,
                courseenrollment__is_active=True,
            )
        )
