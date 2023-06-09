__all__ = ['Error']

from django.db import models

class Error(models.Model):
    url = models.TextField()
    page_id = models.IntegerField(null=True)
    proxy_id = models.IntegerField(null=True)
    headers = models.TextField(null=True) # request headers
    exc_type = models.TextField()
    exc_value = models.TextField()

    class Meta:
        db_table = __name__.split('.')[-1]
        managed = False
