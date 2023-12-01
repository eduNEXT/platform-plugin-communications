"""
Backend for util.query module.
"""


def use_read_replica_if_available(queryset):
    """
    Use the read replica if it is available.
    """
    return queryset
