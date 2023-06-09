from configurations import values
from django_configurations_autoenv import AutoenvMixin
from django_configurations_base import BaseConfiguration
from django_configurations_installed_apps import InstalledAppsMixin


class Base(AutoenvMixin, InstalledAppsMixin, BaseConfiguration):
    DATABASES = values.DatabaseURLValue(environ_name='DJANGO_DATABASE_URL')
    DJANGO_ALLOW_ASYNC_UNSAFE = True
    ALLOW_ASYNC_UNSAFE = True


class Dev(Base):
    DEBUG = True


class Prod(Base):
    DEBUG = False

try:
    import psycopg2
except ImportError:
    # Fall back to psycopg2cffi
    from psycopg2cffi import compat
    compat.register()
