__all__ = ['Response']

from django.db import models

from .mixins import HeadersMixin

class Response(HeadersMixin,models.Model):
    url = models.TextField()
    page_id = models.IntegerField(null=True)
    proxy_id = models.IntegerField(null=True)

    status = models.IntegerField()
    headers = models.TextField(null=True)

    class Meta:
        db_table = __name__.split('.')[-1]
        managed = False
