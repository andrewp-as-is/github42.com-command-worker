__all__ = ['Page','PageBase']

from django.db import models


class Page(models.Model):
    url = models.TextField(unique=True)
    status = models.IntegerField(null=True)
    etag = models.TextField(null=True)

    checked_at = models.DateTimeField(null=True)
    # updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'pages_page'
        managed = False


class PageBase(models.Model):
    url = models.TextField(unique=True)

    class Meta:
        db_table = 'pages_page'
        managed = False

class Pagination(models.Model):
    page = models.OneToOneField('Page', on_delete=models.CASCADE)

    class Meta:
        db_table = 'pages_pagination'
        managed = False

class PaginationPage(models.Model):
    pagination = models.ForeignKey('Pagination', on_delete=models.CASCADE)
    page = models.IntegerField()
    is_downloaded = models.BooleanField(default=False)

    class Meta:
        db_table = 'pages_pagination_page'
        managed = False
        unique_together = [('pagination', 'page')]
