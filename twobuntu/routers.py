from django.conf import settings
from django.db import DEFAULT_DB_ALIAS


class ReadOnlyError(Exception):
    """
    Error raised when writing during read-only mode.
    """


class ReadOnlyAwareRouter(object):
    """
    Ensure that no write operations are performed in read-only mode.
    """

    def db_for_write(self, model, **hints):
        """
        Raise an exception when attempting to write during read-only mode.
        """
        if getattr(settings, 'READ_ONLY', False):
            raise ReadOnlyError('Write operations are not permitted when read-only mode is enabled.')
        return DEFAULT_DB_ALIAS
