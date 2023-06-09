__all__ = ['Request','RequestBase']

from django.db import models

from .mixins import HeadersMixin


class Request(HeadersMixin,models.Model):
    is_pushed = models.BooleanField(default=False,verbose_name='pushed')
    priority = models.IntegerField()

    url = models.TextField(unique=True)
    page_id = models.IntegerField(null=True)
    headers = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = __name__.split('.')[-1]
        managed = False

class RequestBase(models.Model):
    priority = models.IntegerField()

    url = models.TextField(unique=True)
    page_id = models.IntegerField(null=True)
    headers = models.TextField(null=True)

    class Meta:
        db_table = __name__.split('.')[-1]
        managed = False
